"""Contact sheet of frames: python qa_sheet.py video.mp4 out.png [times...|--every S] [--cols N]"""
import subprocess, sys, os, json
from PIL import Image, ImageDraw, ImageFont
args = sys.argv[1:]
video, out = args[0], args[1]
cols = 4
if "--cols" in args:
    cols = int(args[args.index("--cols") + 1])
dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", video],
                                      capture_output=True, text=True).stdout)["format"]["duration"])
if "--every" in args:
    step = float(args[args.index("--every") + 1])
    times = [t * step + step / 2 for t in range(int(dur // step))]
else:
    times = [float(t) for t in args[2:] if not t.startswith("--") and t.replace('.', '', 1).isdigit()]
frames = []
for t in times:
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-f", "image2pipe",
                        "-vcodec", "png", "-"], capture_output=True)
    if p.stdout:
        import io
        frames.append((t, Image.open(io.BytesIO(p.stdout)).convert("RGB")))
w = 480
h = int(frames[0][1].height * w / frames[0][1].width)
rows = (len(frames) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * (h + 18)), (40, 40, 40))
d = ImageDraw.Draw(sheet)
for k, (t, im) in enumerate(frames):
    x, y = (k % cols) * w, (k // cols) * (h + 18)
    sheet.paste(im.resize((w, h), Image.LANCZOS), (x, y + 18))
    d.text((x + 4, y + 2), f"{t:.1f}s", fill=(255, 220, 120))
sheet.save(out)
print(out, len(frames), "frames, duration", dur)
