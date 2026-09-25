"""Procedural sound design: every effect and the music bed are synthesised here.

python sfx.py            -> writes build/sfx/*.wav (48 kHz stereo)
"""
import os

import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "build", "sfx")
RNG = np.random.default_rng(1234)

# D major pentatonic, handy for anything tonal so it sits with the music bed
NOTE = {"D4": 293.66, "E4": 329.63, "F#4": 369.99, "A4": 440.0, "B4": 493.88, "D5": 587.33, "E5": 659.25,
        "F#5": 739.99, "A5": 880.0, "B5": 987.77, "D6": 1174.66, "E6": 1318.51, "F#6": 1479.98, "A6": 1760.0,
        "B6": 1975.53, "D7": 2349.32}


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def env_ad(n, attack=0.005, decay=0.2, curve=1.0):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    d = np.exp(-np.maximum(t - attack, 0) / max(decay, 1e-4)) ** curve
    return a * d


def fade(x, fin=0.003, fout=0.01):
    x = x.copy()
    ni, no = int(fin * SR), int(fout * SR)
    if ni:
        x[:ni] *= np.linspace(0, 1, ni)
    if no:
        x[-no:] *= np.linspace(1, 0, no)
    return x


def sweep_sine(f0, f1, dur, shape="exp"):
    t = t_axis(dur)
    if shape == "exp":
        f = f0 * (f1 / f0) ** (t / dur)
    else:
        f = f0 + (f1 - f0) * t / dur
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph)


