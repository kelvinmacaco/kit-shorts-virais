// Busca de vídeos grátis no Pexels, para colar no console (ou javascript_tool) com uma página
// do pexels.com aberta no navegador. Ele lê o __NEXT_DATA__ da página de busca (fetch na mesma origem).
// Uso:
//   const r = []; for (const q of ['tank military', 'world map']) r.push(...await px(q, 4));
//   r.map(o => [o.q, o.id, o.t, o.dur, o.wh, o.thumb, o.file].join(' | ')).join('\n')
// Depois baixe com: curl -L -A "Mozilla/5.0" -e https://www.pexels.com/ -o arquivo.mp4 "<file>"
// Para vídeos deitados (wh 3840x2160 etc.), prefira um arquivo de 2560 ou 1920 de largura
// e corte o meio na vertical.
window.px = async (q, n = 6) => {
  const html = await (await fetch('/search/videos/' + encodeURIComponent(q) + '/?orientation=portrait')).text();
  const m = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/);
  const data = JSON.parse(m[1]).props.pageProps.initialData.data;
  return data.filter(x => x.attributes.duration >= 5).slice(0, n).map(x => {
    const a = x.attributes;
    const files = (a.video.video_files || []).filter(f => f.file_type === 'video/mp4' && f.width >= 720 && f.width <= 1440).sort((p, r) => p.width - r.width);
    const th = a.video.thumbnail;
    return { q, id: a.id, t: a.title, dur: a.duration, wh: a.width + 'x' + a.height,
      thumb: typeof th === 'string' ? th : (th && (th.small || th.medium || Object.values(th)[0])) || '',
      file: files.length ? files[files.length - 1].link : (a.video.download_link || '') };
  });
};
