"""MODELO de generate.py: esqueleto genérico de um Short (~50 s), já no padrão das RULES.md e do RETENTION_GUIDE.md.

Uso: python generate.py <pasta-video> <narracao_words.json> <duracao-total> <@do-canal>
(normalmente quem chama é o build/build.ps1, que lê o @ do kit.json do projeto)

O @ do canal NUNCA fica fixo no código: pergunte ao criador qual @ usar (vai no kit.json).

COMO ADAPTAR (ver também a skill short-animation)
1. SCENES: troque pelos trechos do seu roteiro, (nome, início, fim) em segundos GLOBAIS, a partir do
   narracao_words.json. Dentro de cada scene() os tempos são LOCAIS (0 = início da cena).
2. Troque os textos em MAIÚSCULAS ("TÍTULO", "ITEM 1"...) e os tempos pelos das palavras da sua narração.
3. Os clipes ("gancho.mp4"...) ficam em video/assets/video/, cortados com tools/ffmpeg_recipes.md.
   gancho_volta.mp4 é o primeiro segundo do gancho invertido (para o loop).
4. Estrutura padrão (RETENTION_GUIDE.md, seção 2):
   gancho (título no quadro 0) → mistério → 3 itens com o PAVIO temático por cima → revelação
   (o tamanho real) → final calmo (pergunta + like + compartilhar + seguir, fade até o preto) → loop.
   Vídeo energético: troque o final calmo por like_block + plane_svg + follow_card, e use comment_card
   perto de 60% (só se a pausa não soar como encerramento).
5. Regras de ouro: algo muda a cada 1,5–2,5 s; uma interação por cena (contador, alvo, setas...);
   texto dentro de x 90–900 e y 170–1330; a marca @ é posta pela lib abaixo da legenda (WM_TOP).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # lib_short.py copiado de lib/ do kit
from lib_short import *

init(sys.argv[1])
WORDS = sys.argv[2]
TOTAL = float(sys.argv[3])
HANDLE = sys.argv[4] if len(sys.argv) > 4 else None  # o @ do canal, escolhido pelo criador

PAVIO = (9.0, 33.4)  # cobre os 3 itens; explode no clímax do item 3
SCENES = [
    ("gancho", 0.0, 5.0), ("misterio", 5.0, 9.0), ("item1", 9.0, 17.0), ("item2", 17.0, 25.0),
    ("item3", 25.0, 33.0), ("pavio", *PAVIO), ("revelacao", 33.0, 41.0), ("fim", 41.0, 48.0),
    ("rebobina", 48.0, TOTAL),
]
BR = 'Math.round(v).toLocaleString("pt-BR")'


def cut_in(sel, t):
    return f'    tl.fromTo("{sel}", {{ scale: 1.14 }}, {{ scale: 1, transformOrigin: "540px 900px", duration: 0.55, ease: "expo.out" }}, {f(t)});'


def drift(sel, t, dur, s=1.08):
    return f'    tl.fromTo("{sel}", {{ scale: 1 }}, {{ scale: {s}, transformOrigin: "540px 900px", duration: {f(dur)}, ease: "power1.inOut" }}, {f(t)});'


def soft(items, dur=0.45):
    """Palavras que entram devagar (final calmo)."""
    return "\n".join(f'    tl.fromTo("{s}", {{ opacity: 0, y: 18, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: {dur}, ease: "power2.out" }}, {f(t)});'
                     for s, t in items)


def counter(sel, t, dur, to, fmt, frm=0):
    """Número que conta de `frm` até `to` (fmt: expressão JS sobre v)."""
    return (f'    {{ const el = document.querySelector("{sel}"); const c = {{ v: {frm} }};\n'
            f'      tl.fromTo(c, {{ v: {frm} }}, {{ v: {to}, duration: {f(dur)}, ease: "power2.out", onUpdate: () => {{ const v = c.v; el.textContent = {fmt}; }} }}, {f(t)}); }}')


DOTS_CSS = """
    .dots { position: absolute; inset: 0; background-image: radial-gradient(circle, rgba(255,59,59,0.85) 3.4px, transparent 3.9px); background-size: 17px 17px; }
    .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 60% 26% at 50% 40%, rgba(20,17,20,0.96) 0%, rgba(20,17,20,0.85) 55%, rgba(20,17,20,0) 100%); }"""


# ---------------------------------------------------------------- gancho: o título fica no quadro 0 (miniatura) e volta no loop
def hook_html(prefix):
    return "\n      ".join([
        f'<div id="{prefix}-l0" class="kt am" style="top:840px; font-size:120px">TÍTULO</div>',
        f'<div id="{prefix}-l1" class="kt" style="top:968px; font-size:96px">DO GANCHO</div>',
        f'<div id="{prefix}-l2" class="kt rd" style="top:1072px; font-size:116px">PERGUNTA?</div>',
    ])


scene("gancho", f"""
{fvw("s0-vw", "s0-v", "gancho.mp4", 0, 5.0)}
    <div class="gb"></div>
    <div id="s0-t" class="clip" data-start="0" data-duration="2.6">
      {hook_html("s0")}
    </div>
    <div id="s0-a" class="clip" data-start="2.6" data-duration="2.4">
      {kline("s0-a", [("FRASE", ""), ("COM", "")], 900, 100)}
      {kline("s0-a", [("VOCÊ", ""), ("E", ""), ("NÚMERO", "rd")], 1010, 110, 2)}
    </div>
