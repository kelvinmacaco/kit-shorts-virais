"""Peças comuns dos Shorts (HyperFrames, fita VHS/CRT).

Uso nas cenas: from lib_short import *; init(pasta_video)

A marca @ do canal NUNCA vem fixa: pergunte ao criador qual @ usar e passe em write_index(..., handle="@...").
A marca fica sempre logo abaixo da faixa da legenda (WM_TOP), então nunca a sobrepõe.
"""
import html
import json
import math
import random
import re
from pathlib import Path

from PIL import Image

INK = "#EFE8D8"
AMBER = "#FFC21A"
CYAN = "#63D5E8"
RED = "#FF3B3B"
GROUND = "#141114"

# faixa da legenda palavra a palavra e, logo abaixo dela, a marca @ (nunca se sobrepõem)
CAP_TOP, CAP_H = 1168, 124
WM_TOP, WM_H = CAP_TOP + CAP_H + 14, 36
assert WM_TOP >= CAP_TOP + CAP_H, "a marca @ não pode sobrepor a legenda"

PROJ = None
COMPS = None


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def init(proj):
    global PROJ, COMPS
    PROJ = Path(proj)
    COMPS = PROJ / "compositions"
    COMPS.mkdir(exist_ok=True)
    rnd = random.Random(11)
    grain = Image.new("L", (512, 512))
    grain.putdata([rnd.randint(0, 255) for _ in range(512 * 512)])
    grain.save(PROJ / "assets" / "grain.png")


BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .cam {{ position: absolute; inset: 0; }}
    .tvw {{ position: absolute; left: 40px; top: 420px; width: 1000px; height: 750px; }}
    .tv {{ position: absolute; left: 0; top: 0; display: block; width: 1000px; height: 750px; object-fit: cover;
      border: 5px solid {INK}; border-radius: 26px; box-shadow: 0 26px 70px rgba(0,0,0,0.65); }}
    .fvw {{ position: absolute; inset: 0; }}
    .fv {{ position: absolute; left: 0; top: 0; display: block; width: 1080px; height: 1920px; object-fit: cover; }}
    .gt {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(20,17,20,0.8) 0%, rgba(20,17,20,0) 30%); }}
    .gb {{ position: absolute; inset: 0;
      background: linear-gradient(180deg, rgba(20,17,20,0.55) 0%, rgba(20,17,20,0) 18%, rgba(20,17,20,0) 38%, rgba(20,17,20,0.82) 52%, rgba(20,17,20,0.95) 100%); }}
    .dim {{ position: absolute; inset: 0; background: {GROUND}; }}
    .kt {{ position: absolute; left: 0; right: 0; text-align: center; font-family: 'Archivo Black'; color: {INK};
      line-height: 1.06; white-space: nowrap; text-shadow: 0 6px 0 rgba(0,0,0,0.5); }}
    .kt span {{ display: inline-block; margin: 0 0.12em; opacity: 0; }}
    .am {{ color: {AMBER}; }}
    .rd {{ color: {RED}; }}
    .lbl {{ position: absolute; left: 0; right: 0; top: 270px; text-align: center; font-family: 'Archivo Black';
      font-size: 120px; line-height: 1.02; color: {INK}; white-space: nowrap; text-shadow: 0 6px 0 rgba(0,0,0,0.55); }}
    .mono {{ position: absolute; left: 0; right: 0; text-align: center; font-family: 'Space Mono'; font-size: 32px;
      letter-spacing: 0.14em; color: {AMBER}; white-space: nowrap; text-shadow: 0 2px 8px rgba(0,0,0,0.8); }}
    .big {{ position: absolute; left: 0; right: 0; text-align: center; font-family: 'Archivo Black'; line-height: 1;
      color: {AMBER}; white-space: nowrap; text-shadow: 0 14px 0 rgba(0,0,0,0.45); }}
    .draw {{ fill: none; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }}
