import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parents[1]/"content/plan/content-plan.json").read_text(encoding="utf-8"))
core=sum(len(v) for v in p["core_library"].values())
assert core==155,(core,"core post count mismatch")
assert len(p["challenge_30_days"])==30
assert len(p["year_practice_52_weeks"])==52
assert len(p["canonical_labels"])==16
print(f"Content plan OK: {core} core + 30 challenge + 52 weekly = {core+30+52} planned items.")
