# Aprendizados: o que deu certo e o que não deu

Tudo o que foi aprendido produzindo 6 Shorts reais, com várias versões cada, e analisando os números de 20 vídeos de um canal. Cada item termina com a **regra que ficou** no kit. Estas regras já estão em `RULES.md`, nas skills e na biblioteca.

---

## 1. Roteiro e estrutura

| ✅ Deu certo | ❌ Não deu certo | Regra que ficou |
|---|---|---|
| Copiar a **narrativa** da referência (a ordem dos argumentos), não as palavras | Usar qualquer imagem da referência | Mesma lógica, texto e imagens próprios |
| Gancho direto com "você" e um número, ou uma promessa de prova ("eu posso te provar que…") | Abrir com pergunta genérica ou introdução lenta | Gancho em até 2 s, e o título no quadro 0 é a miniatura |
| Um mistério aberto no começo e respondido no fim ("o terceiro já tem data") | Entregar tudo logo de cara | Mistério até os 5 s, pago na revelação |
| Lista de 3 itens, do mais fraco ao mais forte | Vídeos de 60 a 185 s: a pessoa saía antes dos 16 s | 40–60 s; se render mais, parte 1 e parte 2 |
| Fechar com o **tamanho real** das consequências num tema grave (ex.: número de ogivas) | Final sem peso | Em tema grave, o dado do estrago, conferido |
| A pergunta SIM/NÃO **no final**, como reflexão | A pergunta no meio, com pausa: **pareceu encerramento** | A pergunta vai onde não pareça fim |
| CTA de uma frase: like, manda pra "quem é assim" e segue pra parte 2 | CTA longo no fim, que faz a pessoa sair antes de completar | CTA de no máximo 3 s, e a parte 2 prometida vira o próximo vídeo |
| Uma última frase que emenda no gancho (loop) | Final que fecha sem volta | Sempre em loop |
| Números aproximados, conferidos e com fonte | **Número chutado** ou atribuição errada (a frase era da CIA, não do líder citado) | "Aproximado, não chute"; corrija a referência quando ela errar |
| Tom neutro, nomeando países e pessoas pelo que fazem | Rótulos políticos ("eixo das ditaduras") | Neutro e sem partido |
| CTA direto | Frase forçada de cumplicidade ("**você sabe quem é**"), que soou mal | Não usar |

## 2. Narração (ElevenLabs v4)

| ✅ | ❌ | Regra |
|---|---|---|
| Marcações de emoção fortes ([shocked], [outraged], [passionate, rising]), MAIÚSCULAS na ênfase e Stability mais baixa (30–35%) | Narração **sem emoção** com Stability 50% | Marcações + MAIÚSCULAS + Stability ajustada ao tom |
| Tom **calmo, pausado e grave** em tema pesado (Stability 50%, Speed 1.0) | Sussurro: sai 10–15 dB mais baixo e **some no celular** | Nada de sussurro; nivelar frase por frase |
| Entregar **primeiro o texto** e esperar a gravação | Montar antes da voz final | Texto → gravação → montagem |
| Regravar **só o trecho novo**, com os mesmos ajustes, e emendar no silêncio | Regravar tudo por causa de uma frase | Skill `short-voice-patch` |
| Encurtar a pausa longa que cai no gancho (1,1 s → 0,6 s) | Pausa longa nos primeiros segundos | Gancho sem buracos |

## 3. Visual e animação

| ✅ | ❌ | Regra |
|---|---|---|
| Fita **VHS/CRT** com paleta fixa: virou identidade e teve o maior tempo assistido | Visual diferente a cada vídeo | Mesma série visual |
| Algo mudando a cada 1,5–2,5 s: punch-in, palavra que pula, corte, tremida | Cenas paradas: "**muito sem interação**" | Uma interação por cena |
| Interações do tema: contador, barra comida, alvos pulsando, fluxos entre bandeiras, radar, ano que rola, setas que se chocam | Só texto sobre vídeo | Biblioteca de peças + skill `short-animation` |
| **Pavio aceso** como progresso: queima a cada sinal e explode no clímax | Contador "**1/3, 2/3, 3/3**" na tela: **genérico** | Indicador temático (`pavio_scene`); `step_badge` só em último caso |
| Final no **mesmo tom**: num vídeo pesado, escuro e lento, com fade até o preto | Coração estourando e cortes rápidos depois do clímax: **quebrou a vibe** | O final segue o tom |
| Marca @ pequena e translúcida **abaixo da legenda** | Marca no centro, competindo com o texto | `WM_TOP` calculado pela legenda; o @ é perguntado ao criador |
| Bandeiras desenhadas em SVG simples | Vídeos de bandeira ruins ou com brasões | Desenhe quando não houver boa filmagem |
| Revisar cada quadro antes de renderizar | Texto saindo da tela, rótulo ilegível, etiqueta cobrindo um nome | Snapshot e folha de contato sempre |

