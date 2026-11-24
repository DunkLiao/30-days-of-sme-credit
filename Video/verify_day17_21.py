"""驗證 Day17～21，更新播放入口。"""
from pathlib import Path
import json
from verify_day01_04 import run

if __name__=='__main__':
 episodes=json.loads((Path(__file__).resolve().parent/'episodes17-21.json').read_text(encoding='utf-8'))
 run(episodes=episodes,batch_key='DAY17_21',label='Day 17～21',date='2026-11-23',teaching_note='本批採虛構案例；Day18 明列營業淨現金流減資本支出及現金股利的口徑，利息核對是否已計入。Day19～20 不虛構真實同業統計值，不以單一指標或偏離決定准駁。Day21 交貨不等於驗收或已可收款。')