""", f"""
{drift("#s0-vw", 0, 5.0, 1.12)}
{shake("#s0-t > div", 1.2, 10)}
    tl.to("#s0-t > div", {{ opacity: 0, filter: "blur(10px)", duration: 0.12, ease: "power2.in", stagger: 0.03 }}, 2.4);
{words_js([("#s0-a0", 2.65), ("#s0-a1", 2.9), ("#s0-a2", 3.3), ("#s0-a3", 3.5)])}
{slam("#s0-a4", 3.9, 2.0)}
{shake("#s0-vw", 3.9, 16)}
""")

# ---------------------------------------------------------------- mistério: aberto aqui, pago na revelação
scene("misterio", f"""
{fvw("s1-vw", "s1-v", "misterio.mp4", 0, 4.0)}
    <div class="gb"></div>
    <div class="luzes">{"".join(f'<i id="s1-z{k}"></i>' for k in range(3))}</div>
    {kline("s1-a", [("SÃO", ""), ("3", "am"), ("SINAIS", "")], 860, 120)}
    {kline("s1-a", [("O", ""), ("ÚLTIMO", ""), ("É", ""), ("O", ""), ("PIOR", "rd")], 1000, 96, 3)}
""", "\n".join([
    cut_in("#s1-vw", 0),
    words_js([("#s1-a0", 0.1)]),
    slam("#s1-a1", 0.3, 2.6),
    *(f'    tl.fromTo("#s1-z{k}", {{ background: "rgba(255,59,59,0)", scale: 0.6 }}, {{ background: "rgba(255,59,59,1)", scale: 1, duration: 0.25, ease: "back.out(2)" }}, {f(0.35 + k * 0.16)});' for k in range(3)),
    words_js([("#s1-a2", 0.7), ("#s1-a3", 1.6), ("#s1-a4", 1.8), ("#s1-a5", 2.2), ("#s1-a6", 2.35)]),
    slam("#s1-a7", 2.6, 2.2),
    shake("#s1-vw", 2.6, 16),
]), f"""
    .luzes {{ position: absolute; left: 0; right: 0; top: 740px; display: flex; justify-content: center; gap: 48px; }}
    .luzes i {{ width: 54px; height: 54px; border-radius: 50%; border: 5px solid {RED}; box-shadow: 0 0 30px rgba(255,59,59,0.8); }}""")

# ---------------------------------------------------------------- item 1: rótulo + contador
scene("item1", f"""
{fvw("s2-vw", "s2-v", "item1.mp4", 0, 8.0)}
    <div class="gt"></div>
    <div id="s2-d" class="clip dim" data-start="1.8" data-duration="6.2" style="opacity:0.5"></div>
    <div id="s2-m" class="clip mono" data-start="0.05" data-duration="1.8" style="top:280px; font-size:34px"><span id="s2-m-i" style="display:inline-block">PRIMEIRO SINAL</span></div>
{label("s2-l", "ITEM 1", 0.4, 1.8, 330, 130)}
    <div id="s2-n" class="clip big" data-start="2.0" data-duration="6.0" style="top:420px; font-size:200px"><span id="s2-num" style="display:inline-block">0%</span></div>
    <div id="s2-s" class="clip mono" data-start="3.0" data-duration="5.0" style="top:660px; font-size:32px; color:{INK}"><span id="s2-s-i" style="display:inline-block">O QUE O NÚMERO SIGNIFICA</span></div>
