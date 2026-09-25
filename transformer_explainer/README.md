# "Attention Is All You Need", explained

A ~15 minute motion-graphics explainer of Vaswani et al. (2017), built entirely
from code with no API keys: the animation is [Manim](https://www.manim.community/),
the narration is the open-weight [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
text-to-speech model running locally on CPU, and every sound effect and the music bed
are synthesised with NumPy/SciPy.

The video focuses on two things that often stay fuzzy:

1. **Why "query", "key" and "value"?** It builds up from a plain dictionary lookup,
   to a soft (differentiable) lookup, to self-attention on a real sentence, to why
   the three learned projections are needed at all.
2. **How attention plugs into the network**: residual stream, layer norm, the
   position-wise feed-forward network, stacking, the decoder (masking and
   cross-attention) and training.

## Chapters

| # | Scene file | Topic |
|---|------------|-------|
| – | `s01_coldopen.py` | The "it" problem, the paper, the two goals |
| 01 | `s02_recurrence.py` | Why recurrence was a bottleneck |
| 02 | `s03_vectors.py` | Tokens as vectors, the dot product |
| 03 | `s04_lookup.py` | Query, key, value as a soft dictionary lookup |
| 04 | `s05_selfattention.py` | Self-attention worked through on one sentence |
| 05 | `s06_whythree.py` | Why three separate projections |
| 06 | `s07_matrix.py` | The matrix form, equation (1), why divide by √dₖ |
| 07 | `s08_multihead.py` | Multi-head attention and the paper's Figure 4 |
| 08 | `s09_position.py` | Positional encoding |
| 09 | `s10_encoder.py` | Residuals, layer norm, feed-forward, stacking, training |
| 10 | `s11_decoder.py` | Masked attention, cross-attention, output, Figure 1 |
| 11 | `s12_legacy.py` | Results (Table 2) and legacy |
| 12 | `s13_recap.py` | Recap and credits |

## Pipeline

```
script.py        narration, with {bookmarks} for syncing animation to words
tts.py           Kokoro TTS -> build/vo/*.wav + word timings (manifest.json)
common.py        design system (palette, chips, vectors, heatmaps) + timing helpers
scenes/*.py      one Manim scene per chapter; each logs its audio cues while rendering
sfx.py           procedural sound effects -> build/sfx/*.wav
music.py         procedural ambient bed (D major pads, sub, plucked arpeggio)
mix.py           places narration + cues at their logged frame times, ducks music,
                 normalises to -16 LUFS, writes subtitles
particles.py     subtle drifting dust layer, screen-blended in post
assemble.sh      concat scenes, blend, mux audio + soft subtitles + chapters -> output/*.mp4
share_encode.sh  smaller 720p copy for upload limits
```

Audio sync is frame-accurate: every narration clip and sound cue is logged with
Manim's own renderer clock during rendering, so the mixer places it exactly where
the corresponding frames landed.

## Rebuilding

Requirements: Python 3.11, ffmpeg, a LaTeX install (for `MathTex`), Cairo/Pango,
espeak-ng, the Inter and JetBrains Mono fonts.

```bash
python -m venv /opt/venv
/opt/venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
/opt/venv/bin/pip install "kokoro>=0.9.4" manim soundfile scipy pyloudnorm matplotlib faster-whisper

python prep_assets.py path/to/1706.03762v7.pdf   # crops the paper's figures
/opt/venv/bin/python tts.py --speed 1.05          # narration
/opt/venv/bin/python sfx.py                       # sound effects
./render_all.sh h 4                               # 1080p60 scenes, 4 in parallel
./assemble.sh                                     # 1080p60 master in output/ (~140 MB)
./share_encode.sh                                 # two-pass 720p30 copy under 30 MiB for sharing
```

The master is 1080p60 (H.264, AAC, -16 LUFS integrated, -1 dBTP) with 13 chapter
markers and a soft English subtitle track; the same subtitles are written alongside as `.srt`.

## Credits

Based on Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser & Polosukhin,
*Attention Is All You Need*, NIPS 2017, [arXiv:1706.03762](https://arxiv.org/abs/1706.03762).
Figures from the paper are reproduced with attribution under Google's stated permission
for journalistic or scholarly use. The feed-forward "key-value memory" view is from
Geva et al., *Transformer Feed-Forward Layers Are Key-Value Memories* (EMNLP 2021).
