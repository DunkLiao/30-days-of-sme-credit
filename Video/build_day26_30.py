"""沿用共用流程，只製作 Day26～30。"""
from pathlib import Path
import json, sys
import build_day06_10 as pipeline
ROOT=Path(__file__).resolve().parent
EPISODES=json.loads((ROOT/'episodes26_30_source.json').read_text(encoding='utf-8'))
if __name__=='__main__':
 if '--day' in sys.argv:
  day=sys.argv[sys.argv.index('--day')+1].zfill(2)
  EPISODES=[ep for ep in EPISODES if ep['day']==day]
  if not EPISODES: raise SystemExit('本批沒有指定集數')
  if '--prepare' in sys.argv: raise SystemExit('逐集修訂不得覆寫整批 manifest')
 pipeline.EPISODES=EPISODES
 pipeline.SOURCE_NOTES={ep['day']:ep['source_note'] for ep in EPISODES}
 if '--prepare' in sys.argv: pipeline.prepare('episodes26-30.json')
 else:
  pipeline.finalize()
  for ep in EPISODES:
   p=ROOT/ep['slug']/'NOTES.md'
   p.write_text(p.read_text(encoding='utf-8').replace('2026-11-23','2026-11-24'),encoding='utf-8')
   if ep['day']=='28':
    p=ROOT/ep['slug']/'index.html'
    p.write_text(p.read_text(encoding='utf-8').replace('</style>','.question-scene .quiet{margin-top:0}</style>'),encoding='utf-8')
