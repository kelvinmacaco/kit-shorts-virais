---
name: short-analytics
description: Use quando o criador mandar prints (ou um zip de prints) do YouTube Studio e/ou TikTok Studio. Tabula as métricas por vídeo, compara com as metas do RETENTION_GUIDE.md, tira conclusões com números e atualiza as regras do kit para os próximos vídeos.
---

# Análise do canal

1. **Abra os prints.** Se vier um zip, extraia numa pasta nova e leia todas as imagens.
2. **Tabule os dados num script**, para não errar conta:
   - **TikTok, por vídeo:** duração, views, tempo médio, % assistida (médio ÷ duração), "assistiu ao vídeo completo", novos seguidores, curtidas, comentários, compartilhamentos, salvos e horário de postagem;
   - **YouTube, por vídeo:** duração, views, retenção média e "% ainda assistindo em 0:30".
3. **Tire conclusões que os números sustentam**, deixando claro quando a amostra é pequena:
   - onde as pessoas saem (os primeiros 8 s?);
   - quais temas e horários passam do lote inicial (~150–200 views no TikTok);
   - o que segura a retenção (pergunta aberta respondida no fim, lista de rostos, estilo);
   - por que ninguém segue ou comenta.
4. **Compare com a tabela de metas** da seção 3 do `RETENTION_GUIDE.md`, mostrando o hoje e a meta lado a lado.
5. **Atualize o kit:**
   - acrescente as conclusões e as regras novas ao `RETENTION_GUIDE.md` e ao `RULES.md`;
   - se surgir uma peça visual nova que valha para todo vídeo, crie em `lib\lib_short.py`, teste num projeto temporário (check + snapshot) e documente no README.
6. **Responda ao criador em linguagem simples:**
   - os 3 a 6 achados principais com números;
   - o que muda nos próximos vídeos;
   - o pedido dos próximos prints, 48 h depois de cada post.
