# Guia de retenção e seguidores

Regras tiradas da análise real de 20 Shorts e TikToks (10 de cada rede) de um canal pequeno de comentário, sobre economia, política e reflexão. Os números servem de ponto de partida: meça o seu canal com a skill `short-analytics` e atualize este guia.

## 1. O que os dados mostraram

1. **No TikTok, a pessoa sai antes dos 16 segundos.** Em vídeos de 60 a 185 s, o tempo médio ficou entre 6 e 16 s, e só 1–9% assistiram até o fim. O TikTok mostra cada vídeo para umas 150–200 pessoas e para de distribuir quando ninguém termina.
2. **O horário pesou.** Os únicos vídeos que passaram de 600 views no TikTok foram postados por volta das 22h30. Os de manhã e de tarde ficaram em ~170.
3. **O YouTube Shorts é mais paciente.** A retenção média ficou entre 40 e 59%. Temas de dinheiro e poder passaram de mil views; reflexão abstrata, sem gancho concreto, ficou com menos de 10.
4. **O vídeo que mais segurou** (84% ainda assistindo em 0:30, mesmo com 3 min) **abriu uma pergunta e só respondeu no fim**, com uma lista de rostos em que cada item renovava a curiosidade.
5. **A maior perda acontece nos primeiros 8 segundos**: de 30 a 40% em alguns vídeos.
6. **Seguidores e comentários quase zero quando o vídeo não pede:** sem pergunta na tela, sem "parte 2", sem uma promessa clara do canal.
7. **O estilo animado de fita VHS foi o que mais prendeu** (38% do vídeo assistido e 18% de engajamento). O que faltava nele era ser mais curto.

## 2. Esqueleto de roteiro (~45–55 s)

| Tempo | Parte | O que dizer | Na tela |
|---|---|---|---|
| 0–2 s | Gancho | Frase com "você" e um número ou uma acusação | Título enorme já no quadro 0 |
| 2–5 s | Mistério | "…e o último é o pior" ou "o terceiro já tem data" | Palavra-chave pulando |
| 5–35 s | Lista de 3 a 5 itens | Um item a cada 6–8 s, com uma ponte de curiosidade | Indicador de progresso **temático**, números, cortes de 2 s |
| ~60% ou final | Pergunta | "Você…? Comenta SIM ou NÃO" | `comment_card` ou reflexão no final escuro |
| 35–45 s | Revelação | Responde o mistério; em tema grave, o tamanho real do estrago | Número grande, tremida |
| 45–50 s | CTA, numa frase | Like, manda pra quem ___ e segue pra parte 2 | Coração, avião, `follow_card` |
| 50–55 s | Loop | Frase que emenda no gancho | A cena volta até o quadro 0 |

## 3. Metas para medir (prints de 48 h)

| Métrica | Ponto de partida observado | Meta |
|---|---|---|
| TikTok: tempo médio / duração | 10–38% | **acima de 50%** |
| TikTok: viu até o fim | 1–9% | **acima de 20%** |
| TikTok: views por vídeo | ~170 | passar de 500 com frequência |
| Seguidores por 1.000 views | ~0,4 | **acima de 5** |
| YouTube: % ainda assistindo em 0:30 | 37–84% | **acima de 70%** |
| Comentários por vídeo | 0 | 3 ou mais |

## 4. Aprendizados da produção

- **Contagem temática, não genérica.** Um "1/3, 2/3, 3/3" na tela pareceu genérico. Funcionou melhor um indicador do próprio tema, como um pavio aceso que queima a cada sinal e explode no clímax (`pavio_scene` na biblioteca).
- **A pergunta no meio pode soar como final.** Se a narração para para perguntar, leve a pergunta para o fim, como reflexão, e deixe o meio correr.
- **O final acompanha o tom.** Num vídeo pesado, um final alegre e rápido (coração estourando, flashes) quebra o clima. Use fade até o preto, entradas suaves e nenhum efeito sonoro.
- **Mais animação segura mais gente.** Cada cena deve ter uma interação: contador, alvo pulsando, fluxo entre elementos, radar, setas que se chocam, calendário que gira.
- **Tema grave:** mostre o tamanho real das consequências, com dado conferido.
- **Narração:**
  - nada de sussurro, que some no celular;
  - mais emoção sai com marcações fortes, MAIÚSCULAS e Stability mais baixa;
  - um tom calmo e pesado também funciona, com pausas só onde pesam.
- **Frases forçadas de "cumplicidade"** ("você sabe quem é") soaram mal. Prefira um CTA direto.
- **A marca @ fica abaixo da legenda e nunca a sobrepõe.** O @ é sempre perguntado ao criador.
