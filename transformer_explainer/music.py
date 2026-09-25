"""Procedural ambient music bed (D major / B minor pads, sub, soft plucked arpeggio).

python music.py [seconds]  -> build/music.wav (48 kHz stereo)
"""
import os
import sys

import numpy as np
import soundfile as sf

from sfx import IR_LONG, SR, lowpass, reverb

ROOT = os.path.dirname(os.path.abspath(__file__))
CHORD_DUR = 8.0
# (pad voicing as MIDI notes, bass root MIDI)
PROG = [
    ([47, 54, 57, 61, 62], 35),   # Bm9
    ([43, 50, 54, 59, 62], 31),   # Gmaj7
    ([50, 57, 61, 64, 66], 38),   # Dmaj9
    ([45, 52, 57, 59, 64], 33),   # Asus2
    ([40, 50, 55, 59, 66], 28),   # Em9
    ([43, 50, 57, 59, 64], 31),   # G6/9
    ([42, 50, 57, 62, 64], 30),   # D/F#
    ([45, 52, 55, 62, 64], 33),   # A7sus4
]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pad_chord(notes, dur, rng, attack=2.6, release=3.2):
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for m in notes:
        f = hz(m)
        for det, pan in ((-7, -0.45), (0, 0.0), (7, 0.45)):
            ff = f * 2 ** (det / 1200)
            y = np.zeros(n)
            for h in range(1, 9):
                if ff * h > 5000:
                    break
                amp = 1.0 / h ** 1.8
                y += amp * np.sin(2 * np.pi * ff * h * t + rng.uniform(0, 2 * np.pi))
            l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
            out[:, 0] += y * l
            out[:, 1] += y * r
    envv = np.ones(n)
    a = int(attack * SR)
    envv[:a] = np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    rs = int(dur * SR)
    envv[rs:] = np.cos(np.linspace(0, np.pi / 2, n - rs)) ** 2
    trem = 1 + 0.08 * np.sin(2 * np.pi * 0.11 * t + rng.uniform(0, 6))
    return out * (envv * trem)[:, None] / len(notes)


def sub_note(root, dur, release=2.0):
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    f = hz(root + 12)
    y = np.sin(2 * np.pi * f * t) + 0.15 * np.sin(2 * np.pi * 2 * f * t)
    envv = np.ones(n)
    a = int(1.5 * SR)
    envv[:a] = np.linspace(0, 1, a) ** 2
    rs = int(dur * SR)
    envv[rs:] = np.linspace(1, 0, n - rs) ** 2
    return np.stack([y * envv, y * envv], 1)


def pluck(f, vel, pan):
    d = 1.4
    t = np.arange(int(d * SR)) / SR
    y = np.sin(2 * np.pi * f * t) + 0.28 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.12) \
        + 0.08 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / 0.06)
    y *= np.minimum(t / 0.004, 1) * np.exp(-t / 0.42) * vel
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    return np.stack([y * l, y * r], 1)


def build(total):
    rng = np.random.default_rng(2017)
    n = int((total + 6) * SR)
    pad = np.zeros((n, 2))
    sub = np.zeros((n, 2))
    arp = np.zeros((n, 2))
    k = 0
    t0 = 0.0
    step = 60 / 76 / 2   # eighth notes at 76 bpm
    while t0 < total + 2:
        notes, root = PROG[k % len(PROG)]
        ch = pad_chord(notes, CHORD_DUR, rng)
        s = int(t0 * SR)
        e = min(n, s + len(ch))
        pad[s:e] += ch[: e - s]
        sb = sub_note(root, CHORD_DUR)
        e2 = min(n, s + len(sb))
        sub[s:e2] += sb[: e2 - s]
        # arpeggio over this chord (enters after the intro)
        tones = sorted(set(m + 12 for m in notes[1:]))
        pattern = [0, 2, 1, 3, 2, 4, 3, 1, 0, 2, 4, 3, 1, 2, 3, 4]
        cycle = k // len(PROG)
        for i in range(int(CHORD_DUR / step)):
            tt = t0 + i * step
            if tt < 14.0 or tt > total - 6:
                continue
            if rng.random() > (0.62 if cycle % 2 == 0 else 0.5):
                continue
            m = tones[pattern[i % len(pattern)] % len(tones)] + (12 if (cycle % 3 == 2 and i % 4 == 0) else 0)
            vel = rng.uniform(0.45, 0.85)
            p = pluck(hz(m), vel, 0.35 if i % 2 else -0.35)
            ss = int((tt + rng.uniform(-0.008, 0.008)) * SR)
            ee = min(n, ss + len(p))
            arp[ss:ee] += p[: ee - ss]
        k += 1
        t0 += CHORD_DUR
    pad = lowpass(pad.T, 2600).T
    arp_w = reverb(arp, 0.55, IR_LONG)[:n]
    pad_w = reverb(pad, 0.25, IR_LONG)[:n]
    mix = pad_w * 1.0 + sub * 0.22 + arp_w * 0.55
    # global fades
    fi, fo = int(5 * SR), int(8 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)[:, None] ** 2
    end = int(total * SR)
    mix[end - fo:end] *= np.linspace(1, 0, fo)[:, None] ** 2
    mix[end:] = 0
    mix = mix[:end]
    mix /= np.max(np.abs(mix)) + 1e-9
    return mix * 10 ** (-3 / 20)


if __name__ == "__main__":
    total = float(sys.argv[1]) if len(sys.argv) > 1 else 960.0
    y = build(total)
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    sf.write(os.path.join(ROOT, "build", "music.wav"), y.astype(np.float32), SR)
    print("music", len(y) / SR, "s")
