---
name: short-start
description: Ponto de partida para fazer um YouTube Short/TikTok do zero com este kit. Use quando o criador mandar um vídeo de referência, um tema ou disser "quero um Short sobre…". Coordena as outras skills na ordem certa (roteiro → narração → mídia → animação → montagem → revisão → publicação → análise) e garante que nenhuma regra fique de fora.
---

# Short novo: o fluxo completo

Antes de tudo, leia `RULES.md`, `LESSONS_LEARNED.md` e `RETENTION_GUIDE.md`. Use as skills na ordem abaixo e **carregue cada uma quando chegar a vez dela**.

| Etapa | Skill deste kit | Skills de apoio (use ao máximo) |
|---|---|---|
| 0. Perguntar o @ do canal, a voz e o tom | `short-script` (passo 1) | ferramenta de perguntas |
| 1. Analisar a referência e escrever o roteiro e o texto da narração | `short-script` | `graphify` para consultar a lib; busca na web para conferir os números |
| 2. Esperar o mp3 do criador | — | — |
| 3. Narração: transcrever, encurtar pausas e nivelar | `short-build` (seção 1) | `media-use` (transcrição, mixagem) |
| 4. Mídia grátis: vídeos, trilha, efeitos e cortes | `short-media` | `media-use` (mídia e tratamentos), navegador embutido |
| 5. Animação: cenas, peças e indicador temático | `short-animation` | `hyperframes` (contrato de render), `hyperframes-registry` (blocos prontos antes de desenhar à mão) |
| 6. Montagem: generate.py, VHS e índice com o @ | `short-build` | `hyperframes-cli`, `media-use` (media-treatment) |
| 7. Revisão: check, quadros, render, volume, loop | `short-review` | `hyperframes-cli` (check, snapshot, render) |
| 8. Publicação: títulos, descrição, horário, comentário | `short-publish` | — |
| 9. Depois de 48 h: prints → ajustes | `short-analytics` | — |
| Trocar só um trecho da fala | `short-voice-patch` | — |

## Regras que nunca podem faltar
- **O @ do canal é perguntado ao criador** e vai para o `kit.json`. A biblioteca recusa montar sem ele.
- **A marca @ fica abaixo da legenda e nunca a sobrepõe** (`WM_TOP`).
- **Primeiro o texto da narração**; só depois a montagem.
- **Nada da referência** na imagem, nada com Content ID na trilha.
- **Cada aprendizado novo** entra no `LESSONS_LEARNED.md`, no `RULES.md` e, se for visual, na `lib`.
