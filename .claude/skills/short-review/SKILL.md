---
name: short-review
description: Use depois de gerar as cenas de um Short para conferir e entregar - hyperframes check, snapshots e folhas de contato com checklist, correções, render, medição de volume (LUFS e pico real), cópia final para a Área de Trabalho, conferência do loop e REVIEW.md honesto.
---

# Revisão, render e entrega

Apoio: a skill **`hyperframes-cli`** (check, snapshot, render: leia a saída em JSON).

1. **Check:** `npx --yes hyperframes@<versão> check --json`. Corrija todo erro de lint, runtime e layout. Avisos que podem ficar (anote no REVIEW):
   - contraste da marca translúcida;
   - título curto no loop (é o mesmo do quadro 0);
   - rótulo do pavio coberto pela faísca por um instante;
   - `nested_media_start_basis_ambiguous`.
2. **Quadros:** `snapshot -o <pasta> --no-end --at "..."` com 1 ou 2 momentos por cena, mais o quadro 0 e o último. Leia as folhas de contato e confira este checklist:
   - [ ] texto saindo da tela, ou uma linha longa demais;
   - [ ] texto ilegível (vermelho sobre claro, `mono` pequeno sobre vídeo claro);
   - [ ] etiquetas cobrindo nomes ou outro texto;
   - [ ] a marca @ **abaixo** da legenda e sem tocá-la;
   - [ ] nenhuma cena parada por mais de 3 s;
   - [ ] clipe coerente com a fala, sem logos;
   - [ ] o final no tom do vídeo.
3. **Corrija e tire os quadros de novo** só nos momentos alterados.
4. **Render:** `render --quality standard -o renders/<nome>_master.mp4`, em segundo plano (~3 min para 60 s). Escreva o REVIEW enquanto isso.
5. **Volume:** `ffmpeg -i master.mp4 -af ebur128=peak=true -f null -`. Meta: cerca de −13,5 LUFS e pico real abaixo de −2 dBTP.
6. **Cópia final** para a Área de Trabalho: x264 CRF 19, AAC 192k, `+faststart`, com o nome `<TÍTULO> - Short.mp4`.
7. **Loop:** o quadro 0 e o último lado a lado (`hstack`) devem ser iguais.
8. **`video/REVIEW.md`:** as decisões, o que foi **medido**, o que foi **só olhado** ("ninguém ouviu o som"), os avisos mantidos e as fontes.
9. **Aprendizado novo?** Acrescente no `LESSONS_LEARNED.md` deste kit.
