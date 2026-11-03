# MODELO: gera as cenas e aplica a fita VHS em toda filmagem real.
# Antes de rodar, preencha ..\kit.json (copiado de kit.example.json): caminhos e o @ do canal,
# que deve ser perguntado ao criador. Ajuste a lista $alvos às cenas do generate.py.
# Rodar:  powershell -ExecutionPolicy Bypass -File build\build.ps1 -Duracao 49.5
# NUNCA passe a saída por "| Select-Object -First ...": isso interrompe o script e o VHS não é aplicado.
param([double]$Duracao = 49.5)
$ErrorActionPreference = "Continue"
$proj = Split-Path -Parent $PSScriptRoot
$cfg = Get-Content "$proj\kit.json" -Raw -Encoding UTF8 | ConvertFrom-Json
if (-not $cfg.handle -or $cfg.handle -notlike "@*" -or $cfg.handle -like "*SEU_CANAL*") {
  throw "Falta o @ do canal no kit.json: pergunte ao criador qual @ usar."
}
$video = "$proj\video"
$env:Path = "$($cfg.ffmpeg_bin);" + $env:Path
Set-Location $video
& $cfg.python -X utf8 "$proj\build\generate.py" "." "$proj\assets\audio\narracao_words.json" $Duracao $cfg.handle
# tela cheia (.fv) leva listras mais finas; janelas de TV (.tv) levam a fita completa
# uma linha por cena que tem filmagem: @(cena, seletor, receita)
$alvos = @(
  @("gancho", ".fv", "vhs_full.json"), @("misterio", ".fv", "vhs_full.json"), @("item1", ".fv", "vhs_full.json"),
  @("item2", ".fv", "vhs_full.json"), @("item3", ".fv", "vhs_full.json"), @("revelacao", ".fv", "vhs_full.json"),
  @("rebobina", ".fv", "vhs_full.json")
)
foreach ($a in $alvos) {
  $r = npx --yes "hyperframes@$($cfg.hyperframes)" media-treatment --file "compositions/$($a[0]).html" --selector $a[1] --grading "$proj\build\$($a[2])" --apply --json 2>$null | Out-String
  if ($r -match '"ok":\s*true') { "VHS ok: $($a[0]) $($a[1])" } else { "VHS FALHOU: $($a[0]) $($a[1])" }
}
