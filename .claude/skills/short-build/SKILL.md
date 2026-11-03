---
name: short-build
description: Use quando o criador mandar o mp3 da narração de um Short já roteirizado. Transcreve e nivela a voz, busca vídeos grátis (Pexels) e trilha (Pixabay sem Content ID), corta os clipes, escreve o generate.py das cenas com lib_short, aplica a fita VHS, confere quadros, renderiza com HyperFrames e entrega o vídeo na Área de Trabalho.
---

# Montagem de um Short

Faz parte do fluxo `short-start`. Detalhes de mídia na `short-media`, de animação na `short-animation` e de conferência e render na `short-review`. Apoio: `hyperframes`, `hyperframes-cli` e `media-use`.

Leia antes `RULES.md` e o `ROTEIRO.md` do projeto. O `kit.json` do projeto **precisa** ter o `handle` (o @ escolhido pelo criador). Se estiver vazio ou for "@SEU_CANAL", **pergunte ao criador** antes de continuar.

## 1. Narração
- Copie o mp3 para `assets\audio\narracao_raw.mp3`.
- Procure pausas longas com `silencedetect=n=-40dB:d=0.6`. Encurte as que caírem no gancho e, se o tom for energético, as maiores que 0,8 s. Use a receita de emenda em `tools\ffmpeg_recipes.md`.
- Transcreva com `build\transcribe.py`, gerando `assets\audio\narracao_words.json` com o tempo de cada palavra.
- Nivele: `python -I -X utf8 build\level_voice.py <mp3> <words.json> video\assets\audio\narracao.mp3`.
- Copie `hyperframes.json`, `package.json`, `meta.json`, `AGENTS.md` e `CLAUDE.md` de `template\video\` para `video\`. Ajuste o `id` do `meta.json`.

## 2. Mídia
- Rode `tools\pexels_search.js` no navegador embutido, numa página do pexels.com, com várias buscas de uma vez.
- Baixe as miniaturas, monte uma folha (ffmpeg `tile`) e **olhe antes de escolher**.
- Descarte logos, marcas, camisas de time e o que não combina com a fala.
- Baixe com `curl -L -A "Mozilla/5.0" -e https://www.pexels.com/` para `assets\video\stock\`.
- Trilha: do Pixabay, só faixas **sem "Content ID Registered"**, em `video\assets\audio\musica.mp3`.
- Efeitos sonoros: veja `tools\sfx\README.md`; ficam em `video\assets\sfx\`.
- Corte os clipes com as receitas (vertical 1080×1920 ou janela de TV 1000×750) em `video\assets\video\`. Faça o clipe invertido do gancho para o loop.
- **Não chame uma função de shell de `cut`**, porque isso esconde o comando `cut` do sistema.

## 3. Cenas (`build\generate.py`)
- Parta do `template\build\generate.py`, que é comentado. Use `SCENES = [(nome, início, fim)]` com os tempos das palavras; dentro de cada cena os tempos são **locais** (0 = início da cena).
- Use as peças do `lib_short`:
  - texto: `kline`/`words_js`/`slam`/`punch`/`shake`/`label`;
  - números: contadores com `onUpdate`;
  - like e compartilhar: `like_block`/`plane_svg`;
  - interação: `comment_card`/`follow_card`/`step_badge`.
- **Animação em toda cena.** Se a lista pedir progresso, faça um indicador temático como cena sobreposta (ex.: `pavio_scene` da biblioteca, um pavio que queima a cada item e explode no clímax).
- **Legendas:** `write_captions(WORDS, TOTAL, SKIP, alt_from, alt_top)`. O `SKIP` cobre os trechos em que a tipografia da cena já mostra a fala.
- **Índice:** `write_index(TOTAL, SCENES, SFX, dur_voz, 0.1, handle=HANDLE)`. O `HANDLE` vem do `kit.json`, via `build.ps1`.
- **A marca @ fica abaixo da legenda** (`WM_TOP`). Não posicione a marca à mão.
- **Loop:** a última cena termina com o clipe invertido no quadro 0 do gancho e o mesmo título.
- **O final segue o tom do vídeo:** num vídeo pesado, escuro e lento, sem estouros.
- **Regras do HyperFrames:**
  - `class="clip"` + `data-start`/`data-duration`;
  - não anime visibility ou opacity do próprio clip, só de um elemento interno;
  - use `immediateRender:false` em fromTo posteriores;
  - cada `<audio>` tem id e track próprios;
  - vídeos sempre `muted`;
  - linhas SVG com `pathLength="1"` para o efeito de desenhar.

## 4. Gerar, conferir e renderizar
- Ajuste `$alvos` no `build\build.ps1`: as cenas com filmagem, `.fv` (tela cheia) e `.tv` (janela de TV).
- Rode `powershell -ExecutionPolicy Bypass -File build\build.ps1 -Duracao <TOTAL>`. **Nunca** passe a saída por `Select-Object -First`.
- `npx --yes hyperframes@<versão> check --json`: corrija os erros. São esperados, e podem ficar:
  - contraste da marca translúcida;
  - título do loop curto.
- Tire snapshots (`snapshot -o <pasta> --no-end --at "..."`) e olhe as folhas de contato. Procure:
  - texto saindo da tela;
  - legenda ilegível;
  - elementos encobertos;
  - cena parada.
- Renderize com `render --quality standard -o renders\<nome>_master.mp4` e meça com `ebur128=peak=true` (meta: cerca de −13,5 LUFS, pico abaixo de −2 dBTP).
- Copie para a Área de Trabalho com x264 CRF 19, AAC 192k e `+faststart`.
- Confira o loop: o quadro 0 e o último lado a lado (`hstack`) devem ser iguais.
- Escreva `video\REVIEW.md` com as decisões, o que foi medido e o que foi só olhado ("ninguém ouviu o som").

## 5. Entrega
Envie o vídeo, os títulos (TikTok e YouTube, com 5 # cada), a descrição e o comentário para fixar. Lembre o horário de postagem e peça os prints de 48 h.
