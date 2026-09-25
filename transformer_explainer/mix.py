"""Assemble the soundtrack from the per-scene event logs written during rendering.

python mix.py [quality_dir]   (default 1080p60)
Writes build/mix.wav, build/subtitles.srt and build/concat.txt (scene video list).
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

import music
from sfx import SR, highpass

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(ROOT, "build")
SCENES = [("s01_coldopen", "S01_ColdOpen"), ("s02_recurrence", "S02_Recurrence"), ("s03_vectors", "S03_Vectors"),
          ("s04_lookup", "S04_Lookup"), ("s05_selfattention", "S05_SelfAttention"), ("s06_whythree", "S06_WhyThree"),
          ("s07_matrix", "S07_Matrix"), ("s08_multihead", "S08_MultiHead"), ("s09_position", "S09_Position"),
          ("s10_encoder", "S10_EncoderLayer"), ("s11_decoder", "S11_Decoder"), ("s12_legacy", "S12_Legacy"),
          ("s13_recap", "S13_Recap")]

VO_LUFS = -19.0        # each narration clip normalised to this before mixing
SFX_BUS_DB = -7.0      # sfx bus trim (effects are peak-normalised to -3 dBFS)
MUSIC_DB = -11.0       # music relative level (music is peak-normalised to -3 dBFS)
SFX_TRIM = {"tick": 8, "click": 6, "type": 8, "blip_down": 4, "ticks_fast": 5, "ding": -3, "chime": -2, "glitch": 3,
            "pop": 2, "pop_soft": 2}
DUCK_DB = -7.0         # extra music attenuation while the narrator speaks
TARGET_LUFS = -16.0
CEILING_DB = -1.2


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                         capture_output=True, text=True).stdout
    return float(json.loads(out)["format"]["duration"])


def place(bus, clip, t):
    s = int(round(t * SR))
    if s >= len(bus):
        return
    e = min(len(bus), s + len(clip))
    bus[s:e] += clip[: e - s]


def smooth_env(x, attack, release, hop):
    y = np.zeros_like(x)
    a = np.exp(-hop / attack)
    r = np.exp(-hop / release)
    v = 0.0
    for i, xi in enumerate(x):
        c = a if xi > v else r
        v = c * v + (1 - c) * xi
        y[i] = v
    return y


def limiter(x, ceiling_db=-1.0, lookahead=0.005, release=0.12):
    """Look-ahead peak limiter (vectorised): min-filtered gain, smoothed, then a safety clip."""
    from scipy.ndimage import minimum_filter1d
    ceiling = 10 ** (ceiling_db / 20)
    peak = np.max(np.abs(x), axis=1)
    need = np.minimum(1.0, ceiling / np.maximum(peak, 1e-9))
    la = int(lookahead * SR)
    g = minimum_filter1d(need, size=2 * la + 1, mode="nearest")
    a = np.exp(-1 / (release * SR))
    g_rel = signal.lfilter([1 - a], [1, -a], g - 1.0) + 1.0   # smooth recovery
    g = np.minimum(g, g_rel)
    g = minimum_filter1d(g, size=la + 1, mode="nearest")
    y = x * g[:, None]
    return np.clip(y, -ceiling, ceiling)


def srt_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def main():
    qdir = sys.argv[1] if len(sys.argv) > 1 else "1080p60"
    meter = pyln.Meter(SR)
    offsets, durs, vids = [], [], []
    t = 0.0
    for stem, cls in SCENES:
        vid = os.path.join(BUILD, "media", "videos", stem, qdir, f"{cls}.mp4")
        ev = json.load(open(os.path.join(BUILD, "events", f"{cls}.json")))
        d = probe_duration(vid)
        if abs(d - ev["duration"]) > 0.06:
            print(f"WARNING {cls}: video {d:.3f}s vs log {ev['duration']:.3f}s")
        offsets.append(t)
        durs.append(d)
        vids.append(vid)
        t += d
    total = t
    print(f"total {total:.2f}s ({total / 60:.2f} min)")
    titles = ["Intro: what does 'it' mean?", "01 Why not recurrence?", "02 Words as vectors", "03 Query, key, value",
              "04 Self-attention", "05 Why three projections?", "06 The equation", "07 Multi-head attention",
              "08 Word order", "09 Into the network", "10 The decoder", "11 Impact", "12 Recap"]
    with open(os.path.join(BUILD, "chapters.txt"), "w") as f:
        f.write(";FFMETADATA1\ntitle=Attention Is All You Need - explained\n")
        for title, off, d in zip(titles, offsets, durs):
            f.write(f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(off * 1000)}\nEND={int((off + d) * 1000)}\ntitle={title}\n")
    with open(os.path.join(BUILD, "concat.txt"), "w") as f:
        for v in vids:
            f.write(f"file '{v}'\n")

    n = int((total + 1) * SR)
    vo = np.zeros((n, 2))
    fx = np.zeros((n, 2))
    sfx_cache = {}
    subs = []
    manifest = json.load(open(os.path.join(BUILD, "vo", "manifest.json")))
    for (stem, cls), off in zip(SCENES, offsets):
        ev = json.load(open(os.path.join(BUILD, "events", f"{cls}.json")))
        for e in ev["events"]:
            if e["type"] == "vo":
                y, sr = sf.read(e["file"])
                y = signal.resample_poly(y, SR, sr)
                y = highpass(y, 75)
                loud = meter.integrated_loudness(y)
                y = y * 10 ** ((VO_LUFS - loud) / 20)
                place(vo, np.stack([y, y], 1), off + e["t"])
                words = manifest[cls][e["key"]]["words"]
                subs.append((off + e["t"], words))
            else:
                if e["name"] not in sfx_cache:
                    sfx_cache[e["name"]] = sf.read(os.path.join(BUILD, "sfx", f"{e['name']}.wav"))[0]
                gdb = e["gain"] + SFX_BUS_DB + SFX_TRIM.get(e["name"], 0)
                place(fx, sfx_cache[e["name"]] * 10 ** (gdb / 20), off + e["t"])

    mus = music.build(total + 0.5)
    mus = np.concatenate([mus, np.zeros((max(0, n - len(mus)), 2))])[:n]
    # ducking envelope from the narration
    hop = 0.01
    h = int(hop * SR)
    frames = len(vo) // h
    rms = np.sqrt(np.mean(vo[: frames * h, 0].reshape(frames, h) ** 2, axis=1))
    active = (20 * np.log10(rms + 1e-9) > -50).astype(float)
    envd = smooth_env(active, 0.08, 0.6, hop)
    duck = 10 ** (DUCK_DB * envd / 20)
    duck = np.repeat(duck, h)
    duck = np.concatenate([duck, np.full(n - len(duck), duck[-1])])
    mix = vo + fx + mus * 10 ** (MUSIC_DB / 20) * duck[:, None]

    loud = meter.integrated_loudness(mix)
    mix *= 10 ** ((TARGET_LUFS - loud) / 20)
    mix = limiter(mix, CEILING_DB)
    print("final LUFS", round(meter.integrated_loudness(mix), 2), "peak dBFS", round(20 * np.log10(np.abs(mix).max()), 2))
    for name, bus in (("vo", vo), ("sfx", fx), ("music", mus * 10 ** (MUSIC_DB / 20) * duck[:, None])):
        g = 10 ** ((TARGET_LUFS - loud) / 20)
        print(f"  {name:6s} LUFS {meter.integrated_loudness(bus * g):6.1f}")
    sf.write(os.path.join(BUILD, "mix.wav"), mix[: int(total * SR)].astype(np.float32), SR, subtype="FLOAT")
    if os.environ.get("STEMS"):
        os.makedirs(os.path.join(BUILD, "stems"), exist_ok=True)
        g = 10 ** ((TARGET_LUFS - loud) / 20)
        for name, bus in (("vo", vo), ("sfx", fx), ("music", mus * 10 ** (MUSIC_DB / 20) * duck[:, None])):
            sf.write(os.path.join(BUILD, "stems", f"{name}.wav"), (bus[: int(total * SR)] * g).astype(np.float32), SR)

    # subtitles: split each narration clip into short cues
    phrases = [("twenty seventeen", "2017"), ("five hundred and twelve", "512"),
               ("two thousand and forty-eight", "2,048"), ("sixty-four", "64"), ("twenty-eight point four", "28.4"),
               ("thirty-seven thousand", "37,000"), ("forty-nine", "49"), ("fifty", "50"), ("blue,", "BLEU,"),
               ("Bert", "BERT"), ("W Q,", "W_Q,"), ("W Q", "W_Q"), ("W K", "W_K"), ("W V,", "W_V,"), ("W V.", "W_V."), ("W V", "W_V"),
               ("W O,", "W_O,"), ("W O.", "W_O."), ("d k,", "d_k,"), ("d k.", "d_k."), ("d k", "d_k")]

    def merge(words):
        out, i = [], 0
        while i < len(words):
            for ph, rep in phrases:
                toks = ph.split()
                seg = words[i:i + len(toks)]
                if len(seg) == len(toks) and all(a[0] == b for a, b in zip(seg, toks)):
                    out.append([rep, seg[0][1], seg[-1][2]])
                    i += len(toks)
                    break
            else:
                out.append(words[i])
                i += 1
        return out

    cues = []
    for t0, words in subs:
        words = merge([[re.sub(r"\[([^\]]+)\]\(/[^)]*/\)", r"\1", w), s, e] for w, s, e in words])
        cur, start = [], None
        for w, s, e in words:
            if start is None:
                start = t0 + s
            cur.append(w)
            end = t0 + e
            if len(" ".join(cur)) > 38 or re.search(r"[.?!:;]$", w) or (re.search(r",$", w) and len(cur) > 3):
                cues.append((start, end, " ".join(cur)))
                cur, start = [], None
        if cur:
            cues.append((start, end, " ".join(cur)))
    with open(os.path.join(BUILD, "subtitles.srt"), "w") as f:
        for i, (s, e, text) in enumerate(cues, 1):
            f.write(f"{i}\n{srt_time(s)} --> {srt_time(max(e, s + 0.8))}\n{text}\n\n")
    print("wrote build/mix.wav, build/subtitles.srt,", len(cues), "cues")


if __name__ == "__main__":
    main()
