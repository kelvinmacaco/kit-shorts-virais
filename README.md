# Kit Shorts Virais

Um kit para produzir **YouTube Shorts e TikToks** de 40 a 60 segundos com o **Claude Code**, organizado em **skills**. A partir de um vídeo de referência (ou só um tema), o Claude:

1. pergunta o @ do canal, a voz e o tom;
2. analisa a referência, confere os números e escreve o roteiro e o texto da narração para o ElevenLabs v4;
3. depois que você grava a voz, busca vídeos grátis, anima as cenas em HyperFrames (visual de fita VHS/CRT, legenda palavra por palavra, final em loop), confere, renderiza e entrega o vídeo;
4. escreve títulos, descrição e comentário fixado, e depois analisa os seus números.

O kit guarda **só o conceito de produção**: as regras, a biblioteca, o modelo e tudo o que foi aprendido com 6 Shorts reais e a análise de 20 vídeos, **o que deu certo e o que não deu** (`LESSONS_LEARNED.md`). Não há vídeos, áudios nem o @ de ninguém aqui.

> **O @ do canal é sempre perguntado ao criador** e fica no `kit.json` do projeto, que não vai para o Git. A marca @ fica **logo abaixo da faixa da legenda e nunca a sobrepõe**: a biblioteca calcula a posição a partir da legenda e recusa montar sem um @.

---

## As skills (carregam sozinhas ao abrir o Claude Code nesta pasta)

| Skill | Quando usar |
|---|---|
| **`short-start`** | **Comece por aqui.** Coordena o fluxo inteiro e chama as outras na ordem |
| `short-script` | Referência → roteiro, texto do ElevenLabs, títulos, descrição |
| `short-media` | Vídeos grátis (Pexels/Pixabay), trilha sem Content ID, efeitos e cortes |
| `short-animation` | A peça certa para cada cena (contadores, pavio, alvos, setas, bandeiras, final, loop) |
| `short-build` | Narração → generate.py → VHS → índice com o @ |
| `short-review` | Check, quadros, render, volume, loop, REVIEW |
| `short-publish` | Títulos com 5 #, descrição, comentário fixado, horário |
| `short-analytics` | Prints do YouTube/TikTok Studio → achados → regras novas |
| `short-voice-patch` | Trocar só uma parte da fala e emendar |

**Skills de apoio que o kit usa ao máximo** (instale antes):

| Skill | Para quê | Como instalar |
|---|---|---|
| `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` | Contrato de render, check, snapshot e render, blocos prontos, mídia e tratamentos (VHS) | Plugin **HyperFrames** no gerenciador de plugins do Claude Code |
| `graphify` | Mapa do código do kit, para o Claude achar uma peça sem ler tudo | `pip install graphifyy` e depois `graphify install --project` nesta pasta |

## O que tem aqui

```
kit-shorts-virais/
  README.md            este arquivo
  LESSONS_LEARNED.md      tudo o que foi aprendido: o que deu certo e o que não deu, por área
  RULES.md            as regras obrigatórias de roteiro, visual, áudio e publicação
  RETENTION_GUIDE.md     o que os dados mostraram, o esqueleto de roteiro e as metas
  kit.example.json     modelo do kit.json de cada projeto (@, caminhos, voz, horário)
  .claude/skills/      as 9 skills do kit
  lib/                 lib_short.py (peças de cena), level_voice.py, transcribe.py, measure_phrases.py, vhs*.json
  template/              projeto-modelo: generate.py genérico e comentado, build.ps1, roteiro e narração modelo
  tools/         busca no Pexels, receitas de ffmpeg, de onde vêm os efeitos sonoros
```

## Requisitos

| O quê | Para quê | Observação |
|---|---|---|
| Windows 10/11 | os scripts `.ps1` | os comandos de ffmpeg e Python valem em outros sistemas |
| [Claude Code](https://claude.com/claude-code) | roda as skills | de preferência o app desktop, que tem navegador embutido para buscar vídeos |
| FFmpeg (build "full") | cortar vídeos, emendar áudio, medir volume | o caminho da pasta `bin` vai no `kit.json` |
| Python 3.10+ com `faster-whisper` | transcrição palavra por palavra | ex.: o venv do [OpenMontage](https://github.com/calesthio/OpenMontage) (`tools.analysis.transcriber`); fixe `av<19` |
| Node.js 20+ | HyperFrames | `npx --yes hyperframes@0.8.230 ...` (versão fixada) |
| Conta no ElevenLabs | narração (o criador grava) | modelo Eleven v4 |

## Como usar

1. Clone o repositório e abra o Claude Code **nesta pasta**.
2. Mande o vídeo de referência (ou o tema). A skill `short-start` assume a partir daí.
3. Responda o **@ do canal**, a voz e o tom.
4. Grave no ElevenLabs o texto que ela entregar e mande o mp3.
5. Receba o vídeo pronto, os títulos e a descrição. Poste perto das 22h.
6. Depois de 48 h, mande os prints do YouTube/TikTok para ajustar os próximos.

## Como funciona por dentro

- **`lib_short.py`** gera cada cena como uma sub-composição HyperFrames (HTML + timeline GSAP pausado), além de:
  - legendas palavra por palavra (`write_captions`);
  - textura de fita (`write_textura`);
  - transições (`write_transicoes`);
  - o índice com voz, trilha e efeitos (`write_index`, que **exige** `handle="@..."`).
- **Peças:**
  - texto e movimento: `kline`, `words_js`, `slam`, `punch`, `shake`, `label`;
  - like, compartilhar e loop: `like_block`, `plane_svg`, `osd_rewind`;
  - interação: `step_badge`, `comment_card`, `follow_card`;
  - progresso temático: **`pavio_scene`**.
- **`level_voice.py`** nivela a narração frase por frase. O master fica em cerca de −13,5 LUFS, com pico real abaixo de −2 dBTP.
- **`build.ps1`** (no projeto) lê o `kit.json`, roda o `generate.py` com o @ e aplica a fita VHS (`media-treatment`).

## Licenças e créditos

- **Código e textos:** licença MIT (`LICENSE`).
- **Vídeos:** use só material grátis (licenças do Pexels/Pixabay); os arquivos não vão para o Git.
- **Trilhas:** do Pixabay, **sem "Content ID Registered"**.
- **Efeitos sonoros:** do pacote do HyperFrames (`tools/sfx/README.md`).
- **Fontes:** Archivo Black, Inter e Space Mono (Google Fonts).
- **Nada de imagens do vídeo de referência.**
