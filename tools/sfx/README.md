# Efeitos sonoros

O kit usa estes arquivos em `video/assets/sfx/`, com os nomes exatos que o `SFX_DUR` do `lib_short.py` espera:

| Arquivo | Uso |
|---|---|
| `pop.mp3` | palavra que entra, rótulo, número |
| `whoosh.mp3` | corte de cena |
| `whoosh-short.mp3` | corte rápido |
| `impact-bass-1.mp3` | os 3 ou 4 momentos fortes |
| `glitch-1.mp3`, `glitch-3.mp3` | falha de fita, tremida |
| `riser.mp3` | subida antes do clímax (comece cerca de 10 s antes) |
| `sparkle.mp3` | brilho (like, faísca) |
| `rewind.mp3` | rebobinar (o `whoosh-cinematic` invertido: `ffmpeg -i whoosh-cinematic.mp3 -af areverse rewind.mp3`) |

Eles vêm do pacote de sons do HyperFrames (skill `media-use` do plugin HyperFrames). Não são versionados aqui: copie do pacote ou de um projeto anterior. Em vídeos de final calmo, não use pop, sparkle nem rewind no final.