""", "\n".join([
    cut_in("#s2-vw", 0), fade_in("#s2-m-i", 0.1), lbl_in("s2-l", 0.45),
    counter("#s2-num", 2.1, 0.6, 84.9, 'v.toFixed(1).replace(".", ",") + "%"'),
    '    tl.fromTo("#s2-num", { scale: 1.3 }, { scale: 1, duration: 0.3, ease: "expo.out", immediateRender: false }, 2.7);',
    shake("#s2-vw", 2.7, 16), fade_in("#s2-s-i", 3.1), drift("#s2-vw", 3.0, 5.0, 1.08),
]))

# ---------------------------------------------------------------- item 2: rótulo + alvos pulsando
scene("item2", f"""
{fvw("s3-vw", "s3-v", "item2.mp4", 0, 8.0)}
    <div class="gt"></div>
    <div id="s3-m" class="clip mono" data-start="0.05" data-duration="1.8" style="top:280px; font-size:34px"><span id="s3-m-i" style="display:inline-block">SEGUNDO SINAL</span></div>
    <div id="s3-pp" class="clip" data-start="0.4" data-duration="7.6" data-layout-allow-overlap>
      {"".join(f'<div id="s3-p{k}" class="ping" style="left:450px; top:850px"></div>' for k in range(2))}
    </div>
{label("s3-l", "ITEM 2", 0.4, 8.0, 330, 130, "am")}
    <div id="s3-s" class="clip mono" data-start="1.4" data-duration="6.6" style="top:480px; font-size:32px; color:{INK}"><span id="s3-s-i" style="display:inline-block">DETALHE QUE PROVA</span></div>
