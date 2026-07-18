from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.database import list_tables_and_views, read_query

EXPORT_DIR = ROOT / "data" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

for name in list_tables_and_views()["name"]:
    frame = read_query(f'SELECT * FROM "{name}"')
    frame.to_csv(EXPORT_DIR / f"{name}.csv", index=False)
    print(f"Exported {name}: {len(frame):,} rows")
