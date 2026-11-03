"""Nivela a narração frase por frase (ganho por trecho + limitador).

Uso: python level_voice.py <entrada.mp3> <narracao_words.json> <saida.mp3>
"""
import json
import math
import struct
import subprocess
import sys

FF = r"C:\Claude\Video\tools\ffmpeg\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
ALVO_DB = -18.5      # nível de fala de referência no arquivo original
MAX_SOBE, MAX_DESCE = 7.0, -3.0
GANHO_BASE = 1.5     # +3,5 dB no final, fala normal perto de -15 dB

entrada, words_json, saida = sys.argv[1], sys.argv[2], sys.argv[3]
segs = json.load(open(words_json, encoding="utf-8"))["segments"]

raw = subprocess.run([FF, "-v", "error", "-i", entrada, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
amostras = struct.unpack(f"<{len(raw) // 2}h", raw)


def nivel(a, b):
    trecho = amostras[int(a * 16000):int(b * 16000)]
    rms = math.sqrt(sum(x * x for x in trecho) / max(1, len(trecho))) / 32768
    return 20 * math.log10(rms + 1e-9)


# fronteiras no meio dos silêncios entre frases
trechos = []
for i, s in enumerate(segs):
    ini = 0.0 if i == 0 else (segs[i - 1]["end"] + s["start"]) / 2
    fim = 999.0 if i == len(segs) - 1 else (s["end"] + segs[i + 1]["start"]) / 2
    db = nivel(s["start"], s["end"])
    ganho = max(MAX_DESCE, min(MAX_SOBE, ALVO_DB - db))
    trechos.append((ini, fim, 10 ** (ganho / 20)))
    print(f"{s['start']:6.2f}-{s['end']:6.2f} {db:6.1f} dB -> {ganho:+.1f} dB  {s['text'].strip()[:50]}")

expr = "1"
for ini, fim, g in reversed(trechos):
    expr = f"if(between(t,{ini:.3f},{fim:.3f}),{g:.3f},{expr})"
filtro = f"volume='{GANHO_BASE}*{expr}':eval=frame,alimiter=limit=0.84:attack=2:release=40:level=disabled"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", entrada, "-af", filtro, "-ar", "44100", "-b:a", "192k", saida], check=True)
print("ok:", saida)