"""


def scene(cid, body, js, extra_css=""):
    (COMPS / f"{cid}.html").write_text(f"""<template>
  <style>{BASE_CSS}{extra_css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
""", encoding="utf-8")


def fv(vid, src, start, dur, rate=None, mstart=None):
    r = f' data-playback-rate="{rate}"' if rate else ""
    m = f' data-media-start="{f(mstart)}"' if mstart else ""
    return f'<video id="{vid}" class="clip fv" src="assets/video/{src}" data-start="{f(start)}" data-duration="{f(dur)}"{r}{m} muted playsinline></video>'


def fvw(wid, vid, src, start, dur, rate=None, mstart=None):
    return f'    <div id="{wid}" class="fvw">{fv(vid, src, start, dur, rate, mstart)}</div>'


def tvv(vid, src, start, dur, rate=None):
    r = f' data-playback-rate="{rate}"' if rate else ""
    return f'<video id="{vid}" class="clip tv" src="assets/video/{src}" data-start="{f(start)}" data-duration="{f(dur)}"{r} muted playsinline></video>'


def words_js(items, dur=0.14):
    return "\n".join(
        f'    tl.fromTo("{s}", {{ opacity: 0, filter: "blur(8px)", scale: 1.2 }}, {{ opacity: 1, filter: "blur(0px)", scale: 1, duration: {dur}, ease: "expo.out" }}, {f(t)});'
        for s, t in items)


def kline(prefix, words, top, size, start_index=0):
    spans = "".join(f'<span id="{prefix}{start_index + k}" class="{c}">{w}</span>' for k, (w, c) in enumerate(words))
    return f'<div class="kt" style="top:{top}px; font-size:{size}px">{spans}</div>'


def punch(sel, t, s, origin="540px 760px"):
    return f'    tl.set("{sel}", {{ scale: {s}, transformOrigin: "{origin}" }}, {f(t)});'


def shake(sel, t, amp=14):
    pts = [(amp, -amp * 0.6), (-amp * 0.75, amp * 0.5), (amp * 0.45, amp * 0.3), (0, 0)]
    return "\n".join(f'    tl.set("{sel}", {{ x: {f(x)}, y: {f(y)} }}, {f(t + n * 0.033)});' for n, (x, y) in enumerate(pts))


def slam(sel, t, frm=2.0):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, scale: {frm} }}, {{ opacity: 1, scale: 1, duration: 0.16, ease: "expo.out" }}, {f(t)});'


def fade_in(sel, t):
    return f'    tl.fromTo("{sel}", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "expo.out" }}, {f(t)});'


def enter_tv(sel, t):
    return f'    tl.fromTo("{sel}", {{ scale: 0.94, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.22, ease: "expo.out" }}, {f(t)});'


def zoom_in(sel, t, dur=0.55):
    return f'    tl.fromTo("{sel}", {{ scale: 1.14 }}, {{ scale: 1, transformOrigin: "540px 900px", duration: {dur}, ease: "expo.out" }}, {f(t)});'


def label(lid, text, start, end, top=270, size=120, cls=""):
    return f'    <div id="{lid}" class="clip lbl {cls}" data-start="{f(start)}" data-duration="{f(end - start)}" style="top:{top}px; font-size:{size}px"><div id="{lid}-i">{text}</div></div>'


def lbl_in(lid, t):
    return slam(f"#{lid}-i", t, 1.6)


HEART = ("M300 520 C 120 390 40 290 40 190 C 40 110 105 50 180 50 C 230 50 275 80 300 120 "
         "C 325 80 370 50 420 50 C 495 50 560 110 560 190 C 560 290 480 390 300 520 Z")
BURST = "".join(
    f'<path d="M {f(300 + 300 * math.cos(a))} {f(290 + 300 * math.sin(a))} L {f(300 + 370 * math.cos(a))} {f(290 + 370 * math.sin(a))}" stroke="{AMBER}" stroke-width="12" stroke-linecap="round"/>'
    for a in [2 * math.pi * k / 10 for k in range(10)])
PLANE = "M40 300 L560 80 L420 520 L300 380 L200 470 L220 340 Z M220 340 L560 80"


def like_block(pid, start, dur, words, t_like):
    """Coração que enche no "like". words = [(palavra, classe, t)]."""
    spans = "".join(f'<span id="{pid}-l{k}" class="{c}">{w}</span>' for k, (w, c, _) in enumerate(words))
    body = f"""    <div id="{pid}" class="clip" data-start="{f(start)}" data-duration="{f(dur)}" data-layout-allow-overlap>
      <div id="{pid}-hw" style="position:absolute; left:300px; top:330px; width:480px; height:448px">
        <svg viewBox="0 0 600 560" style="width:100%;height:100%;overflow:visible">
          <g id="{pid}-burst" opacity="0">{BURST}</g>
          <path id="{pid}-heart" d="{HEART}" fill="none" stroke="{INK}" stroke-width="16" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="kt" style="top:880px; font-size:88px">{spans}</div>
    </div>"""
    js = f"""    tl.fromTo("#{pid}-hw", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }}, {f(start + 0.08)});
{words_js([(f"#{pid}-l{k}", t) for k, (_, _, t) in enumerate(words)])}
    tl.set("#{pid}-heart", {{ attr: {{ fill: "{RED}", stroke: "{RED}" }} }}, {f(t_like)});
    tl.fromTo("#{pid}-hw", {{ scale: 1.35 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2.5)", immediateRender: false }}, {f(t_like)});
    tl.fromTo("#{pid}-burst", {{ opacity: 1, scale: 0.7, svgOrigin: "300 290" }}, {{ opacity: 0, scale: 1.35, svgOrigin: "300 290", duration: 0.45, ease: "power2.out", immediateRender: false }}, {f(t_like)});"""
    return body, js


def plane_svg(pid, left=780, top=180, size=200):
    return (f'<div id="{pid}" style="position:absolute; left:{left}px; top:{top}px; width:{size}px; height:{size}px">'
            f'<svg viewBox="0 0 600 600" style="width:100%;height:100%;overflow:visible"><path d="{PLANE}" fill="none" stroke="{INK}" stroke-width="30" stroke-linejoin="round"/></svg></div>')


def plane_js(pid, t, hold=3.0):
    return (f'    tl.fromTo("#{pid}", {{ x: -760, y: 260, rotation: -30, opacity: 0 }}, {{ x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.5, ease: "expo.out" }}, {f(t)});\n'
            f'    tl.to("#{pid}", {{ x: 20, y: -16, duration: {hold}, ease: "sine.inOut" }}, {f(t + 0.55)});')


def osd_rewind(pid, start, dur):
    body = (f'    <div id="{pid}" class="clip mono" data-start="{f(start)}" data-duration="{f(dur)}" style="top:214px; font-size:40px; color:{INK}"><span id="{pid}-in" style="display:inline-block">'
            f'<svg viewBox="0 0 64 34" style="width:64px;height:34px;vertical-align:-4px;margin-right:18px"><polygon points="32,0 32,34 0,17" fill="{INK}"/><polygon points="64,0 64,34 32,17" fill="{INK}"/></svg>REBOBINANDO</span></div>')
    n = int(dur / 0.2)
    js = "\n".join(f'    tl.set("#{pid}-in", {{ opacity: {1 if k % 2 == 0 else 0.25} }}, {f(start + k * 0.2)});' for k in range(n))
    return body, js


# ---------------------------------------------------------------- retenção e seguidores (ver RETENTION_GUIDE.md)
BUBBLE = "M60 40 H540 a40 40 0 0 1 40 40 V330 a40 40 0 0 1 -40 40 H250 L140 470 V370 H60 a40 40 0 0 1 -40 -40 V80 a40 40 0 0 1 40 -40 Z"


def step_badge(pid, start, dur, n, total, left=70, top=200):
    """Etiqueta "1/4" no canto de cima: mostra em que item da lista a pessoa está."""
    body = (f'    <div id="{pid}" class="clip" data-start="{f(start)}" data-duration="{f(dur)}" data-layout-allow-overlap>'
            f'<div id="{pid}-i" style="position:absolute; left:{left}px; top:{top}px; padding:8px 22px 10px; border-radius:16px; '
            f'background:{AMBER}; color:{GROUND}; font-family:\'Archivo Black\'; font-size:48px; line-height:1; '
            f'box-shadow:0 8px 24px rgba(0,0,0,0.5)">{n}<span style="font-size:30px; opacity:0.7">/{total}</span></div></div>')
    js = f'    tl.fromTo("#{pid}-i", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, transformOrigin: "0% 50%", duration: 0.25, ease: "back.out(2.4)" }}, {f(start)});'
    return body, js


def comment_card(pid, start, dur, pergunta, opcoes=("SIM", "NÃO"), top=500):
    """Pergunta para comentar (perto de 60% do vídeo): balão, pergunta e duas opções na tela."""
    ops = "".join(
        f'<div id="{pid}-o{k}" style="padding:12px 46px 16px; border:5px solid {INK}; border-radius:20px; background:rgba(20,17,20,0.65); '
        f'font-family:\'Archivo Black\'; font-size:64px; line-height:1; color:{AMBER if k == 0 else INK}">{o}</div>'
        for k, o in enumerate(opcoes))
    body = f"""    <div id="{pid}" class="clip" data-start="{f(start)}" data-duration="{f(dur)}" data-layout-allow-overlap>
      <div id="{pid}-w" style="position:absolute; left:110px; top:{top}px; width:860px">
        <div style="display:flex; align-items:center; justify-content:center; gap:22px">
          <svg viewBox="0 0 600 480" style="width:84px;height:68px"><path d="{BUBBLE}" fill="{AMBER}"/></svg>
          <span style="font-family:'Space Mono'; font-weight:700; font-size:38px; letter-spacing:0.12em; color:{AMBER}">COMENTA:</span>
        </div>
        <div style="margin-top:18px; text-align:center; font-family:'Archivo Black'; font-size:76px; line-height:1.05; color:{INK};
          text-shadow:0 6px 0 rgba(0,0,0,0.5)">{pergunta}</div>
        <div style="display:flex; justify-content:center; gap:40px; margin-top:34px">{ops}</div>
      </div>
    </div>"""
    js = "\n".join([
        f'    tl.fromTo("#{pid}-w", {{ y: 70, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.8)" }}, {f(start)});',
        *(slam(f"#{pid}-o{k}", start + 0.35 + 0.15 * k, 1.8) for k in range(len(opcoes))),
        f'    tl.to("#{pid}-o0", {{ scale: 1.1, duration: 0.22, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {f(start + 1.0)});',
    ])
    return body, js


def follow_card(pid, start, dur, texto="SEGUE PRA PARTE 2", top=1010):
    """Botão de seguir (+) com o motivo para seguir. Precisa sumir antes do rebobinar do loop."""
    body = f"""    <div id="{pid}" class="clip" data-start="{f(start)}" data-duration="{f(dur)}" data-layout-allow-overlap>
      <div style="position:absolute; left:0; right:0; top:{top}px; display:flex; justify-content:center">
        <div id="{pid}-w" style="display:flex; align-items:center; gap:22px; padding:14px 38px 14px 16px; border-radius:60px;
          background:{INK}; box-shadow:0 14px 40px rgba(0,0,0,0.55)">
          <div id="{pid}-plus" style="width:84px; height:84px; border-radius:50%; background:{RED}; display:flex; align-items:center; justify-content:center">
            <svg viewBox="0 0 40 40" style="width:44px;height:44px"><path d="M20 6 V34 M6 20 H34" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>
          </div>
          <span style="font-family:'Archivo Black'; font-size:50px; line-height:1; color:{GROUND}; white-space:nowrap">{texto}</span>
        </div>
      </div>
    </div>"""
    js = "\n".join([
        f'    tl.fromTo("#{pid}-w", {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, {f(start)});',
        f'    tl.fromTo("#{pid}-plus", {{ rotation: -180 }}, {{ rotation: 0, duration: 0.45, ease: "back.out(1.6)" }}, {f(start + 0.1)});',
        f'    tl.to("#{pid}-w", {{ scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {f(start + 0.9)});',
    ])
    return body, js


def pavio_scene(t0, fim, keys, lit, boom, notches=(330, 610, 890), x0=120, x1=975):
    """Pavio aceso no topo da tela: indicador de progresso temático (no lugar de "1/3, 2/3, 3/3").

    t0/fim: início e fim da cena em tempo global (a mesma entrada de SCENES; ponha "pavio" depois das
    cenas que ele cobre, para ficar por cima). keys: [(t_global, x)] da faísca, do início até a bomba.
    lit: [t_global] em que cada marca acende. boom: t_global em que a faísca chega à bomba e explode.
    Retorna (body, js, css) para scene("pavio", body, js, css).
    """
    segs = []
    for (ta, xa), (tb, xb) in zip(keys, keys[1:]):
        ease = "none" if tb - ta > 2 else "power2.in"
        segs.append(f'    tl.fromTo("#pv-sp", {{ x: {xa - x0} }}, {{ x: {xb - x0}, duration: {f(tb - ta)}, ease: "{ease}", immediateRender: false }}, {f(ta - t0)});')
        segs.append(f'    tl.fromTo("#pv-burn", {{ width: {xa - x0} }}, {{ width: {min(xb, x1) - x0}, duration: {f(tb - ta)}, ease: "{ease}", immediateRender: false }}, {f(ta - t0)});')
    lits = [f'    tl.set("#pv-n{k}", {{ background: "{RED}", borderColor: "{RED}" }}, {f(t - t0)});\n'
            f'    tl.fromTo("#pv-n{k}", {{ scale: 1.8 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, {f(t - t0)});\n'
            f'    tl.set("#pv-t{k}", {{ color: "{RED}" }}, {f(t - t0)});' for k, t in enumerate(lit)]
    n = max(1, int((fim - t0) / 0.07))
    bomb = (f'<svg viewBox="0 0 100 100" style="width:100%;height:100%;overflow:visible"><circle cx="46" cy="58" r="36" fill="#1b1719" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="58" y="14" width="22" height="16" rx="3" fill="#1b1719" stroke="{INK}" stroke-width="4" transform="rotate(35 69 22)"/>'
            f'<circle cx="34" cy="46" r="8" fill="rgba(239,232,216,0.35)"/></svg>')
    marks = "".join(f'<div id="pv-n{k}" class="notch" style="left:{x - 12}px"></div><div id="pv-t{k}" class="ntxt" style="left:{x - 30}px">{k + 1}</div>'
                    for k, x in enumerate(notches))
    body = f"""    <div id="pv" style="position:absolute; inset:0">
      <div class="rope"></div>
      <div id="pv-burn" class="burn"></div>
      {marks}
      <div id="pv-bomb" class="bomb">{bomb}</div>
      <div id="pv-sp" class="spark"><i></i><b class="p1"></b><b class="p2"></b><b class="p3"></b></div>
      <div id="pv-ring" class="ring"></div>
    </div>
    <div id="pv-flash" class="flash"></div>"""
    js = "\n".join([
        '    tl.fromTo("#pv", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 0);',
        '    tl.fromTo("#pv-sp", { scale: 0 }, { scale: 1.4, duration: 0.25, ease: "back.out(3)" }, 0);',
        f'    tl.to("#pv-sp i", {{ scale: 1.35, opacity: 0.75, duration: 0.07, yoyo: true, repeat: {n}, ease: "none" }}, 0.25);',
        f'    tl.to("#pv-sp .p1", {{ x: -22, y: -26, opacity: 0, duration: 0.3, repeat: {int(n * 0.07 / 0.3)}, ease: "power1.out" }}, 0.25);',
        f'    tl.to("#pv-sp .p2", {{ x: 18, y: -30, opacity: 0, duration: 0.37, repeat: {int(n * 0.07 / 0.37)}, ease: "power1.out" }}, 0.3);',
        f'    tl.to("#pv-sp .p3", {{ x: -6, y: 24, opacity: 0, duration: 0.33, repeat: {int(n * 0.07 / 0.33)}, ease: "power1.out" }}, 0.35);',
        *segs, *lits,
        f'    tl.to("#pv-bomb", {{ x: 6, duration: 0.05, yoyo: true, repeat: 15, ease: "none" }}, {f(boom - 1.3 - t0)});',
        f'    tl.to("#pv-bomb", {{ scale: 2.6, opacity: 0, duration: 0.35, ease: "power2.out" }}, {f(boom - t0)});',
        f'    tl.to("#pv-sp", {{ opacity: 0, duration: 0.1 }}, {f(boom - t0)});',
        f'    tl.fromTo("#pv-ring", {{ scale: 0.2, opacity: 1 }}, {{ scale: 9, opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }}, {f(boom - t0)});',
        f'    tl.fromTo("#pv-flash", {{ opacity: 0.9 }}, {{ opacity: 0, duration: 0.55, ease: "power2.out", immediateRender: false }}, {f(boom - t0)});',
        f'    tl.to("#pv", {{ opacity: 0, duration: 0.25 }}, {f(fim - 0.3 - t0)});',
    ])
    css = f"""
    .rope {{ position: absolute; left: {x0}px; top: 211px; width: {x1 - x0}px; height: 8px; border-radius: 4px;
      background: repeating-linear-gradient(90deg, #b39e74 0 14px, #7d6d50 14px 20px); box-shadow: 0 2px 8px rgba(0,0,0,0.7); }}
    .burn {{ position: absolute; left: {x0}px; top: 211px; width: 0; height: 8px; border-radius: 4px; background: #1d1917; }}
    .notch {{ position: absolute; top: 203px; width: 24px; height: 24px; border-radius: 50%; border: 4px solid {INK}; background: {GROUND}; }}
    .ntxt {{ position: absolute; top: 232px; width: 60px; text-align: center; font-family: 'Space Mono'; font-weight: 700; font-size: 24px; color: {INK};
      text-shadow: 0 2px 6px rgba(0,0,0,0.9); }}
    .bomb {{ position: absolute; left: {x1 - 8}px; top: 170px; width: 84px; height: 84px; }}
    .spark {{ position: absolute; left: {x0 - 26}px; top: 189px; width: 52px; height: 52px; }}
    .spark i {{ position: absolute; inset: 0; border-radius: 50%; background: radial-gradient(circle, #fff 0%, {AMBER} 35%, rgba(255,120,30,0.6) 55%, rgba(255,59,59,0) 72%); }}
    .spark b {{ position: absolute; left: 22px; top: 22px; width: 8px; height: 8px; border-radius: 50%; background: {AMBER}; box-shadow: 0 0 8px {AMBER}; }}
    .ring {{ position: absolute; left: {x1 - 10}px; top: 172px; width: 80px; height: 80px; border-radius: 50%; border: 8px solid {AMBER}; opacity: 0; }}
    .flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; }}"""
    return body, js, css


# ---------------------------------------------------------------- legendas
NUM_FIX = [
    (r"R\$(\d+)\.000,00", r"R$ \1 MIL"),
    (r"R\$(\d+)\.(\d{3}),00", r"R$ \1.\2"),
    (r"R\$(\d+)\.00", r"R$ \1 MIL"),
]


def load_words(words_json):
    raw = json.loads(Path(words_json).read_text(encoding="utf-8"))["word_timestamps"]
    words = [{"t": w["word"].strip(), "s": float(w["start"]), "e": float(w["end"])} for w in raw]
    merged = []
    for w in words:  # o whisper quebra "R" "$" "10" ".000" ",00" e "matéria" "-prima"
        glue = merged and (w["t"][:1] in ".,$-" or merged[-1]["t"].endswith("$"))
        if glue:
            merged[-1]["t"] += w["t"]
            merged[-1]["e"] = w["e"]
        else:
            merged.append(dict(w))
    for w in merged:
        t = w["t"].replace("...", "…")
        for pat, rep in NUM_FIX:
            t = re.sub(pat, rep, t)
        w["t"] = t.rstrip(",") if "R$" in t else t
    return merged


def write_captions(words_json, total, skip, alt_from=None, alt_top=790):
    words = load_words(words_json)

    def skipped(w):
        return any(a <= w["s"] < b for a, b in skip)

    groups, cur = [], []
    for w in words:
        if skipped(w) or w["s"] >= total - 0.1:
            if cur:
                groups.append(cur)
                cur = []
            continue
        if cur:
            prev = cur[-1]
            chars = sum(len(x["t"]) + 1 for x in cur) + len(w["t"])
            if prev["t"][-1:] in ".,?!:…" or w["s"] - prev["e"] >= 0.15 or len(cur) >= 3 or chars > 17:
                groups.append(cur)
                cur = []
        cur.append(w)
    if cur:
        groups.append(cur)

    def show(t):
        t = t.upper()
        return t[:-1] if t[-1:] in ".," else t

    cap_html, cap_js = [], []
    prev_end, wi = 0.0, 0
    for gi, g in enumerate(groups):
        start = max(g[0]["s"] - 0.06, prev_end + 0.02)
        nxt = groups[gi + 1][0]["s"] - 0.06 if gi + 1 < len(groups) else total - 0.05
        end = max(min(g[-1]["e"] + 0.22, nxt - 0.02, total - 0.05), start + 0.3)
        prev_end = end
        text = " ".join(show(w["t"]) for w in g)
        fs = max(54, min(78, int(880 / (0.68 * len(text)))))
        alt = alt_from is not None and start >= alt_from
        if alt:
            fs = min(fs, 46)
        spans = []
        for k, w in enumerate(g):
            wid = f"cap-w{wi}"
            wi += 1
            spans.append(f'<span class="w" id="{wid}">{show(w["t"])}</span>')
            on = max(w["s"], start)
            off = g[k + 1]["s"] if k + 1 < len(g) else end
            cap_js.append(f'    tl.set("#{wid}", {{ color: "{AMBER}" }}, {f(on)});')
            cap_js.append(f'    tl.fromTo("#{wid}", {{ scale: 1.2 }}, {{ scale: 1, duration: 0.18, ease: "expo.out", immediateRender: false }}, {f(on)});')
            cap_js.append(f'    tl.set("#{wid}", {{ color: "{INK}" }}, {f(off)});')
        gid = f"cap-g{gi}"
        cap_html.append(f'    <div id="{gid}" class="clip cap{" cap-alt" if alt else ""}" data-start="{f(start)}" data-duration="{f(end - start)}">'
                        f'<div class="cap-in" id="{gid}-in" style="font-size:{fs}px">{"".join(spans)}</div></div>')
        cap_js.append(f'    tl.fromTo("#{gid}-in", {{ opacity: 0, scale: 0.9, filter: "blur(6px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.13, ease: "expo.out" }}, {f(start)});')
        cap_js.append(f'    tl.to("#{gid}-in", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {f(end - 0.1)});')
        cap_js.append(f'    tl.set("#{gid}-in", {{ opacity: 0 }}, {f(end)});')
    (COMPS / "legendas.html").write_text(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .cap {{ position: absolute; left: 0; right: 0; top: {CAP_TOP}px; height: {CAP_H}px; display: flex;
      align-items: center; justify-content: center; text-align: center; overflow: visible; }}
    .cap-alt {{ top: {alt_top}px; height: 80px; }}
    .cap-in {{ font-family: 'Inter'; font-weight: 900; text-transform: uppercase; color: {INK};
      letter-spacing: -0.01em; line-height: 1; white-space: nowrap;
      text-shadow: 0 5px 0 rgba(0,0,0,0.55), 0 0 24px rgba(0,0,0,0.65); }}
    .w {{ display: inline-block; margin: 0 0.16em; }}
  </style>
  <div id="root" data-composition-id="legendas" data-width="1080" data-height="1920">
{chr(10).join(cap_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cap_js)}
    window.__timelines["legendas"] = tl;
  </script>
</template>
""", encoding="utf-8")
    return len(groups)


def write_textura(total):
    (COMPS / "textura.html").write_text(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
    #tx-grain {{ position: absolute; left: 0; top: 0; width: 1340px; height: 2180px; opacity: 0.07;
      background: url(assets/grain.png) repeat; background-size: 256px; mix-blend-mode: overlay; }}
    #tx-scan {{ position: absolute; inset: 0;
      background: repeating-linear-gradient(0deg, rgba(255,255,255,0.035) 0 2px, transparent 2px 4px); }}
  </style>
  <div id="root" data-composition-id="textura" data-width="1080" data-height="1920">
    <div id="tx-fita" class="clip" data-start="0" data-duration="{f(total)}" data-layout-ignore>
      <div id="tx-grain"></div>
      <div id="tx-scan"></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    let seed = 3;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < {math.ceil(total * 15)}; i++) {{
      tl.set("#tx-grain", {{ x: -Math.floor(rnd() * 256), y: -Math.floor(rnd() * 256) }}, i / 15);
    }}
    window.__timelines["textura"] = tl;
  </script>
</template>
""", encoding="utf-8")


def write_transicoes(total, cuts):
    tr = random.Random(33)
    js = []
    for t in cuts:
        by, ly = tr.randint(260, 1500), tr.randint(200, 1700)
        js.append(f'    tl.set("#tr-band", {{ y: {by}, x: {tr.randint(-40, 40)}, opacity: 0.4 }}, {f(t - 0.05)});')
        js.append(f'    tl.to("#tr-band", {{ y: {by + tr.randint(120, 260)}, opacity: 0, duration: 0.2, ease: "none" }}, {f(t - 0.05)});')
        js.append(f'    tl.set("#tr-line", {{ y: {ly}, opacity: 0.75 }}, {f(t)});')
        js.append(f'    tl.to("#tr-line", {{ opacity: 0, duration: 0.1, ease: "none" }}, {f(t + 0.03)});')
        js.append(f'    tl.fromTo("#tr-flash", {{ opacity: 0.13 }}, {{ opacity: 0, duration: 0.12, ease: "power2.out", immediateRender: false }}, {f(t)});')
    (COMPS / "transicoes.html").write_text(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; }}
    #tr-band {{ position: absolute; left: -60px; right: -60px; top: 0; height: 170px; opacity: 0;
      background: url(assets/grain.png) repeat; background-size: 200px; mix-blend-mode: screen;
      filter: contrast(2.6) brightness(0.9);
      -webkit-mask-image: linear-gradient(180deg, transparent, #000 30%, #000 70%, transparent);
      mask-image: linear-gradient(180deg, transparent, #000 30%, #000 70%, transparent); }}
    #tr-line {{ position: absolute; left: 0; right: 0; top: 0; height: 4px; opacity: 0;
      background: linear-gradient(90deg, {RED}, {INK} 40%, {CYAN}); }}
    #tr-flash {{ position: absolute; inset: 0; background: {INK}; opacity: 0; }}
  </style>
  <div id="root" data-composition-id="transicoes" data-width="1080" data-height="1920">
    <div id="tr-fita" class="clip" data-start="0" data-duration="{f(total)}" data-layout-ignore>
      <div id="tr-band"></div><div id="tr-line"></div><div id="tr-flash"></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["transicoes"] = tl;
  </script>
</template>
""", encoding="utf-8")


SFX_DUR = {"glitch-1": 2.638, "glitch-3": 3.096, "whoosh": 0.575, "whoosh-short": 0.575, "pop": 0.72,
           "impact-bass-1": 2.116, "riser": 10.032, "rewind": 5.544, "sparkle": 1.8}


def write_index(total, scenes, sfx, voice_dur, music_vol=0.1, handle=None):
    """Monta o index.html. `handle` é o @ do canal: pergunte ao criador qual usar (nunca invente nem use um padrão)."""
    if not handle or not str(handle).startswith("@") or "SEU_CANAL" in str(handle):
        raise ValueError('Falta o @ do canal: pergunte ao criador qual @ usar e passe handle="@...".')
    h = html.escape(str(handle), quote=True)
    hosts = []
    for z, (cid, a, b) in enumerate(scenes, start=2):
        hosts.append(f'<div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                     f'data-start="{f(a)}" data-duration="{f(min(b, total) - a)}" data-track-index="{z}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920" style="z-index:{z}"></div>')
    audio = [
        f'<audio id="voz" class="clip" src="assets/audio/narracao.mp3" data-start="0" data-duration="{f(min(total, voice_dur))}" data-track-index="20" data-volume="1"></audio>',
        f'<audio id="trilha" class="clip" src="assets/audio/musica.mp3" data-start="0" data-duration="{f(total)}" data-track-index="21" data-volume="{music_vol}" data-fade-in="0.2" data-fade-out="0.3"></audio>',
    ]
    for k, (aid, name, at, vol) in enumerate(sfx):
        dur = min(SFX_DUR[name], total - at)
        audio.append(f'<audio id="{aid}" class="clip" src="assets/sfx/{name}.mp3" data-start="{f(at)}" data-duration="{f(dur)}" '
                     f'data-track-index="{22 + k}" data-volume="{vol}"></audio>')
    (PROJ / "index.html").write_text(f"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait"
  data-composition-variables='[{{"id":"handle","type":"string","label":"Marca d&#39;água","default":"{h}"}}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {GROUND}; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      #bg {{ position: absolute; inset: 0; z-index: 0;
        background: radial-gradient(ellipse 75% 60% at 50% 45%, #1c181c 0%, {GROUND} 60%, #09070a 100%); }}
      #watermark {{ position: absolute; left: 0; right: 0; top: {WM_TOP}px; height: {WM_H}px; z-index: 40;
        text-align: center; font-family: 'Inter'; font-weight: 700; font-size: 30px; line-height: 36px;
        letter-spacing: 0.02em; color: rgba(255,255,255,0.24); white-space: nowrap; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f(total)}" data-width="1080" data-height="1920" data-fps="30">
      <div id="bg"></div>
      {chr(10).join("      " + h for h in hosts).strip()}
      <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{f(total)}" data-track-index="10" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:30"></div>
      <div id="transicoes" data-composition-id="transicoes" data-composition-src="compositions/transicoes.html" data-start="0" data-duration="{f(total)}" data-track-index="12" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:26"></div>
      <div id="textura" data-composition-id="textura" data-composition-src="compositions/textura.html" data-start="0" data-duration="{f(total)}" data-track-index="9" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:25"></div>
      <div id="watermark" class="clip" data-start="0" data-duration="{f(total)}" data-track-index="11" data-var-text="handle" data-layout-allow-overlap data-layout-allow-occlusion>{h}</div>
      {chr(10).join("      " + a for a in audio).strip()}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
""", encoding="utf-8")
