"""驗證本批五支影片，另存紀錄並更新播放入口。"""
import json
from pathlib import Path
from verify_day01_04 import run

if __name__=='__main__':
 episodes=json.loads((Path(__file__).resolve().parent/'episodes06-10.json').read_text(encoding='utf-8'))
 run(episodes=episodes,batch_key='DAY06_10',label='Day 06～10',date='2026-11-23',teaching_note='本批聚焦查核步驟，不宣告固定法規門檻、補件日期、處分排除期間或自動免責；個案依適用規定確認。')
