# Regras do kit (valem para todo Short)

## Antes de começar: pergunte ao criador
- **Qual @ do canal usar.** Nunca invente, nunca reaproveite o @ de outro projeto e nunca use um @ padrão. Guarde a resposta no `kit.json` do projeto. Sem @, o `build.ps1` e o `write_index` param de propósito.
- **Qual voz e quais ajustes do ElevenLabs** ele usa. Se não tiver preferência, sugira Eleven v4 com Stability entre 35 e 50%, Similarity 75%, Speed 1.0 e sem "v4 Enhance".
- **O tom do vídeo:** energético e indignado, ou calmo, pausado e dramático (bom para temas pesados).

## Marca @
- Fica pequena e translúcida (Inter 700, 30px, branco a 24%), **logo abaixo da faixa da legenda**. A biblioteca calcula `WM_TOP = CAP_TOP + CAP_H + 14`.
- **Nunca sobrepõe a legenda.** Não mude `WM_TOP` à mão; se a legenda mudar de lugar, mude `CAP_TOP`/`CAP_H`, e a marca acompanha.

## Roteiro
- **Duração:** 40 a 60 s, ou 110 a 150 palavras. Se render mais, divida em parte 1 e parte 2.
- **Gancho:** em até 2 s, falando com o "você", com um número ou uma acusação concreta. O título fica enorme já no quadro 0 (é a miniatura).
- **Mistério:** aberto até os 5 s e respondido no fim ("o terceiro já tem data", "o último é o pior").
- **Lista de 3 a 5 itens,** com uma ponte de curiosidade a cada 8 s ou menos.
- **Contagem temática:** evite um "1/3, 2/3, 3/3" genérico na tela e use algo do tema (ex.: um pavio aceso que anda a cada sinal e explode no estopim). O `step_badge` só serve como último recurso.
- **Pergunta de comentário (SIM/NÃO):** se uma pausa no meio parecer encerramento, leve a pergunta para o final, como reflexão.
- **CTA:** no máximo 3 s, numa frase: like, mandar para "quem é assim" e "segue pra parte 2". Esse pedido de compartilhar com alguém é obrigatório.
- **Final em loop:** a última frase emenda no gancho.
- **Números:** "aproximados, não chute". Mantenha a lógica da referência com dados reais conferidos e cite a fonte. Se não houver fonte boa, não cite número.
- **Tom:** política e economia em tom neutro e sem partido, nomeando países e pessoas pelo que fazem, sem rótulos.
- **Temas graves:** mostre o tamanho real das consequências, com dado conferido.
- **Não use a frase "Você sabe quem é"** nem a cena do olho piscando: o feedback foi que soa forçado.
- **Narração:**
  - marcações de emoção do ElevenLabs v4 e MAIÚSCULAS para ênfase;
  - números por extenso;
  - **nada de sussurro**;
  - pausas só onde pesam.
- **Ordem de entrega:** **primeiro o texto da narração**. Só monte depois que o criador mandar o mp3. Para trocar só um trecho, peça só a parte nova, com os mesmos ajustes de voz (skill `short-voice-patch`).

## Visual
- **Movimento:** nada parado por mais de 3 s. Algo muda a cada 1,5–2,5 s: um corte, zoom, número, palavra que pula, tremida ou animação.
- **Interação em cada cena:** contadores, barras, alvos pulsando, fluxos entre elementos, radar, setas que se chocam. Mais animação segura mais gente.
- **Fita VHS/CRT em toda filmagem real:**
  - cores INK #EFE8D8, AMBER #FFC21A, RED #FF3B3B, CYAN #63D5E8, GROUND #141114;
  - fontes Archivo Black, Inter 900 e Space Mono.
- **Área segura para texto:** x de 90 a 900 (os botões do TikTok ficam à direita) e y de 170 a 1330.
- **Vídeos:** só grátis (Pexels/Pixabay), vistos em miniatura antes de usar. **Descarte** logos, marcas e camisas de time, e também o que não combina com a fala (moto ≠ carro).
- **O final segue o tom do vídeo.** Num vídeo pesado, o final é escuro e lento, com fades e sem estouro de coração, flash ou corte rápido. Num vídeo leve, pode ter coração e aviãozinho.

## Áudio
- **Voz:** nivelada frase por frase (`level_voice.py`).
- **Trilha:** do Pixabay, sem Content ID, a cerca de 0,10.
- **Efeitos:** pop nas palavras, whoosh nos cortes e impacto só nos 3 ou 4 momentos fortes.
- **Master:** cerca de −13,5 LUFS, com pico real abaixo de −2 dBTP.

## Publicação
- **Horário:** postar entre 19h e 23h, de preferência perto das 22h. 1 por dia, no mesmo horário.
- **Títulos:**
  - TikTok: frase curta + 5 hashtags;
  - YouTube Shorts: gancho em até 60 caracteres + 5 hashtags.
- **Descrição do YouTube:** a lista, a pergunta, o CTA, as fontes e várias hashtags.
- **Comentário fixado:** a pergunta do vídeo ou a fonte, mais "parte 2 vem aí".
- **Acompanhamento:** prints de 48 h depois de cada post, comparados com as metas do `RETENTION_GUIDE.md`.
