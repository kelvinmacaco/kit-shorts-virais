import json
import sys

sys.path.insert(0, ".")
from tools.analysis.transcriber import Transcriber

entrada, saida_dir, saida_json = sys.argv[1], sys.argv[2], sys.argv[3]
modelo = sys.argv[4] if len(sys.argv) > 4 else "medium"

r = Transcriber().execute({
    "input_path": entrada,
    "model_size": modelo,
    "language": "pt",
    "output_dir": saida_dir,
})
print("OK" if r.success else "ERRO", r.error)
d = r.data or {}
with open(saida_json, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2, default=str)
for s in d.get("segments", []):
    print(f"[{s.get('start', 0):6.2f}-{s.get('end', 0):6.2f}] {s.get('text', '').strip()}")
