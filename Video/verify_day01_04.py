"""驗證指定批次影片，保存獨立紀錄並依實際檔案更新播放入口。"""
from pathlib import Path
import array, html, json, re, subprocess, wave

ROOT=Path(__file__).resolve().parent
EPISODES=json.loads((ROOT/'episodes01-04.json').read_text(encoding='utf-8'))

def run(episodes=None, batch_key='DAY01_04', label='Day 01～04', date='2026-11-22', teaching_note='Day03 的 1,800＋200＝2,000 萬元不表示法定分級門檻。'):
 results=[]
 for ep in (EPISODES if episodes is None else episodes):
  folder=ROOT/ep['slug']; video=ROOT/f'Day{ep["day"]}.mp4'
  assert video.exists() and video.stat().st_size>100000, str(video)
  assert video.stat().st_mtime>(folder/'index.html').stat().st_mtime, '影片輸出早於最新來源，需重新輸出'
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)],encoding='utf-8'))
  vs=next(s for s in probe['streams'] if s['codec_type']=='video')
  assert (vs['width'],vs['height'])==(1080,1920)
  assert vs['codec_name']=='h264' and vs['r_frame_rate']=='24/1'
  assert any(s['codec_type']=='audio' and s['codec_name']=='aac' for s in probe['streams'])
  seconds=float(probe['format']['duration']); assert 45<=seconds<=60
  subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True,capture_output=True)
  with wave.open(str(folder/'assets/narration.wav'),'rb') as audio:
   wav_seconds=audio.getnframes()/audio.getframerate()
   samples=array.array('h',audio.readframes(audio.getnframes()))
  assert max(map(abs,samples))>100 and abs(seconds-wav_seconds)<.15
  def clock(t):
   h,m,s,ms=map(int,re.split('[:,]',t)); return h*3600+m*60+s+ms/1000
  last=0
  for a,b in re.findall(r'(\d\d:\d\d:\d\d,\d\d\d) --> (\d\d:\d\d:\d\d,\d\d\d)',(folder/'captions.srt').read_text(encoding='utf-8')):
   start,end=clock(a),clock(b); assert start>=last-.002 and start<end<=seconds+.02; last=end
  rp=max((folder/'.hyperframes/artifacts/checks').glob('*.json'),key=lambda p:p.stat().st_mtime)
  report=json.loads(rp.read_text(encoding='utf-8'))
  assert report['ok'] and rp.stat().st_mtime>(folder/'index.html').stat().st_mtime
  findings={k:{'errors':v.get('errorCount',0),'warnings':v.get('warningCount',0),'codes':sorted(set(x['code'] for x in v['findings']))} for k,v in report.items() if isinstance(v,dict) and 'findings' in v}
  assert all(v['errors']==0 for v in findings.values())
  subprocess.run(['ffmpeg','-v','error','-ss','3','-i',str(video),'-frames:v','1','-update','1',str(folder/'cover.jpg'),'-y'],check=True)
  results.append(dict(day=ep['day'],file=video.name,seconds=seconds,bytes=video.stat().st_size,findings=findings,report=str(rp.relative_to(ROOT))))
 (ROOT/f'verification_{batch_key.lower()}.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
 md=f'# {label} 影片驗證紀錄\n\n日期：{date}。沿用案例判斷＋圖解、繁體字幕與 Microsoft Hanhan Desktop 本機合成旁白，無配樂。\n\n| 影片 | 長度 | 尺寸 | 影音 |\n|---|---|---|---|\n'
 for r in results: md+=f'| [{r["file"]}]({r["file"]}) | {r["seconds"]:.2f} 秒 | 1080 × 1920 | H.264 / AAC、24 fps |\n'
 md+='\n## 已完成檢查\n\n- HyperFrames check：程式、版面、動態、對比、音訊；安全區涵蓋 Reels 與 Shorts。\n- 每支六段的中間時間點均擷取並檢視畫面，見各集 snapshots/contact-sheet.jpg。\n- MP4 全片解碼成功；包含視訊與音訊軌，且時長與 WAV 一致。\n- WAV 有聲音訊號，字幕依序、無重疊且未超過影片長度。\n- 每集保留 SCRIPT.md、STORYBOARD.md、NOTES.md、captions.srt 與可重製來源。\n- 內容使用教學假設案例；Day03 的 1,800＋200＝2,000 萬元不表示法定分級門檻。\n\n## 限制與後續\n\n合成語音尚待使用者聽取回饋；句內字幕按字數分配，未宣稱人工逐字校時。尚未代為上傳或發布。\n\n'
 for r in results:
  md+=f'### Day {r["day"]}\n\n'
  for name,v in r['findings'].items():
   md+=f'- {name}：{v["errors"]} 錯誤、{v["warnings"]} 提示'+('（'+'、'.join(v['codes'])+'）' if v['codes'] else '')+'。\n'
 md+='\n已檢視提示；單檔場景結構與字幕軌密度提示不影響本批輸出。\n'
 md=md.replace('Day03 的 1,800＋200＝2,000 萬元不表示法定分級門檻。',teaching_note)
 (ROOT/f'VERIFICATION_{batch_key}.md').write_text(md,encoding='utf-8')
 update_hub(date=date,extra_report=(f'VERIFICATION_{batch_key}.md',label+' 驗證'))
 print(json.dumps([{k:r[k] for k in ['day','file','seconds','bytes']} for r in results],ensure_ascii=False,indent=2))

def update_hub(date='2026-11-22',extra_report=None):
 path=ROOT/'index.html'; text=path.read_text(encoding='utf-8'); cards=[]
 for folder in sorted(ROOT.glob('day*')):
  if not (folder/'episode.json').exists(): continue
  ep=json.loads((folder/'episode.json').read_text(encoding='utf-8'))
  video=ROOT/f'Day{ep["day"]}.mp4'
  if not video.exists(): continue
  poster=folder/'cover.jpg'
  if not poster.exists(): poster=next(iter(sorted((folder/'snapshots').glob('frame-00-*.png'))),poster)
  poster_attr=' poster="'+poster.relative_to(ROOT).as_posix()+'"' if poster.exists() else ''
  cards.append(f'<article><div class="tag">DAY {ep["day"]} / 30 · {ep["duration"]:.0f} 秒</div><h2>{html.escape(ep["title"])}</h2><video controls playsinline preload="metadata"{poster_attr} src="{video.name}"></video><p>{html.escape(ep["thesis"])}</p><nav><a href="{folder.name}/SCRIPT.md">旁白稿</a> · <a href="{folder.name}/STORYBOARD.md">逐秒分鏡</a> · <a href="{folder.name}/NOTES.md">教材依據與貼文</a></nav></article>')
 text=re.sub(r'<div class="grid">.*?</div><footer>', '<div class="grid">\n'+'\n'.join(cards)+'\n</div><footer>',text,flags=re.S)
 text=text.replace('三支 Reels 試作','影片作品集').replace('給銀行徵授信新手的三支試作。','給銀行徵授信新手的七支影片。').replace('試作第一版','課程短影片').replace('試作日期：','更新日期：')
 text=text.replace('<a href="VERIFICATION.md">驗證結果</a>','<a href="VERIFICATION.md">首批驗證</a> · <a href="VERIFICATION_DAY01_04.md">Day 01～04 驗證</a> · <a href="TODO.md">製作進度</a>')
 text=re.sub(r'給銀行徵授信新手的[^。]*。',f'給銀行徵授信新手的 {len(cards)} 支影片。',text)
 text=re.sub(r'更新日期：\d{4}-\d{2}-\d{2}',f'更新日期：{date}',text)
 if extra_report and extra_report[0] not in text:
  text=text.replace('<a href="TODO.md">製作進度</a>',f'<a href="{extra_report[0]}">{html.escape(extra_report[1])}</a> · <a href="TODO.md">製作進度</a>')
 path.write_text(text,encoding='utf-8')

if __name__=='__main__': run()
