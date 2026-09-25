"""Rasterise the paper (arXiv:1706.03762v7) and crop the figures used in the video.
Google grants permission to reproduce the paper's tables and figures, with
attribution, for journalistic or scholarly works (see the paper's first page)."""
import os, subprocess, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "paper")
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "build", "attention.pdf")
os.makedirs(OUT, exist_ok=True)
tmp = os.path.join(HERE, "build", "pages")
os.makedirs(tmp, exist_ok=True)
for page in (1, 3, 4, 14):
    subprocess.run(["pdftoppm", "-r", "300", "-f", str(page), "-l", str(page), "-png", PDF,
                    os.path.join(tmp, f"p{page}")], check=True)

def load(page):
    f = [x for x in os.listdir(tmp) if x.startswith(f"p{page}-")][0]
    return Image.open(os.path.join(tmp, f)).convert("RGB")

def autocrop(img, box, margin=30):
    reg = img.crop(box)
    a = np.asarray(reg).astype(int)
    mask = (a < 235).any(axis=2)
    ys, xs = np.where(mask)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    return reg.crop((max(x0 - margin, 0), max(y0 - margin, 0), min(x1 + margin, reg.width), min(y1 + margin, reg.height)))

p1 = load(1); W, H = p1.size
p1.save(os.path.join(OUT, "page1.png"))
p3 = load(3); W, H = p3.size
autocrop(p3, (0, int(0.06 * H), W, int(0.503 * H))).save(os.path.join(OUT, "fig1.png"))
p4 = load(4); W, H = p4.size
autocrop(p4, (0, int(0.06 * H), W, int(0.29 * H))).save(os.path.join(OUT, "fig2.png"))
p14 = load(14); W, H = p14.size
bottom = autocrop(p14, (int(0.17 * W), int(0.447 * H), int(0.84 * W), int(0.772 * H)))
rb = bottom.rotate(-90, expand=True)
rb.crop((0, 0, rb.width - 26, rb.height)).save(os.path.join(OUT, "fig4_its.png"))
top = autocrop(p14, (int(0.17 * W), int(0.20 * H), int(0.84 * W), int(0.445 * H)))
top.rotate(-90, expand=True).save(os.path.join(OUT, "fig4_full.png"))
for f in sorted(os.listdir(OUT)):
    print(f, Image.open(os.path.join(OUT, f)).size)
