import json
import math
import subprocess
import sys

FF = r"C:\Claude\Video\tools\ffmpeg\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
audio, words_json = sys.argv[1], sys.argv[2]
segs = json.load(open(words_json, encoding="utf-8"))["segments"]

# PCM mono 16 kHz em memória
raw = subprocess.run([FF, "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
n = len(raw) // 2
import struct
samples = struct.unpack(f"<{n}h", raw)

for s in segs:
    a, b = int(s["start"] * 16000), int(s["end"] * 16000)
    chunk = samples[a:b]
    if not chunk:
        continue
    rms = math.sqrt(sum(x * x for x in chunk) / len(chunk)) / 32768
    db = 20 * math.log10(rms + 1e-9)
    print(f"{s['start']:6.2f}-{s['end']:6.2f}  {db:6.1f} dB  {s['text'].strip()[:60]}")