""", "\n".join([
    cut_in("#s3-vw", 0), fade_in("#s3-m-i", 0.1), lbl_in("s3-l", 0.45), fade_in("#s3-s-i", 1.5),
    *(f'    tl.fromTo("#s3-p{k}", {{ scale: 0.2, opacity: 0.9 }}, {{ scale: 1.6, opacity: 0, duration: 0.9, ease: "power1.out", repeat: 6, immediateRender: false }}, {f(0.5 + k * 0.45)});' for k in range(2)),
    drift("#s3-vw", 0.6, 7.4, 1.1),
]), """
    .ping { position: absolute; width: 180px; height: 180px; border-radius: 50%; border: 6px solid #FF3B3B; opacity: 0; }""")

# ---------------------------------------------------------------- item 3: o mais forte; setas que se chocam
scene("item3", f"""
{fvw("s4-vw", "s4-v", "item3.mp4", 0, 8.0)}
    <div class="gt"></div>
    <div id="s4-m" class="clip mono" data-start="0.05" data-duration="1.8" style="top:280px; font-size:34px"><span id="s4-m-i" style="display:inline-block">E O TERCEIRO…</span></div>
{label("s4-l", "ITEM 3", 0.6, 8.0, 330, 130, "rd")}
    <div id="s4-x" class="clip" data-start="2.0" data-duration="6.0" data-layout-allow-overlap>
      <div id="s4-ar" class="arrow ar-r">LADO A ▶</div>
      <div id="s4-ab" class="arrow ar-b">◀ LADO B</div>
      <div id="s4-hit" class="hit"></div>
    </div>
""", "\n".join([
    cut_in("#s4-vw", 0), fade_in("#s4-m-i", 0.1), lbl_in("s4-l", 0.65),
    '    tl.fromTo("#s4-ar", { x: -700, opacity: 0 }, { x: 0, opacity: 1, duration: 1.6, ease: "power2.in" }, 2.2);',
    '    tl.fromTo("#s4-ab", { x: 700, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: "power2.in" }, 3.2);',
    '    tl.fromTo("#s4-hit", { opacity: 0.95, scale: 0.3 }, { opacity: 0, scale: 2.2, duration: 0.5, ease: "power2.out", immediateRender: false }, 3.8);',
    shake("#s4-vw", 3.8, 24),
]), f"""
    .arrow {{ position: absolute; top: 1080px; width: 440px; padding: 14px 0; text-align: center; font-family: 'Archivo Black'; font-size: 54px; color: #fff;
      border-radius: 14px; opacity: 0; box-shadow: 0 14px 30px rgba(0,0,0,0.5); }}
    .ar-r {{ left: 100px; background: {RED}; }}
    .ar-b {{ left: 540px; background: #2F6BD6; }}
    .hit {{ position: absolute; left: 390px; top: 960px; width: 300px; height: 300px; border-radius: 50%; opacity: 0;
      background: radial-gradient(circle, #fff 0%, rgba(255,194,26,0.9) 35%, rgba(255,59,59,0) 70%); }}""")

# ---------------------------------------------------------------- pavio: indicador temático por cima dos 3 itens (explode no clímax)
pv_b, pv_j, pv_c = pavio_scene(*PAVIO, keys=[(9.0, 120), (9.4, 150), (10.0, 330), (17.0, 360), (17.6, 610), (25.0, 640), (25.7, 890), (31.6, 905), (33.0, 990)],
                               lit=[10.0, 17.6, 25.7], boom=33.0)
scene("pavio", pv_b, pv_j, pv_c)

# ---------------------------------------------------------------- revelação: o tamanho real (contador + tela que se enche)
scene("revelacao", f"""
{fvw("s5-vw", "s5-v", "revelacao.mp4", 0, 4.4)}
    <div id="s5-d" class="clip dim" data-start="0" data-duration="4.4" style="opacity:0.5"></div>
    <div id="s5-a" class="clip" data-start="0.05" data-duration="4.3">
      {kline("s5-a", [("E", ""), ("AGORA,", "")], 820, 80)}
      {kline("s5-a", [("IMAGINA", ""), ("O", "")], 920, 100, 2)}
      {kline("s5-a", [("TAMANHO", "am"), ("DISSO", "am")], 1030, 110, 4)}
    </div>
    <div id="s5-c" class="clip" data-start="4.4" data-duration="3.6" data-layout-allow-overlap>
      <div class="dim" style="opacity:0.92"></div>
      <div id="s5-dots" class="dots"></div>
      <div class="vig"></div>
      <div class="mono" style="top:560px; font-size:40px; color:{INK}"><span id="s5-h" style="display:inline-block">HOJE:</span></div>
      <div class="big" style="top:630px; font-size:230px"><span id="s5-n" style="display:inline-block">0</span></div>
      <div class="mono" style="top:880px; font-size:38px; color:{INK}"><span id="s5-o" style="display:inline-block">O QUE ESSE NÚMERO É</span></div>
      <div class="mono" style="top:1000px; font-size:30px; color:{INK}"><span id="s5-src" style="display:inline-block; opacity:0.75">FONTE · ANO</span></div>
    </div>
""", "\n".join([
    drift("#s5-vw", 0, 4.4, 1.15),
    words_js([("#s5-a0", 0.1), ("#s5-a1", 0.4), ("#s5-a2", 1.2), ("#s5-a3", 1.6), ("#s5-a4", 1.8)]),
    slam("#s5-a5", 2.2, 1.8),
    fade_in("#s5-h", 4.5),
    '    tl.fromTo("#s5-dots", { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 1.8, ease: "power1.in" }, 4.5);',
    counter("#s5-n", 4.6, 1.6, 12187, BR),
    '    tl.fromTo("#s5-n", { scale: 1.35 }, { scale: 1, duration: 0.35, ease: "expo.out", immediateRender: false }, 6.2);',
    shake("#s5-n", 6.2, 22), fade_in("#s5-o", 6.1), fade_in("#s5-src", 6.4),
]), DOTS_CSS)

# ---------------------------------------------------------------- final calmo: pergunta, like, compartilhar, seguir; fade até o preto
scene("fim", f"""
    <div class="dim" style="opacity:0.92"></div>
    <div id="s6-dots" class="dots"></div>
    <div class="vig"></div>
    <div id="s6-q" style="position:absolute; inset:0">
      {kline("s6-q", [("E", ""), ("VOCÊ…", "")], 760, 90)}
      {kline("s6-q", [("PERGUNTA", ""), ("FÁCIL?", "am")], 870, 90, 2)}
      <div class="opts"><span id="s6-o0">SIM</span><span id="s6-o1">NÃO</span></div>
    </div>
    <div id="s6-hw" style="position:absolute; left:405px; top:520px; width:270px; height:252px; opacity:0">
      <svg viewBox="0 0 600 560" style="width:100%;height:100%;overflow:visible"><path id="s6-heart" d="{HEART}" style="fill:rgba(198,40,40,0)" stroke="{INK}" stroke-width="14" stroke-linejoin="round"/></svg>
    </div>
    {kline("s6-l", [("DEIXA", ""), ("O", ""), ("LIKE", "")], 830, 76)}
    {kline("s6-a", [("MANDA", ""), ("PRA", ""), ("QUEM", "")], 960, 64)}
    {kline("s6-a", [("É", ""), ("ASSIM", "am")], 1040, 64, 3)}
    <div class="fcw"><div id="s6-fc" class="fc"><b>+</b>SEGUE PRA PARTE 2</div></div>
    <div id="s6-black" class="dim" style="opacity:0"></div>
""", "\n".join([
    '    tl.fromTo("#s6-dots", { opacity: 1 }, { opacity: 0.28, duration: 2.0, ease: "power1.inOut" }, 0);',
    soft([("#s6-q0", 0.1), ("#s6-q1", 0.4), ("#s6-q2", 1.0), ("#s6-q3", 1.3), ("#s6-o0", 2.0), ("#s6-o1", 2.4)]),
    '    tl.to("#s6-q", { opacity: 0, y: -40, filter: "blur(8px)", duration: 0.5, ease: "power2.in" }, 3.0);',
    '    tl.fromTo("#s6-hw", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.7, ease: "power2.out" }, 3.1);',
    soft([("#s6-l0", 3.15), ("#s6-l1", 3.4), ("#s6-l2", 3.55)]),
    '    tl.to("#s6-heart", { fill: "rgba(198,40,40,1)", stroke: "rgba(198,40,40,1)", duration: 0.6, ease: "power1.out" }, 3.6);',
    soft([("#s6-a0", 4.2), ("#s6-a1", 4.35), ("#s6-a2", 4.5), ("#s6-a3", 4.7), ("#s6-a4", 4.85)]),
    '    tl.fromTo("#s6-fc", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }, 5.6);',
    '    tl.fromTo("#s6-black", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "power1.in" }, 6.4);',
]), f"""{DOTS_CSS}
    .opts {{ position: absolute; left: 0; right: 0; top: 1000px; display: flex; justify-content: center; gap: 40px; }}
    .opts span {{ padding: 10px 44px 14px; border: 4px solid rgba(239,232,216,0.8); border-radius: 18px; font-family: 'Archivo Black'; font-size: 52px;
      color: {INK}; opacity: 0; }}
    .fcw {{ position: absolute; left: 0; right: 0; top: 1170px; display: flex; justify-content: center; }}
    .fc {{ display: flex; align-items: center; gap: 18px; padding: 12px 34px 14px 14px; border-radius: 60px; border: 3px solid rgba(239,232,216,0.7);
      background: rgba(20,17,20,0.7); font-family: 'Archivo Black'; font-size: 44px; color: {INK}; opacity: 0; }}
    .fc b {{ width: 64px; height: 64px; border-radius: 50%; border: 3px solid {INK}; display: flex; align-items: center; justify-content: center; font-size: 46px; line-height: 1; }}""")

# ---------------------------------------------------------------- loop: do preto, o gancho volta (clipe invertido) até o quadro 0, com o mesmo título
FULL = TOTAL - 48.0
scene("rebobina", f"""
{fvw("s7-vw", "s7-v", "gancho_volta.mp4", 0, FULL, round(1.0 / FULL, 4))}
    <div class="gb"></div>
    <div id="s7-black" class="dim" style="opacity:1"></div>
    <div id="s7-t" class="clip" data-start="0.5" data-duration="{f(FULL - 0.5)}">
      {hook_html("s7")}
    </div>
""", """
    tl.fromTo("#s7-black", { opacity: 1 }, { opacity: 0, duration: 0.8, ease: "power1.inOut" }, 0);
    tl.fromTo("#s7-t > div", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power2.out", stagger: 0.07 }, 0.5);
""")

# ---------------------------------------------------------------- legendas, textura, transições e som
# SKIP: trechos em que a tipografia da cena já mostra a fala (aqui, quase tudo). alt_from: a legenda sobe para y=630 no loop.
n_caps = write_captions(WORDS, TOTAL, [(0.0, 48.0)], alt_from=48.0, alt_top=630)
write_textura(TOTAL)
write_transicoes(TOTAL, [5.0, 9.0, 17.0, 25.0, 33.0, 37.4])  # cortes em tempo GLOBAL (nenhum no final calmo)
SFX = [  # (id, arquivo, tempo GLOBAL, volume): pop nas palavras, whoosh nos cortes, impacto só nos momentos fortes
    ("x-c1", "whoosh", 4.87, 0.4), ("x-3", "pop", 5.28, 0.45), ("x-pior", "impact-bass-1", 7.58, 0.26), ("x-c2", "whoosh", 8.87, 0.4),
    ("x-n", "impact-bass-1", 11.68, 0.26), ("x-c3", "whoosh", 16.87, 0.4), ("x-c4", "whoosh", 24.87, 0.4), ("x-choque", "glitch-1", 28.78, 0.22),
    ("x-boom", "impact-bass-1", 32.98, 0.4), ("x-subida", "riser", 29.2, 0.07), ("x-12k", "impact-bass-1", 39.18, 0.32),
]
write_index(TOTAL, SCENES, SFX, TOTAL - 0.2, 0.1, handle=HANDLE)
print(f"ok: {n_caps} grupos de legenda, {len(SCENES)} cenas, duração {TOTAL}s")
