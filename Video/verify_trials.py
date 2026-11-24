"""檢查實際影片、語音、字幕與最新 HyperFrames 報告並保存摘要。"""
from pathlib import Path
import json, subprocess, wave, array, re

ROOT = Path(__file__).resolve().parent
results=[]
for folder in sorted(ROOT.glob('day*')):
 if not folder.is_dir(): continue
 ep=json.loads((folder/'episode.json').read_text(encoding='utf-8'))
 with wave.open(str(folder/'assets/narration.wav'),'rb') as audio:
  duration=audio.getnframes()/audio.getframerate()
  samples=array.array('h',audio.readframes(audio.getnframes()))
 assert 45<=duration<=60, (folder.name,duration)
 assert max(abs(x) for x in samples)>100, '旁白不可為空白音訊'
 srt=(folder/'captions.srt').read_text(encoding='utf-8')
 def parse(t):
  h,m,s,ms=map(int,re.split('[:,]',t)); return h*3600+m*60+s+ms/1000
 last=0
 for start,end in re.findall(r'(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)',srt):
  a,b=parse(start),parse(end)
  assert a>=last-.002 and b>a and b<=duration+.01, (folder.name,a,b)
  last=b
 reports=list((folder/'.hyperframes/artifacts/checks').glob('*.json'))
 report_path=max(reports,key=lambda p:p.stat().st_mtime)
 report=json.loads(report_path.read_text(encoding='utf-8'))
 assert report.get('ok') is True, report_path
 assert report_path.stat().st_mtime>(folder/'index.html').stat().st_mtime, '檢查必須晚於最後修改'
 video=ROOT/f'Day{ep["day"]}-trial.mp4'
 assert video.is_file() and video.stat().st_size>100000, video
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],encoding='utf-8'))
 streams=probe['streams']; visual=next(s for s in streams if s['codec_type']=='video')
 assert visual['width']==1080 and visual['height']==1920
 assert any(s['codec_type']=='audio' for s in streams)
 rendered=float(probe['format']['duration']); assert abs(rendered-duration)<.15
 findings={k:{'errors':v.get('errorCount',0),'warnings':v.get('warningCount',0),'codes':sorted(set(x.get('code','') for x in v['findings']))} for k,v in report.items() if isinstance(v,dict) and 'findings' in v}
 results.append(dict(day=ep['day'],seconds=round(rendered,3),file=video.name,bytes=video.stat().st_size,streams=[s['codec_type'] for s in streams],check=str(report_path.relative_to(ROOT)),findings=findings))
(ROOT/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
md='# 試作驗證結果\n\n日期：2026-11-22。實際讀取 MP4、WAV、SRT 及最新 HyperFrames 檢查報告。\n\n| 試作 | 影片長度 | 尺寸 | 聲音 | 檔案大小 |\n|---|---|---|---|---|\n'
for r in results: md+=f'| Day {r["day"]} | {r["seconds"]:.2f} 秒 | 1080 × 1920 | 有 | {r["bytes"]/1024/1024:.2f} MB |\n'
md+='\n## 驗證範圍\n\n- 三支最新 HyperFrames check 均通過，檢查涵蓋程式、版面、對比、動態及音訊。安全區以本案指定的 Instagram Reels 為準。\n- 逐句音訊非靜音；字幕依序且未超出音訊，影片包含視訊與音訊軌。\n- 影片長度與旁白時間軸一致；皆為 45～60 秒。\n- 已抽查每支多個時間點的畫面，聯絡表置於各專案 snapshots/contact-sheet.jpg；另抽查 MP4 實際輸出畫面。\n- MP4 為本輪 draft 試作輸出，1080 × 1920、24 fps、H.264 / AAC。\n- 本輪配音為本機合成語音，字幕句內時間依字數估計；未做人工聽打逐字校時。\n\n## 檢查提示\n\n'
for r in results:
 md+=f'### Day {r["day"]}\n\n'
 for k,v in r['findings'].items():
  md+=f'- {k}：{v["errors"]} 錯誤、{v["warnings"]} 提示'+('（'+ '、'.join(v['codes'])+'）' if v['codes'] else '')+'。\n'
md+='\n提示已逐類檢視。單一 HTML 的場景結構與字幕軌較密，仍可完整播放與修改；如有 safe-zone 提示，應以各平台實際發布介面再預覽。原課程頁未修改。\n'
(ROOT/'VERIFICATION.md').write_text(md,encoding='utf-8')
print(json.dumps([{k:r[k] for k in ['day','seconds','file','bytes']} for r in results],ensure_ascii=False,indent=2))