## 4. Mídia

| ✅ | ❌ | Regra |
|---|---|---|
| Vídeos grátis do Pexels, escolhidos por **miniatura** | Escolher só pelo título | Folha de miniaturas antes de baixar |
| Trilha do Pixabay **sem Content ID** | Trilha com Content ID (bloqueio e desmonetização) | Filtrar sempre |
| Trocar o que não combina com a fala | **Carro guinchado** numa fala sobre moto; **camisa de time com logo** | Descartar marcas e incoerências |
| Vídeo deitado de alta resolução (2560/1920) cortado na vertical | Upscale de 720p deitado | Baixar a versão maior |
| Trechos de filme trocados por vídeos grátis | Usar cena de filme famoso | Nada com direitos autorais |

## 5. Áudio

| ✅ | ❌ | Regra |
|---|---|---|
| Nivelar a narração **frase por frase** (`level_voice.py`) | `loudnorm` dinâmico, que distorceu os níveis relativos | Ganho por frase + limitador |
| Trilha a ~0,10 sob a voz | Trilha alta | 0,10–0,12 |
| Pop nas palavras, whoosh nos cortes, impacto só em 3–4 momentos | Impacto em tudo | Efeitos com parcimônia; final calmo sem efeitos |
| Master em cerca de −13,5 LUFS, com pico real abaixo de −2 dBTP | — | Medir sempre com `ebur128` |

## 6. Publicação e números

| ✅ | ❌ | Regra |
|---|---|---|
| Os vídeos postados por volta de **22h30** foram os únicos a passar de 600 views no TikTok | Os postados de manhã e de tarde ficaram em ~170 views | Postar entre 19h e 23h |
| Temas de dinheiro no bolso, poder e política com dados | Reflexão abstrata sem gancho concreto (menos de 10 views) | Gancho concreto sempre |
| Pergunta aberta respondida no fim (84% ainda assistindo em 0:30) | Vídeo sem pergunta nem "parte 2": **1 seguidor em 2.583 views** | Pergunta + parte 2 + CTA |
| Título com 5 # (TikTok e YouTube) e descrição com fontes e várias # | Título tomado por hashtags | Gancho primeiro, # depois |
| Prints de 48 h para medir | Mudar sem medir | Skill `short-analytics` |

## 7. Técnica (HyperFrames, ffmpeg, Windows)

| ❌ Problema | ✅ Solução |
|---|---|
| `faster-whisper` quebrou com `av` 19 | Fixar `av<19` |
| O whisper quebra "R$ 10.000,00" em vários pedaços | Juntar tokens que começam com `$ . , -` e normalizar ("R$ 10 MIL") em `load_words` |
| `Select-Object -First` na saída do `build.ps1` **interrompeu o script**, e o VHS não foi aplicado | Nunca truncar a saída do montar |
| Uma função de shell chamada `cut` escondeu o comando `cut` do sistema | Nome `corta` |
| f-strings do Python dentro de `python -c` no PowerShell quebram por causa das chaves | Scripts em arquivo ou Bash |
| O scraper de Pixabay do OpenMontage dava 403 | Usar o navegador embutido (fetch de mesma origem) + curl com referer |
| No app desktop (MSIX), arquivos gravados em AppData ficam **invisíveis** para o usuário | Gravar fora de AppData (ex.: `C:\...\projetos`, Área de Trabalho) |
| `visibility`/`opacity` animados no próprio clip: o lint reclamava | Animar um elemento interno |
| `fromTo` posterior aplicando o estado inicial cedo demais (cópias vermelha e ciano aparecendo antes) | `immediateRender: false` |
| `<audio>` repetindo a mesma track | Track única por efeito |
| Composição grande demais por causa do grão | Grão por loop JS com semente |
| Linhas SVG que não "desenhavam" | `pathLength="1"` + dasharray/dashoffset 1 |
| Renomear uma pasta aberta como cwd do shell | Sair da pasta antes (`cd` para fora) |
| O render de 60 s leva ~3 min | Renderizar em segundo plano e escrever o REVIEW enquanto isso |
| Avisos de check que **podem ficar**: contraste da marca translúcida, título curto no loop, rótulo do pavio coberto pela faísca por um instante | Documentar no REVIEW |

## 8. Trabalho com o criador

| ✅ | ❌ | Regra |
|---|---|---|
| Mostrar o que mudou e por quê, em linguagem simples | Jargão técnico | Português simples, frases curtas |
| Perguntar o **@ do canal**, a voz e o tom antes de começar | Supor ou reaproveitar de outro projeto | Perguntar sempre e guardar no `kit.json` |
| Aplicar o feedback a todos os vídeos futuros (regras, lib, skills) | Corrigir só o vídeo da vez | Toda lição vira regra |
| Dizer o que foi medido e o que só foi olhado ("ninguém ouviu o som") | Dizer que está perfeito sem conferir | REVIEW honesto |
