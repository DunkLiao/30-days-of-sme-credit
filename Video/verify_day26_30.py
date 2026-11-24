"""驗證 Day26～30，更新播放入口。"""
from pathlib import Path
import json
from verify_day01_04 import run
if __name__=='__main__':
 episodes=json.loads((Path(__file__).resolve().parent/'episodes26-30.json').read_text(encoding='utf-8'))
 run(episodes=episodes,batch_key='DAY26_30',label='Day 26～30',date='2026-11-24',teaching_note='本批採新編虛構案例。不以關係人應收、說法落差、分期款項或一次停機直接認定舞弊、違法或違約；不猜測聯徵逐位代碼，不把股東墊款自動視為權益，不把留存紀錄視為自動免責。審查與決策依機構職責分工及權限辦理。')
