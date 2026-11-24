"""驗證 Day11～15 並更新影片播放入口。"""
from pathlib import Path
import json
from verify_day01_04 import run

if __name__=='__main__':
 episodes=json.loads((Path(__file__).resolve().parent/'episodes11-15.json').read_text(encoding='utf-8'))
 run(episodes=episodes,batch_key='DAY11_15',label='Day 11～15',date='2026-11-23',teaching_note='Day14 的1,000→1,200及200→400萬元為教學假設，年增率為20%與100%；不代表分級或准駁門檻。本批不以單一差異或比率直接認定舞弊或還款能力。')
