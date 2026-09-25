"""Subtle drifting 'dust' layer, screen-blended over the final video in post.

python particles.py <seconds>  -> build/particles.mp4 (960x540, 30 fps, black background)
"""
import os
import subprocess
import sys

import numpy as np

W, H, FPS = 960, 540, 30
ROOT = os.path.dirname(os.path.abspath(__file__))


def sprite(r):
    s = int(np.ceil(r * 3))
    y, x = np.mgrid[-s:s + 1, -s:s + 1]
    g = np.exp(-(x ** 2 + y ** 2) / (2 * r ** 2))
    return g.astype(np.float32)


def main(total):
    rng = np.random.default_rng(42)
    n = 64
    depth = rng.uniform(0, 1, n)                     # 0 near (big, blurry), 1 far (small, sharp)
    radius = 0.9 + 3.6 * (1 - depth) ** 1.6
    alpha = 0.05 + 0.22 * depth ** 0.7 * rng.uniform(0.5, 1.0, n)
    speed = 3 + 9 * (1 - depth)                      # px/s at 960x540
    ang = rng.normal(-np.pi / 2 + 0.25, 0.25, n)      # mostly upward drift
    vx, vy = np.cos(ang) * speed, np.sin(ang) * speed
    px, py = rng.uniform(0, W, n), rng.uniform(0, H, n)
    tw_f = rng.uniform(0.05, 0.25, n)
    tw_p = rng.uniform(0, 2 * np.pi, n)
    cols = np.array([[0.75, 0.82, 1.0], [0.62, 0.7, 1.0], [1.0, 0.85, 0.55]], np.float32)
    col = cols[rng.choice(3, n, p=[0.55, 0.3, 0.15])]
    sprites = [sprite(r) for r in radius]
    out = os.path.join(ROOT, "build", "particles.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv444p", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = int(total * FPS) + 1
    pad = 20
    for f in range(frames):
        t = f / FPS
        img = np.zeros((H + 2 * pad, W + 2 * pad, 3), np.float32)
        x = (px + vx * t) % (W + 2 * pad)
        y = (py + vy * t) % (H + 2 * pad)
        a = alpha * (0.65 + 0.35 * np.sin(2 * np.pi * tw_f * t + tw_p))
        fade_in = min(1.0, t / 4.0)
        for i in range(n):
            sp = sprites[i]
            s = sp.shape[0] // 2
            xi, yi = int(x[i]), int(y[i])
            x0, x1 = xi - s, xi + s + 1
            y0, y1 = yi - s, yi + s + 1
            if x0 < 0 or y0 < 0 or x1 > img.shape[1] or y1 > img.shape[0]:
                continue
            img[y0:y1, x0:x1] += sp[..., None] * (a[i] * fade_in) * col[i]
        frame = np.clip(img[pad:pad + H, pad:pad + W] * 255, 0, 255).astype(np.uint8)
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()
    print("wrote", out, frames, "frames")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 60)
