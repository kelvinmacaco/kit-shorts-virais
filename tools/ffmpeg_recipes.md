# Receitas de ffmpeg usadas no kit

Coloque a pasta `bin` do ffmpeg no PATH (está no `kit.json`). Nos exemplos, `$S` é a pasta dos vídeos baixados e `$O` é `video/assets/video`.

```bash
FV="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"   # tela cheia vertical
TV="scale=1000:750:force_original_aspect_ratio=increase,crop=1000:750,fps=30,setsar=1"     # janela de TV 4:3
ENC="-an -c:v libx264 -profile:v high -crf 18 -pix_fmt yuv420p"
corta() { ffmpeg -hide_banner -loglevel error -y -ss $2 -t $3 -i $S/$1 -vf "$4" $ENC $O/$5; }   # não chame de "cut"!
corta 01-terra.mp4 0 4.4 "$FV" gancho.mp4
corta 01-terra.mp4 0 1.0 "$FV,reverse" gancho_volta.mp4             # clipe invertido para o loop
corta 04-tanque.mp4 1.0 2.6 "crop=810:1440:875:0,$FV" tanque.mp4    # vídeo deitado: corta o meio
```

**Folha de miniaturas de um clipe** (para escolher o trecho):
```bash
ffmpeg -i clipe.mp4 -vf "fps=5/<duração>,scale=-2:170,tile=5x1" -frames:v 1 linha.png
```

**Pausas da narração:**
```bash
ffmpeg -i narracao.mp3 -af silencedetect=n=-40dB:d=0.6 -f null - 2>&1 | grep silence_
```

**Encurtar uma pausa** (corta de 3,85 a 4,32 s, dentro do silêncio):
```bash
ffmpeg -i raw.mp3 -filter_complex "[0]atrim=0:3.85,asetpts=PTS-STARTPTS,afade=t=out:st=3.83:d=0.02[a];[0]atrim=start=4.32,asetpts=PTS-STARTPTS,afade=t=in:d=0.02[b];[a][b]concat=n=2:v=0:a=1" -c:a libmp3lame -b:a 192k cortada.mp3
```

**Reordenar trechos** (ex.: levar uma pergunta para o fim):
```bash
ffmpeg -i raw.mp3 -filter_complex "[0]atrim=0:A,asetpts=PTS-STARTPTS[p1];[0]atrim=B:C,asetpts=PTS-STARTPTS[p2];anullsrc=r=44100:cl=mono,atrim=0:0.35[s];[0]atrim=A:B,asetpts=PTS-STARTPTS[q];[0]atrim=start=C,asetpts=PTS-STARTPTS[p3];[p1][p2][s][q][p3]concat=n=5:v=0:a=1" nova.mp3
```

**Volume do master** (meta: cerca de −13,5 LUFS, pico real abaixo de −2 dBTP):
```bash
ffmpeg -i master.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary
```

**Cópia final** (Área de Trabalho):
```bash
ffmpeg -i master.mp4 -c:v libx264 -crf 19 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "<Desktop>/TITULO - Short.mp4"
```

**Conferir o loop** (o primeiro e o último quadro devem ser iguais):
```bash
ffmpeg -i final.mp4 -vf "select='eq(n\,0)',scale=300:-1" -frames:v 1 a.png
ffmpeg -sseof -0.05 -i final.mp4 -vf scale=300:-1 -update 1 -frames:v 1 b.png
ffmpeg -i a.png -i b.png -filter_complex hstack loop.png
```
