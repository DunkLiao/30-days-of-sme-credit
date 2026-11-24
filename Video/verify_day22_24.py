"""驗證 Day22～24，更新播放入口。"""
from pathlib import Path
import json
from verify_day01_04 import run
if __name__=='__main__':
 episodes=json.loads((Path(__file__).resolve().parent/'episodes22-24.json').read_text(encoding='utf-8'))
 run(episodes=episodes,batch_key='DAY22_24',label='Day 22～24',date='2026-11-23',teaching_note='本批採新編虛構案例。Day22 為賒銷批發情境，不代表所有零售業態。Day23 假設收入已依適用會計處理認列；合約資產仍附時間經過以外的收款條件。Day24 不把發票等同交易已全部查證，不宣告無追索權一律免責；責任依個案契約與適用程序確認。')