def bandpass(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def lowpass(x, fc, order=2):
    sos = signal.butter(order, fc, btype="low", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def highpass(x, fc, order=2):
    sos = signal.butter(order, fc, btype="high", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def moving_band_noise(dur, centres, widths=None, env=None, seed=0):
    """Noise whose spectral band follows `centres` (Hz, sampled over the duration)."""
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    x = rng.standard_normal(n)
    f, tt, Z = signal.stft(x, fs=SR, nperseg=1024, noverlap=768)
    k = Z.shape[1]
    c = np.interp(np.linspace(0, 1, k), np.linspace(0, 1, len(centres)), np.log(centres))
    w = np.full(k, 0.55) if widths is None else np.interp(np.linspace(0, 1, k), np.linspace(0, 1, len(widths)), widths)
    lf = np.log(np.maximum(f, 20.0))[:, None]
    mask = np.exp(-0.5 * ((lf - c[None, :]) / w[None, :]) ** 2)
    _, y = signal.istft(Z * mask, fs=SR, nperseg=1024, noverlap=768)
    y = y[:n]
    if env is not None:
        y = y * np.interp(np.linspace(0, 1, n), np.linspace(0, 1, len(env)), env)
    return y


def make_ir(rt60=1.2, dur=None, seed=7, bright=6000):
    dur = dur or rt60 * 1.2
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    t = np.arange(n) / SR
    decay = np.exp(-6.9 * t / rt60)
    irl = rng.standard_normal(n) * decay
    irr = rng.standard_normal(n) * decay
    irl, irr = lowpass(irl, bright), lowpass(irr, bright)
    pre = int(0.012 * SR)
    irl[:pre] = 0
    irr[:pre] = 0
    irl /= np.sqrt(np.sum(irl ** 2))
    irr /= np.sqrt(np.sum(irr ** 2))
    return np.stack([irl, irr], 1)


IR_SHORT = make_ir(0.9, seed=3, bright=7000)
IR_LONG = make_ir(2.4, seed=5, bright=5000)


def reverb(x, wet=0.25, ir=IR_SHORT):
    """x: mono or stereo -> stereo with convolution reverb."""
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    n = x.shape[0] + ir.shape[0] - 1
    out = np.zeros((n, 2))
    out[:x.shape[0]] += x * (1 - wet * 0.5)
    for ch in range(2):
        out[:, ch] += wet * signal.fftconvolve(x[:, ch], ir[:, ch])[:n]
    return out


def stereo(x, pan=0.0, width=0.0, seed=0):
    """Mono -> stereo with constant-power pan and optional decorrelated width."""
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    L, R = x * l * np.sqrt(2), x * r * np.sqrt(2)
    if width > 0:
        d = int(0.0007 * SR)
        R = (1 - width) * R + width * np.concatenate([np.zeros(d), R[:-d]])
    return np.stack([L, R], 1)


def pan_sweep(x, p0, p1):
    p = np.linspace(p0, p1, len(x))
    l = np.cos((p + 1) * np.pi / 4)
    r = np.sin((p + 1) * np.pi / 4)
    return np.stack([x * l, x * r], 1) * np.sqrt(2)


def tone(freq, dur, partials=((1, 1.0),), decay=0.4, attack=0.003):
    t = t_axis(dur)
    y = np.zeros_like(t)
    for mult, amp in partials:
        y += amp * np.sin(2 * np.pi * freq * mult * t) * np.exp(-t / (decay / max(mult, 1) ** 0.5))
    return y * np.clip(t / attack, 0, 1)


# ------------------------------------------------------------------ effects
def fx_pop():
    d = 0.14
    y = sweep_sine(950, 380, d) * env_ad(int(d * SR), 0.002, 0.035)
    click = highpass(RNG.standard_normal(int(0.006 * SR)), 2500) * np.linspace(1, 0, int(0.006 * SR)) * 0.25
    y[:len(click)] += click
    return reverb(fade(y), 0.12)


def fx_pop_soft():
    d = 0.16
    y = sweep_sine(620, 300, d) * env_ad(int(d * SR), 0.004, 0.045)
    return reverb(fade(lowpass(y, 3000)), 0.15)


def fx_tick():
    n = int(0.03 * SR)
    y = bandpass(RNG.standard_normal(n), 2500, 7000) * env_ad(n, 0.0005, 0.004)
    y += 0.35 * np.sin(2 * np.pi * 2200 * np.arange(n) / SR) * env_ad(n, 0.0005, 0.006)
    return stereo(fade(y, 0.0005, 0.005))


def fx_click():
    n = int(0.05 * SR)
    y = np.zeros(n)
    for off, amp in ((0, 1.0), (int(0.004 * SR), 0.6)):
        m = n - off
        y[off:] += amp * bandpass(RNG.standard_normal(m), 1800, 5000) * env_ad(m, 0.0003, 0.005)
    y += 0.4 * np.sin(2 * np.pi * 900 * np.arange(n) / SR) * env_ad(n, 0.0005, 0.01)
    return stereo(fade(y, 0.0005, 0.01))


def fx_blip():
    d = 0.22
    y = sweep_sine(NOTE["A5"], NOTE["D6"], 0.06)
    y = np.concatenate([y, np.sin(2 * np.pi * NOTE["D6"] * t_axis(d - 0.06) + 0.0)])
    y = y * env_ad(len(y), 0.003, 0.07)
    y += 0.25 * np.sin(2 * np.pi * NOTE["D6"] * 2 * t_axis(d)) * env_ad(len(y), 0.003, 0.03)
    return reverb(fade(y), 0.18)


def fx_blip_down():
    d = 0.24
    y = sweep_sine(NOTE["B5"], NOTE["E5"], d) * env_ad(int(d * SR), 0.003, 0.08)
    return reverb(fade(y), 0.2)


def fx_tone(up=True):
    d = 1.0
    f0, f1 = (NOTE["A4"], NOTE["E5"]) if up else (NOTE["E5"], NOTE["A4"])
    y = sweep_sine(f0, f1, d, "lin")
    y += 0.3 * sweep_sine(f0 * 2, f1 * 2, d, "lin")
    envv = np.sin(np.pi * np.linspace(0, 1, len(y))) ** 1.5
    return reverb(fade(lowpass(y * envv, 4000), 0.02, 0.05), 0.3)


def fx_whoosh(soft=False, short=False):
    if short:
        d, cents, env = 0.35, [1800, 5200, 3000], [0, 1, 0.2, 0]
    elif soft:
        d, cents, env = 0.85, [220, 900, 1500, 500], [0, 0.6, 1, 0.5, 0]
    else:
        d, cents, env = 0.75, [300, 1400, 2600, 700], [0, 0.5, 1, 0.35, 0]
    y = moving_band_noise(d, cents, [0.5, 0.6, 0.7, 0.6], env, seed=int(RNG.integers(1e6)))
    y = fade(y, 0.01, 0.05)
    out = pan_sweep(y, -0.6, 0.6)
    return reverb(out, 0.18)


def fx_shimmer(dur=0.9, density=14, bright=False):
    n = int((dur + 1.0) * SR)
    out = np.zeros((n, 2))
    notes = ["D6", "E6", "F#6", "A6", "B6", "D7"] if bright else ["A5", "B5", "D6", "E6", "F#6", "A6"]
    for _ in range(density):
        f = NOTE[notes[RNG.integers(len(notes))]]
        st = int(RNG.uniform(0, dur) * SR)
        g = tone(f, 0.6, ((1, 1.0), (2.0, 0.2), (3.0, 0.08)), decay=0.22, attack=0.004) * RNG.uniform(0.3, 0.8)
        pan = RNG.uniform(-0.7, 0.7)
        s = stereo(g, pan)
        out[st:st + len(s)] += s[: n - st]
    envv = np.linspace(0.6, 1.0, n)[:, None]
    return reverb(out * envv, 0.45, IR_LONG)


def fx_chime(soft=False):
    f = NOTE["A5"] if soft else NOTE["D6"]
    d = 2.0
    parts = ((1, 1.0), (2.0, 0.25), (3.0, 0.1)) if soft else ((1, 1.0), (2.76, 0.35), (5.4, 0.18), (8.9, 0.08))
    y = tone(f, d, parts, decay=0.5 if soft else 0.8, attack=0.002)
    y += 0.5 * tone(f * 1.5, d, ((1, 1.0),), decay=0.35, attack=0.003) if not soft else 0
    return reverb(fade(y, 0.001, 0.2), 0.35, IR_LONG)


def fx_ding():
    y = tone(NOTE["F#6"], 1.5, ((1, 1.0), (2.0, 0.3), (3.0, 0.12)), decay=0.5, attack=0.002)
    y += 0.4 * tone(NOTE["A6"], 1.5, ((1, 1.0),), decay=0.35, attack=0.002)
    return reverb(fade(y, 0.001, 0.2), 0.3, IR_LONG)


def fx_thud():
    d = 0.5
    y = sweep_sine(85, 42, d) * env_ad(int(d * SR), 0.004, 0.12)
    nz = lowpass(RNG.standard_normal(int(d * SR)), 400) * env_ad(int(d * SR), 0.001, 0.03) * 0.5
    return reverb(fade(y + nz, 0.001, 0.05), 0.12)


def fx_impact(soft=False):
    d = 2.5
    boom = sweep_sine(62 if not soft else 70, 34, d) * env_ad(int(d * SR), 0.004, 0.55 if not soft else 0.35)
    nz = lowpass(RNG.standard_normal(int(d * SR)), 1800 if not soft else 900) * env_ad(int(d * SR), 0.001, 0.09)
    body = sweep_sine(180, 90, d) * env_ad(int(d * SR), 0.002, 0.08) * 0.4
    y = boom * 1.0 + nz * (0.45 if not soft else 0.25) + body
    if not soft:
        y += 0.3 * tone(NOTE["D5"], d, ((1, 1.0), (2.0, 0.4), (3.0, 0.2)), decay=0.9)
    return reverb(fade(y, 0.001, 0.3), 0.35, IR_LONG)


def fx_riser(dur=2.9):
    env = np.linspace(0, 1, 50) ** 2.2
    nz = moving_band_noise(dur, [250, 800, 2500, 6000], [0.6, 0.6, 0.7, 0.8], env, seed=77)
    t = t_axis(dur)
    sw = sweep_sine(NOTE["D4"], NOTE["D5"], dur, "exp") * (t / dur) ** 2.5 * 0.35
    sw += sweep_sine(NOTE["A4"], NOTE["A5"], dur, "exp") * (t / dur) ** 2.5 * 0.2
    y = nz + sw
    y = fade(y, 0.05, 0.02)
    return reverb(stereo(y, 0, 0.6), 0.2)


def fx_power_up():
    d = 1.2
    n = int(d * SR)
    y = np.zeros(n)
    for k, nm in enumerate(["D5", "F#5", "A5", "D6", "F#6", "A6"]):
        st = int(k * 0.06 * SR)
        g = tone(NOTE[nm], d - k * 0.06, ((1, 1.0), (2, 0.2)), decay=0.25, attack=0.003) * (0.6 + 0.08 * k)
        y[st:st + len(g)] += g[: n - st]
    y += 0.3 * moving_band_noise(d, [800, 4000], None, [0, 1, 0.3, 0], seed=9)
    return reverb(y, 0.35, IR_LONG)


def fx_swell(dur=1.4):
    t = t_axis(dur)
    nz = highpass(RNG.standard_normal(len(t)), 2500) * (t / dur) ** 3
    nz = fade(nz, 0.01, 0.12)
    return reverb(stereo(nz, 0, 0.8), 0.3, IR_LONG)


def fx_ticks_fast(dur=1.1, count=28):
    n = int((dur + 0.1) * SR)
    y = np.zeros(n)
    tick = fx_tick()[:, 0]
    for k in range(count):
        st = int((k / count) * dur * SR + RNG.uniform(-0.004, 0.004) * SR)
        st = max(st, 0)
        a = 0.9 - 0.5 * k / count
        y[st:st + len(tick)] += a * tick[: n - st]
    return stereo(y, 0, 0.3)


def fx_glitch():
    d = 0.4
    n = int(d * SR)
    y = np.zeros(n)
    pos = 0
    while pos < n:
        seg = int(RNG.uniform(0.012, 0.05) * SR)
        kind = RNG.integers(3)
        if kind == 0:
            s = np.sign(np.sin(2 * np.pi * RNG.uniform(200, 900) * np.arange(seg) / SR)) * 0.4
        elif kind == 1:
            s = RNG.standard_normal(seg) * 0.5
            s = np.round(s * 4) / 4
        else:
            s = np.zeros(seg)
        y[pos:pos + seg] = s[: n - pos]
        pos += seg
    y = lowpass(y, 5000) * env_ad(n, 0.002, 0.2)
    return stereo(fade(y, 0.002, 0.03), 0, 0.5)


def fx_fail():
    y = np.concatenate([tone(NOTE["A4"], 0.18, ((1, 1.0), (3, 0.3), (5, 0.12)), decay=0.25),
                        tone(349.23, 0.4, ((1, 1.0), (3, 0.3), (5, 0.12)), decay=0.25)])
    return reverb(fade(lowpass(y, 2500), 0.002, 0.05), 0.2)


def fx_type():
    n = int(0.26 * SR)
    y = np.zeros(n)
    for k in range(4):
        st = int((k * 0.055 + RNG.uniform(0, 0.012)) * SR)
        m = int(0.03 * SR)
        key = bandpass(RNG.standard_normal(m), 1500, 5000) * env_ad(m, 0.0004, 0.004)
        key += 0.5 * np.sin(2 * np.pi * 160 * np.arange(m) / SR) * env_ad(m, 0.001, 0.008)
        y[st:st + m] += key[: n - st] * RNG.uniform(0.6, 1.0)
    return stereo(y, 0, 0.3)


EFFECTS = {
    "pop": fx_pop, "pop_soft": fx_pop_soft, "tick": fx_tick, "click": fx_click, "blip": fx_blip,
    "blip_down": fx_blip_down, "tone_up": lambda: fx_tone(True), "tone_down": lambda: fx_tone(False),
    "whoosh": lambda: fx_whoosh(), "whoosh_soft": lambda: fx_whoosh(soft=True), "swish": lambda: fx_whoosh(short=True),
    "shimmer": lambda: fx_shimmer(), "sparkle": lambda: fx_shimmer(1.4, 26, True), "chime": lambda: fx_chime(False),
    "chime_soft": lambda: fx_chime(True), "ding": fx_ding, "thud": fx_thud, "impact": lambda: fx_impact(False),
    "impact_soft": lambda: fx_impact(True), "riser": lambda: fx_riser(2.9), "riser_short": lambda: fx_riser(1.3),
    "power_up": fx_power_up, "swell": fx_swell, "ticks_fast": fx_ticks_fast, "glitch": fx_glitch, "fail": fx_fail,
    "type": fx_type,
}


def normalise(x, peak_db=-3.0):
    p = np.max(np.abs(x)) + 1e-9
    return x / p * 10 ** (peak_db / 20)


def build_all():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in EFFECTS.items():
        y = fn()
        if y.ndim == 1:
            y = stereo(y)
        y = normalise(y, -3.0)
        sf.write(os.path.join(OUT, f"{name}.wav"), y.astype(np.float32), SR)
        print(f"{name:12s} {len(y) / SR:5.2f}s")


if __name__ == "__main__":
    build_all()
