---
name: short-script
description: Use quando o criador mandar um vídeo de referência (ou um tema) para virar um YouTube Short/TikTok. Pergunta o @ do canal e a voz, cria a pasta do projeto, analisa a referência, escreve o roteiro de 40–60 s com a mesma narrativa e dados reais conferidos, entrega o texto do ElevenLabs v4 e prepara títulos, descrição e comentário fixado.
---

# Roteiro de um Short novo

Leia antes `RULES.md` e `RETENTION_GUIDE.md` (na raiz deste kit). Fale com o criador em linguagem simples, no idioma dele.

## Passo a passo

1. **Pergunte antes de tudo** (use a ferramenta de perguntas se houver):
   - **qual @ do canal usar**. Nunca invente nem reaproveite o @ de outro projeto;
   - qual voz e quais ajustes do ElevenLabs;
   - o tom do vídeo: energético ou calmo, pausado e dramático.
2. **Crie a pasta do projeto** fora de pastas do sistema, por exemplo `<projetos>\<nome-curto>`:
   - copie `template\` deste kit para lá;
   - copie `lib\*.py` e `lib\vhs*.json` para `<projeto>\build\`;
   - copie `kit.example.json` como `<projeto>\kit.json` e preencha `handle` (o @ respondido), `ffmpeg_bin`, `python`, voz e horário;
   - coloque a referência em `<projeto>\referencia\referencia.mp4`.
3. **Analise a referência:**
   - transcreva com `build\transcribe.py <video> <pasta-tmp> <saida.json>`, rodando o Python do `kit.json` a partir de uma pasta em que `tools.analysis.transcriber` exista (ex.: OpenMontage); modelo medium, idioma pt;
   - tire quadros com ffmpeg (`fps=1/3,scale=150:-1,tile=10x3`) e olhe a montagem;
   - preencha no `ROTEIRO.md` as seções "O que a referência faz" e "Por que funciona";
   - **nada de imagens da referência no nosso vídeo.**
4. **Confira os números** na internet, em fontes oficiais (institutos de estatística, bancos centrais, leis, institutos de pesquisa):
   - mantenha a lógica da referência e arredonde com base no dado real;
   - cite a fonte e corrija a referência quando ela errar (ex.: a quem uma frase é atribuída);
   - sem fonte boa, não cite número.
5. **Escreva o roteiro** em `ROTEIRO.md`, a partir de `SCRIPT_TEMPLATE.md`, seguindo o esqueleto do guia:
   - gancho em até 2 s, com "você" e um número;
   - mistério até os 5 s;
   - 3 a 5 itens com pontes;
   - contagem temática na tela (não só "1/3");
   - pergunta SIM/NÃO onde não pareça encerramento;
   - CTA numa frase: like, **manda pra "quem é assim"** e segue pra parte 2;
   - última frase que emenda no gancho (loop);
   - em tema grave, o tamanho real das consequências;
   - **nunca** "Você sabe quem é".
6. **Escreva o texto do ElevenLabs** em `narracao_elevenlabs.txt`, a partir de `narration_template.txt`:
   - marcações de emoção coerentes com o tom escolhido;
   - MAIÚSCULAS na ênfase, números por extenso, nada de sussurro;
   - instruções de voz conforme o `kit.json`.
7. **Prepare títulos e textos** (seção 5 do roteiro):
   - TikTok: frase curta + 5 #;
   - YouTube Shorts: gancho até 60 caracteres + 5 #;
   - descrição com lista, pergunta, CTA, **fontes** e várias #, citando o @ do `kit.json`;
   - comentário para fixar.
8. **Entregue PRIMEIRO o texto da narração e pare.** Só monte depois que o criador mandar o mp3, com a skill `short-build`.

## Exemplos

- `template\SCRIPT_TEMPLATE.md` e `template\narration_template.txt`: há uma versão energética e outra calma, pausada e dramática.
- `RETENTION_GUIDE.md`, seção 2: o esqueleto de tempo de cada parte.
