---
name: short-voice-patch
description: Use quando o criador quiser mudar só uma parte da fala de um Short já narrado (gancho novo, final novo, tirar uma frase). Pede só as partes novas com os mesmos ajustes de voz, emenda no silêncio com ffmpeg, re-transcreve e desloca os tempos das cenas.
---

# Trocar só um trecho da narração

1. **Escreva só as partes novas**, com as mesmas marcações de emoção. Peça ao criador para gravar **com exatamente os mesmos ajustes de voz** da gravação original. O nome do arquivo do ElevenLabs costuma trazê-los, ex.: `..._s50_sb75_v4` = Stability 50, Similarity 75.
2. **Transcreva o arquivo novo**, que pode trazer várias partes juntas, e ache os limites com `silencedetect=n=-40dB:d=0.15`.
3. **Tirar uma frase:** corte dentro dos silêncios antes e depois dela:
   `atrim=0:A,asetpts=PTS-STARTPTS[a];atrim=start=B,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=0.03`.
4. **Inserir ou trocar trechos:** concatene os pedaços com `atrim` + `anullsrc` (pausas de 0,3–0,4 s) + `concat`, com fades de 20 ms nas bordas. Corte sempre dentro de um silêncio.
5. **Re-transcreva o áudio emendado** para gerar o novo `narracao_words.json` e nivele de novo (`level_voice.py`).
6. **Desloque os tempos no `generate.py`:**
   - se tudo depois do trecho novo andou D segundos, mantenha os tempos antigos e some D (ex.: um gancho novo de 4,6 s, então `D = 4.62`);
   - legendas, cortes e efeitos usam tempo global, então também levam + D.
7. **Refaça a cena do trecho novo** (ex.: um gancho novo pede um quadro 0 novo) e o final do loop.
8. Gere, confira, renderize e entregue como na skill `short-build`.
