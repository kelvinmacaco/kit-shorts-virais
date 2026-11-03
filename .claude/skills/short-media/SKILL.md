---
name: short-media
description: Use para buscar, escolher, baixar e preparar a mídia grátis de um Short - vídeos do Pexels/Pixabay, trilha do Pixabay sem Content ID e efeitos sonoros - e cortar os clipes no formato vertical (1080×1920) ou de janela de TV (1000×750), incluindo o clipe invertido do loop.
---

# Mídia grátis para o Short

Apoio: a skill **`media-use`** do HyperFrames (mídia, efeitos, tratamentos) e o **navegador embutido** do app.

1. **Monte a lista de cenas** a partir do `ROTEIRO.md`: para cada trecho, o que precisa aparecer e por quanto tempo (some ~0,2 s de folga).
2. **Busque no Pexels** com `tools/pexels_search.js`, várias buscas de uma vez, em inglês:
   - abra uma página do pexels.com no navegador embutido e rode o trecho pelo console ou pelo javascript_tool;
   - pegue `id`, título, duração, tamanho, miniatura e link.
3. **Olhe antes de escolher.** Baixe as miniaturas, monte uma folha com o `tile` do ffmpeg e veja. Descarte:
   - logos, marcas, camisas de time, rostos de pessoas famosas;
   - o que não combina com a fala (ex.: carro quando a fala é sobre moto);
   - cenas de filme ou com direitos autorais.
4. **Baixe a melhor versão:**
   - vertical: arquivo de 1080–1440 de largura;
   - deitado: 2560 ou 1920, para cortar o meio sem perder qualidade;
   - comando: `curl -L -A "Mozilla/5.0" -e https://www.pexels.com/`, salvando em `assets/video/stock/`.
5. **Revise cada clipe numa faixa de quadros** (`fps=5/<dur>,tile=5x1`) e escolha o trecho bom (início e duração).
6. **Corte** com as receitas de `tools/ffmpeg_recipes.md`:
   - `FV` para tela cheia, `TV` para janela;
   - `,reverse` para o clipe invertido do gancho (loop) e para os clipes rebobinados;
   - salve em `video/assets/video/`;
   - não chame a função de shell de `cut`.
7. **Trilha:** no Pixabay, só faixas **sem "Content ID Registered"**, com o clima do tom escolhido. Salve em `video/assets/audio/musica.mp3`.
8. **Efeitos sonoros:** os nomes e a origem estão em `tools/sfx/README.md`. Vão em `video/assets/sfx/`.
9. **Sem boa filmagem** (ex.: bandeiras, gráficos), desenhe na animação: SVG simples, sem brasões (skill `short-animation`).
10. Anote no `REVIEW.md` o que foi usado e o que foi descartado, com o motivo.
