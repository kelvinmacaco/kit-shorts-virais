---
name: short-animation
description: Use para desenhar as cenas animadas de um Short no generate.py - escolher a peça certa da lib_short para cada trecho (título do quadro 0, palavras, contadores, alvos, setas, bandeiras SVG, pavio de progresso, revelação com tela que se enche, final calmo ou energético, loop) e garantir uma interação por cena no tom do vídeo.
---

# Animação das cenas

Apoio: a skill **`hyperframes`** (contrato de render, timelines, regras de clip), **`hyperframes-registry`** (procure um bloco pronto antes de desenhar à mão, ex.: glitch, CRT, gráficos) e **`graphify`**, para achar uma peça na `lib` (`graphify explain "pavio_scene"`).

Parta do `template/build/generate.py`, que já tem uma cena de exemplo para cada parte do roteiro.

## Peça certa para cada trecho

| Trecho | Peça | Observação |
|---|---|---|
| Quadro 0 / gancho | `hook_html` + `shake` + `drift` | O mesmo título volta no loop |
| Frase falada | `kline` + `words_js`; `slam` na palavra-chave | Uma linha por trecho de 2–4 palavras |
| Mistério | Luzes que acendem, `slam` em "PIOR"/"DATA" | Calendário que gira ("20??") |
| Números | `counter(...)` + escala de impacto + `shake` | Formato pt-BR (`toLocaleString`) |
| Lugar ou alvo | Anéis `ping` pulsando | Com uma data ou fonte em `mono` |
| Conflito | Setas que se chocam + flash `hit` | Lado A × lado B |
| Lados ou países | Bandeiras SVG + linhas que se desenham (`pathLength="1"`) + pontos viajando com etiquetas | Sem brasões |
| Progresso da lista | **`pavio_scene`**, um pavio que queima a cada item e explode no clímax | No lugar de "1/3"; `step_badge` só em último caso |
| Estrago, escala | Tela que se enche de pontos (`clip-path`) + contador gigante | Fonte do dado em `mono` |
| Janela de TV | `tvv` + `enter_tv` | Para clipes deitados |
| Final **pesado** | Pergunta suave, coração que enche devagar, `follow_card` escuro, fade até o preto | Sem pop, sparkle, flash nem corte |
| Final **leve** | `like_block` + `plane_svg` + `follow_card` | Pode ter pop e brilho |
| Loop | Clipe invertido do gancho terminando no quadro 0 + o mesmo título | Do preto (pesado) ou com `osd_rewind` (leve) |

## Regras
- **Algo muda a cada 1,5–2,5 s** e cada cena tem uma interação.
- **Tempos:** locais dentro de `scene()` e globais em `SCENES`, cortes, efeitos e legendas.
- **Área segura:** texto em x 90–900 e y 170–1330. Linha longa: reduza a fonte (Archivo Black ocupa ~0,75 em por letra).
- **Marca @:** a lib põe abaixo da legenda (`WM_TOP`); não desenhe outra.
- **Regras de clip:**
  - não anime visibility/opacity do próprio clip;
  - use `immediateRender:false` em fromTo posteriores;
  - `repeat` com `yoyo` para efeitos contínuos (faísca, pulso);
  - nada aleatório (o grão usa semente).
- **Tom:** em vídeo pesado, um pulso vermelho de no máximo 0,32 de opacidade; num vídeo leve, cores mais vivas.
