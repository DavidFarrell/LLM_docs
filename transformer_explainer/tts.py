"""Generate the voiceover with Kokoro-82M (local, no API keys).

Writes one WAV per beat plus build/vo/manifest.json holding each beat's
duration, bookmark times and per-word timings (from Kokoro's duration head).
Usage: python tts.py [--only SCENE] [--speed 1.05]
"""
import argparse
import difflib
import json
import os
import re

import numpy as np
import soundfile as sf

from script import SCRIPT

SR = 24000
BUILD = os.environ.get("BUILD_DIR", os.path.join(os.path.dirname(__file__), "build"))
VO_DIR = os.path.join(BUILD, "vo")
MARK = re.compile(r"\{(\w+)\}")
OVERRIDE = re.compile(r"\[([^\]]+)\]\(/[^)]*/\)")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def parse(text):
    """Return (tts_text, words, marks) where marks maps name -> word index."""
    marks = {}
    words = []
    for piece in re.split(r"(\{\w+\})", text):
        m = MARK.fullmatch(piece)
        if m:
            marks[m.group(1)] = len(words)
            continue
        plain = OVERRIDE.sub(r"\1", piece)
        words.extend(plain.split())
    tts_text = MARK.sub("", text)
    tts_text = re.sub(r"\s+", " ", tts_text).strip()
    return tts_text, words, marks


def synth(pipe, text, voice, speed):
    audio, toks, offset = [], [], 0.0
    for r in pipe(text, voice=voice, speed=speed, split_pattern=None):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        for t in r.tokens or []:
            s = None if t.start_ts is None else t.start_ts + offset
            e = None if t.end_ts is None else t.end_ts + offset
            toks.append([t.text, s, e])
        audio.append(a)
        offset += len(a) / SR
    return np.concatenate(audio), toks


def fill_times(toks):
    """Interpolate missing timestamps."""
    n = len(toks)
    for i in range(n):
        for j in (1, 2):
            if toks[i][j] is None:
                prev = next((toks[k][2] for k in range(i - 1, -1, -1) if toks[k][2] is not None), 0.0)
                toks[i][j] = prev
    return toks


def align(words, toks):
    """Map each script word to (start, end) using char-level alignment."""
    a_chars, a_owner = [], []
    for wi, w in enumerate(words):
        for c in norm(w):
            a_chars.append(c)
            a_owner.append(wi)
    b_chars, b_owner = [], []
    for ti, t in enumerate(toks):
        for c in norm(t[0]):
            b_chars.append(c)
            b_owner.append(ti)
    A, B = "".join(a_chars), "".join(b_chars)
    a2b = {}
    if A == B:
        a2b = {i: i for i in range(len(A))}
    else:
        sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
        for blk in sm.get_matching_blocks():
            for k in range(blk.size):
                a2b[blk.a + k] = blk.b + k
    times = []
    for wi, w in enumerate(words):
        idx = [i for i, o in enumerate(a_owner) if o == wi]
        mapped = [a2b[i] for i in idx if i in a2b]
        if not mapped:
            times.append(None)
            continue
        first, last = mapped[0], mapped[-1]
        t0, t1 = toks[b_owner[first]], toks[b_owner[last]]
        # position of char inside its token for sub-token interpolation
        def at(bpos, tok_i, edge):
            chars = [i for i, o in enumerate(b_owner) if o == tok_i]
            frac = (bpos - chars[0] + (1 if edge == "end" else 0)) / max(len(chars), 1)
            s, e = toks[tok_i][1], toks[tok_i][2]
            return s + frac * (e - s)
        times.append([at(first, b_owner[first], "start"), at(last, b_owner[last], "end")])
    # fill gaps
    for i in range(len(times)):
        if times[i] is None:
            prev = next((times[k][1] for k in range(i - 1, -1, -1) if times[k]), 0.0)
            times[i] = [prev, prev]
    return times


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--voice", default="af_heart")
    ap.add_argument("--speed", type=float, default=1.05)
    args = ap.parse_args()

    from kokoro import KPipeline
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    os.makedirs(VO_DIR, exist_ok=True)
    man_path = os.path.join(VO_DIR, "manifest.json")
    manifest = json.load(open(man_path)) if os.path.exists(man_path) else {}

    for scene, beats in SCRIPT.items():
        if args.only and scene != args.only:
            continue
        manifest[scene] = {}
        for key, text in beats:
            tts_text, words, marks = parse(text)
            audio, toks = synth(pipe, tts_text, args.voice, args.speed)
            toks = fill_times(toks)
            wt = align(words, toks)
            # trim trailing silence to a fixed tail
            last = max(e for _, e in wt) if wt else len(audio) / SR
            end = min(len(audio), int((last + 0.12) * SR))
            audio = audio[:end]
            fade = int(0.03 * SR)
            audio[-fade:] *= np.linspace(1, 0, fade)
            path = os.path.join(VO_DIR, f"{scene}_{key}.wav")
            sf.write(path, audio.astype(np.float32), SR)
            manifest[scene][key] = {
                "file": path,
                "dur": len(audio) / SR,
                "marks": {m: round(wt[i][0], 3) if i < len(wt) else round(len(audio) / SR, 3)
                          for m, i in marks.items()},
                "words": [[w, round(s, 3), round(e, 3)] for w, (s, e) in zip(words, wt)],
                "text": tts_text,
            }
            print(f"{scene}/{key}: {len(audio)/SR:6.2f}s  marks={manifest[scene][key]['marks']}")
    json.dump(manifest, open(man_path, "w"), indent=1)
    total = sum(b["dur"] for s in manifest.values() for b in s.values())
    print(f"TOTAL VO: {total:.1f}s ({total/60:.2f} min)")


if __name__ == "__main__":
    main()
