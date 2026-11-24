"""可重建的三支試作：內容資料、逐句時間軸、HyperFrames 與審稿文件。"""
from pathlib import Path
import json, html, shutil, wave, subprocess, re

ROOT = Path(__file__).resolve().parent
EPISODES = [
 dict(day='05', slug='day05-tax-reconciliation', title='營收對不起來，先查什麼？', topic='營業稅申報書與營收勾稽', source='Day05.html', anchors=['body-ch3','body-ch4'], thesis='先對期間，再調差異，最後追金流。', post='申報銷售額與財報營收不同，先把期間與口徑對齊，再用交易和收款證據驗證。收藏這三步，下次接件就能用。', scenes=[
  dict(label='案件疑問', title='營收對不起來', sub='你會先查哪裡？', visual='hook', lines=['客戶說營收很好，申報銷售額卻和財報不同。你會先查哪裡？']),
  dict(label='教學案例', title='同一年，兩個數字', sub='明川公司｜金額單位：萬元', visual='compare', metrics=[['401 累計銷售額','2,400'],['財報營業收入','2,150']], note='差額 250 萬元，原因待查', lines=['假設明川公司，同一年度四零一申報銷售額兩千四百萬元，財報營收兩千一百五十萬元。','差了兩百五十萬元，能直接認定營收造假嗎？']),
  dict(label='停一下，先判斷', title='差異，代表什麼？', sub='先想一個可能原因', visual='question', lines=['先停一下。你會先問期間，還是先下結論？']),
  dict(label='拆解觀念', title='先把口徑對齊', sub='差異是查核起點', visual='steps', items=['期間是否一致？','認列時點是否不同？','交易範圍有何差異？'], lines=['先核對期間是否一致，再確認收入認列時點和交易範圍。','例如預收款或資產處分，可能造成申報與營收的差異。','請客戶逐項說明，取得明細與憑證，建立差異調節表。']),
  dict(label='明天接件就能做', title='把數字接到證據', sub='調節表 → 交易憑證 → 收款紀錄', visual='steps', items=['索取差異調節表','核對訂單、發票與交貨','追查收款與期後退折讓'], lines=['接著比對訂單、發票、交貨與收款紀錄，並追查期後退貨折讓。','即使兩個數字相同，也要驗證交易和收款。']),
  dict(label='今天帶走一句話', title='先對期間，再調差異', sub='最後追金流', visual='closing', lines=['今天記住：先對期間，再調差異，最後追金流。完整練習看第五天課程。'])
 ]),
 dict(day='16', slug='day16-profit-quality', title='賺更多，錢有進來嗎？', topic='損益表審核與獲利品質', source='Day16.html', anchors=['sec-workbench-title','sec-chapters-title'], thesis='看到獲利增加，接著問錢收回來了沒。', post='淨利增加，營業現金流卻是負數？把獲利接回應收帳款、存貨及期後收款，才能繼續評估還款來源。', scenes=[
  dict(label='案件疑問', title='賺更多', sub='錢，也進來了嗎？', visual='hook', lines=['客戶今年賺更多，你就能放心了嗎？先看另一張表。']),
  dict(label='教學案例', title='獲利與現金流背離', sub='明川公司｜同一年度，單位：萬元', visual='compare', metrics=[['本期淨利','＋300'],['營業活動淨現金流','－200']], note='帳面獲利，營運現金卻淨流出', lines=['假設明川公司今年淨利三百萬元，營業活動淨現金流卻是負兩百萬元。','同時，應收帳款比去年增加。你會接著查什麼？']),
  dict(label='停一下，先判斷', title='有獲利，沒現金？', sub='錢可能停在哪裡？', visual='question', lines=['先想一想。營收已經認列，貨款可能還沒收回。']),
  dict(label='拆解觀念', title='沿著現金去找原因', sub='這是待查線索，還需要證據', visual='steps', items=['應收帳款：貨款尚未收回？','存貨：資金投入備貨？','付款：支付時點改變？'], lines=['營業現金流也受存貨備貨和付款時點影響。','所以，淨利和現金流的差額，不能全算成未收貨款。','也不能只憑一年負現金流，就直接認定企業沒有還款能力。']),
  dict(label='明天接件就能做', title='追到實際收款', sub='帳齡 → 期後收款 → 銀行流水', visual='steps', items=['索取應收帳款帳齡','核對期後收款紀錄','查存貨與金流變動原因'], lines=['先索取應收帳款帳齡，核對期後收款與銀行流水。','再查存貨和付款變化，判斷現金流出的原因是否持續。']),
  dict(label='今天帶走一句話', title='看到獲利增加', sub='接著問：錢收回來了沒？', visual='closing', lines=['今天記住：看到獲利增加，接著問錢收回來了沒。完整練習看第十六天課程。'])
 ]),
 dict(day='25', slug='day25-group-network', title='借一家，為什麼查整群？', topic='關係企業與集團網絡穿透查核', source='Day25.html', anchors=['unit-1','unit-3','unit-4'], thesis='畫出關係，更要沿著資金查證。', post='借款主體只有一家，也要追查背後的控制、保證與資金往來。把關係線與金流線分開，才能把問題問清楚。', scenes=[
  dict(label='案件疑問', title='借款的是一家', sub='為什麼要查整個集團？', visual='hook', lines=['借款的是一家公司，為什麼徵信還要查整個集團？']),
  dict(label='教學案例', title='三家公司，三種連結', sub='以下均為虛構教學情境', visual='network', note='箭頭分別代表控制、保證與資金往來', lines=['假設明川公司來借款，背後有控股公司，旁邊還有一家貿易公司。','控股公司提供保證，明川又經常匯款給貿易公司。']),
  dict(label='停一下，先判斷', title='只看借款人，夠嗎？', sub='哪一條線需要繼續追？', visual='question', lines=['只看明川自己的財報，能看清楚這些往來嗎？']),
  dict(label='拆解觀念', title='把兩種線分開畫', sub='關係怎麼連，資金怎麼走', visual='steps', items=['控制線：誰掌握經營？','保證線：誰對誰負責？','金流線：款項流向哪裡？'], lines=['先確認誰控制誰，再核對誰替誰保證。','接著把資金往來另外畫出來，查清用途、條件和回收情形。','同一個集團，不代表每家公司都互相負有保證責任。']),
  dict(label='明天接件就能做', title='每條線，都要有依據', sub='文件核對，加上實際金流', visual='steps', items=['核對股權與控制資料','核對保證契約與範圍','追查往來明細及銀行流水'], lines=['依企業情況核對股權資料、財報揭露及適用的關係企業資料。','再查保證契約、往來明細和銀行流水，記錄來源與查核日期。']),
  dict(label='今天帶走一句話', title='畫出關係', sub='更要沿著資金查證', visual='closing', lines=['今天記住：畫出關係，更要沿著資金查證。完整練習看第二十五天課程。'])
 ])
]

def save_json(path, value):
 path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def prepare(manifest_path=None):
 for ep in EPISODES:
  folder=ROOT/ep['slug']; (folder/'assets/audio').mkdir(parents=True,exist_ok=True)
  (folder/'capture/extracted').mkdir(parents=True,exist_ok=True)
  save_json(folder/'episode.json',ep)
  save_json(folder/'capture/extracted/tokens.json',dict(title=ep['title'],description=ep['topic'],colors=[],fonts=[]))
  source=ROOT.parent/ep['source']
  # 來源是本地教材，保存完整文字供後續重製與查核。
  text=re.sub('<[^>]+>',' ',re.sub(r'<(script|style)\b[^>]*>.*?</\1>','',source.read_text(encoding='utf-8'),flags=re.S))
  (folder/'capture/extracted/visible-text.txt').write_text(html.unescape(text),encoding='utf-8')
 save_json(manifest_path or ROOT/'episodes.json',EPISODES)

def srt_time(t):
 ms=round(t*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def finalize():
 from fontTools.ttLib import TTFont
 from fontTools import subset
 alltext=''.join(json.dumps(ep,ensure_ascii=False) for ep in EPISODES)+Path(__file__).read_text(encoding='utf-8')
 shared=ROOT/'assets'; shared.mkdir(exist_ok=True)
 font=TTFont('C:/Windows/Fonts/msjh.ttc',fontNumber=0)
 opts=subset.Options(); opts.flavor='woff2'; opts.layout_features=['*']
 sub=subset.Subsetter(options=opts); sub.populate(text=alltext); sub.subset(font)
 font.flavor='woff2'; font.save(shared/'trial-tc.woff2')
 for ep in EPISODES:
  folder=ROOT/ep['slug']; assets=folder/'assets'; shutil.copy2(shared/'trial-tc.woff2',assets/'trial-tc.woff2')
  shutil.copy2(shared/'gsap.min.js',assets/'gsap.min.js')
  scenes=ep['scenes']; all_audio=bytearray(); cursor=0; cues=[]
  for i,scene in enumerate(scenes):
   scene['start']=round(cursor,3); scene['cues']=[]
   for j,line in enumerate(scene['lines']):
    with wave.open(str(assets/f'audio/{i+1:02}-{j+1:02}.wav'),'rb') as wav:
     params=wav.getparams(); frames=wav.readframes(wav.getnframes()); seconds=wav.getnframes()/wav.getframerate()
    cue=dict(start=round(cursor+.18,3),end=round(cursor+.18+seconds,3),text=line)
    silence=b'\x00'*int(params.framerate*.18)*params.nchannels*params.sampwidth
    all_audio+=silence+frames; cursor+=.18+seconds
    cues.append(cue); scene['cues'].append(cue)
   minimum=[5,11,4.5,14,12,7][i]
   rest=max(.35,minimum-(cursor-scene['start']))
   all_audio+=b'\x00'*int(params.framerate*rest)*params.nchannels*params.sampwidth; cursor+=rest
   scene['duration']=round(cursor-scene['start'],3)
  ep['duration']=round(cursor,3)
  with wave.open(str(assets/'narration.wav'),'wb') as wav:
   wav.setparams(params); wav.writeframes(all_audio)
  save_json(folder/'episode.json',ep); save_json(folder/'timings.json',cues)
  (folder/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt_time(c["start"])} --> {srt_time(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')
  script=f'# Day {ep["day"]}｜{ep["title"]}\n\n**Voice:** Microsoft Hanhan Desktop（zh-TW，本機試作語音）\n\n**Voice direction:** 沉穩清楚的銀行前輩，正常偏快語速。\n\n'
  board=f'---\nformat: 1080x1920\nmessage: "{ep["thesis"]}"\narc: story-explainer with how-to\naudience: 銀行徵授信新手\n---\n\n# Day {ep["day"]} 逐秒分鏡\n\n## Video direction\n\n奶油白與鈷藍專業圖解；上方系列識別，中間案例圖解，下方字幕。所有公司與數字為教學假設。畫面依旁白逐項出現，避免一次塞滿；底部保留操作介面空間。以既有來源作教學重組，不引入法規門檻。\n\n'
  num=0
  for i,s in enumerate(scenes):
   for c in s['cues']:
    num+=1; script+=f'## Line {num} — {s["label"]} (Frame {i+1})\n\n**Time:** {c["start"]:.2f} – {c["end"]:.2f}s\n\n**Delivery:** 清楚、直接，問句留停頓。\n\n    {c["text"]}\n\n'
   board+=f'## Frame {i+1} — {s["label"]}\n\n- status: animated\n- duration: {s["duration"]:.3f}s\n- start: {s["start"]:.3f}s\n- transition_in: cut\n- type: {"hook" if i==0 else "cta" if i==5 else "feature_showcase"}\n- persuasion: Question→answer pairing + progressive disclosure\n- beat: {"curiosity" if i<3 else "clarity"}\n- scene: {s["title"]}；{s["sub"]}\n- voiceover: {"".join(s["lines"])}\n- blueprint: compose\n- asset_candidates: []\n- focal: {s["visual"]} 圖解\n\nnarrativeRole：{s["label"]}，帶觀眾從疑點前進到查核動作。\n\nkeyMessage：{s.get("note",s["sub"])}\n\n'
   for j,c in enumerate(s['cues']):
    board+=f'Scene {j+1}（全片 {c["start"]:.2f}–{c["end"]:.2f}s）：旁白「{c["text"]}」。對應圖解元素逐項揭露，以平移與透明度銜接；數值卡與清單保留閱讀停頓。\n\n'
  (folder/'SCRIPT.md').write_text(script,encoding='utf-8'); (folder/'STORYBOARD.md').write_text(board,encoding='utf-8')
  sources=f'# Day {ep["day"]} 來源與編輯說明\n\n來源：[{ep["source"]}](../../{ep["source"]})。讀取日期：2026-11-22。\n\n主題：{ep["topic"]}。學習目標：{ep["thesis"]}\n\n明川公司、控股公司、貿易公司及影片所有數字均為新編教學假設，不是真實客戶資料，也不是教材原案例的逐字重現。\n\n'
  if ep['day']=='05': sources+='依據教材第三章的跨來源勾稽與期間一致性、第四章退貨折讓查核。2,400、2,150、250 為教學假設；差異可能來自認列與範圍，需調節查證。未採用教材中未驗證的舞弊比例或門檻。\n'
  if ep['day']=='16': sources+='依據損益品質與金流勾稽檢驗台、帳賺現金流情境。淨利＋300、營業現金流－200 為教學假設，差額不得全部歸因於應收帳款；影片保留存貨、付款時點及持續性判斷。\n'
  if ep['day']=='25': sources+='依據關係企業建檔、實質控制、保證架構及隱蔽性關係企業章節。連線圖為假設情境；控制、保證、金流須分別查證，不以同集團直接推定保證責任，也不使用原課程指名真實企業的風險指控。\n'
  sources+='\n## 貼文草稿\n\n'+ep['post']+f'\n\n完整課程：Day{ep["day"]}.html（實際發布時換成正式網站當日網址）。\n\n#銀行新人 #徵信 #授信 #財報分析 #徵授信實務\n\n## 語音與素材\n\n本機 Microsoft Hanhan Desktop 語音，無外部配音服務。圖形為 HTML/CSS/SVG 原創；字型由本機 Microsoft JhengHei 擷取試作所需字元，僅供本機試作；若對外散布原始專案，應換成可再散布的開源字型。GSAP 為本地固定版本 3.14.2。無背景音樂。\n'
  (folder/'NOTES.md').write_text(sources,encoding='utf-8')
  build_html(folder,ep,cues)
  print(ep['slug'], ep['duration'])

def build_html(folder,ep,cues):
 esc=html.escape; dur=ep['duration']; parts=[]; animations=[]
 for i,s in enumerate(ep['scenes']):
  sid=f's{i}'; start=s['start']; sd=s['duration']; v=s['visual']
  content=''
  if v in ['hook','closing']:
   content=f'<div class="hero-mark reveal">{ep["day"]}</div><div class="ruler reveal"></div><p class="hero-note reveal">{esc(ep["topic"] if v=="hook" else "完整練習：Day "+ep["day"]+" 課程")}</p>'
  elif v=='compare':
   content='<div class="metrics">'+''.join(f'<div class="metric reveal"><p>{esc(l)}</p><strong>{esc(n)}</strong><div class="bar"><i style="width:{100 if j==0 else 89.58 if ep["day"]=="05" else 66.67}%"></i></div></div>' for j,(l,n) in enumerate(s['metrics']))+'</div>'+f'<p class="callout reveal">{esc(s["note"])}</p>'
  elif v=='question':
   content='<div class="question reveal">？</div><div class="choices reveal"><span>找原因</span><span>找證據</span></div><p class="quiet reveal">保留疑點，繼續查證</p>'
  elif v=='steps':
   content='<div class="steps">'+''.join(f'<div class="step reveal"><b>{j+1:02}</b><p>{esc(item)}</p></div>' for j,item in enumerate(s['items']))+'</div>'
  elif v=='network':
   content='''<div class="network"><svg viewBox="0 0 860 650" aria-label="控制、保證與資金往來關係圖"><g fill="none" stroke="#1e2bfa" stroke-width="4"><path class="link" d="M430 140 L430 285"/><path class="link" d="M270 330 Q110 170 305 100" stroke-dasharray="10 10"/><path class="link" d="M430 390 L430 490"/></g></svg><div class="node n1 reveal">控股公司</div><div class="node n2 reveal">明川公司<span>借款人</span></div><div class="node n3 reveal">貿易公司</div><div class="edge e1 reveal">控制 ↓</div><div class="edge e2 reveal">提供保證</div><div class="edge e3 reveal">資金往來 ↓</div></div>'''
  scene_class=v if v!='network' else 'network-scene'
  parts.append(f'<section id="{sid}" class="clip scene {scene_class}" data-start="{start}" data-duration="{sd}" data-track-index="1"><header><span>徵授信新手</span><span>DAY {ep["day"]} / 30</span></header><div class="scene-body"><p class="eyebrow">{i+1:02} / {esc(s["label"])}</p><h1>{esc(s["title"])}</h1><p class="sub">{esc(s["sub"])}</p><div class="graphic">{content}</div></div><p class="case-tag">教學假設案例 · 先查證，再判斷</p></section>')
  animations.append(f'tl.fromTo("#{sid} h1",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.55,ease:"power3.out"}},{start+.06});')
  # 圖解依各段旁白分批進場，整段持續有新資訊。
  reveal_offsets=[.3, min(sd*.37,4.3),min(sd*.68,8.8)]
  if v in ['hook','closing']: reveal_offsets=[.3,1.1,2.1]
  if v=='compare': reveal_offsets=[.5,min(4.4,sd*.4),max(6.5,sd*.7)]
  animations.append(f'document.querySelectorAll("#{sid} .reveal").forEach((e,j)=>tl.fromTo(e,{{y:25,opacity:0}},{{y:0,opacity:1,duration:.55,ease:"power3.out"}},{start}+{json.dumps(reveal_offsets)}[Math.min(j,2)]));')
  if v=='compare': animations.append(f'tl.fromTo("#{sid} .bar i",{{scaleX:0}},{{scaleX:1,duration:1,stagger:.2,ease:"power3.out"}},{start+1});')
 captions=[]
 # 長句拆為短字幕；逐句語音實測，句內按字數比例分配，非 ASR 字級對齊。
 caption_cues=[]
 for c in cues:
  chunks=[x for x in re.split('(?<=[，。？！：])',c['text']) if x]
  chunks2=[]
  for chunk in chunks:
   if len(chunk)>24:
    pivot=len(chunk)//2; chunks2.extend([chunk[:pivot],chunk[pivot:]])
   else: chunks2.append(chunk)
  if ep.get('merge_short_captions'):
   merged=[]; index=0
   while index<len(chunks2):
    chunk=chunks2[index]
    if len(chunk)<ep.get('short_caption_chars',6) and index+1<len(chunks2) and len(chunk)+len(chunks2[index+1])<=24:
     chunk+=chunks2[index+1]; index+=1
    elif len(chunk)<ep.get('short_caption_chars',6) and merged and len(merged[-1])+len(chunk)<=24:
     merged[-1]+=chunk; index+=1; continue
    merged.append(chunk); index+=1
   chunks2=merged
  total=sum(len(x) for x in chunks2); at=c['start']
  for chunk in chunks2:
   seconds=(c['end']-c['start'])*len(chunk)/total
   caption_cues.append(dict(start=at,end=at+seconds,text=chunk)); at+=seconds
 for n,c in enumerate(caption_cues):
  captions.append(f'<div id="cap{n}" class="clip caption" data-start="{c["start"]:.3f}" data-duration="{c["end"]-c["start"]:.3f}" data-track-index="3"><span>{esc(c["text"])}</span></div>')
 (folder/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt_time(c["start"])} --> {srt_time(c["end"])}\n{c["text"]}' for i,c in enumerate(caption_cues))+'\n',encoding='utf-8')
 css='''@font-face{font-family:TrialTC;src:url(assets/trial-tc.woff2)}*{box-sizing:border-box}body{margin:0;background:#fdfae7;color:#111;font-family:TrialTC,sans-serif}#root{width:1080px;height:1920px;position:relative;overflow:hidden;container-type:size}.clip{position:absolute;inset:0}.bg{background:#fdfae7}.scene{padding:170px 94px 390px 84px;background:#fdfae7}header{display:flex;justify-content:space-between;font-size:28px;color:#1e2bfa;border-bottom:2px solid rgba(30,43,250,.2);padding-bottom:28px;letter-spacing:2px}.scene-body{padding-top:64px}.eyebrow{font-size:26px;letter-spacing:2px;color:#1e2bfa;margin:0 0 24px}h1{font-size:76px;line-height:1.35;letter-spacing:-2px;margin:0 0 24px;font-weight:700;max-width:870px}.sub{font-size:36px;line-height:1.6;color:#555;margin:0}.graphic{margin-top:54px;position:relative;min-height:520px}.hero-mark{font-size:310px;font-weight:700;line-height:1.25;color:#1e2bfa;letter-spacing:-12px}.ruler{width:180px;height:7px;background:#1e2bfa;margin:30px 0}.hero-note{font-size:35px;line-height:1.7;max-width:760px;margin:20px 0}.metrics{display:flex;flex-direction:column;gap:26px}.metric{padding:24px 32px;border:2px solid rgba(30,43,250,.2);background:rgba(30,43,250,.04);border-radius:14px}.metric p{font-size:30px;margin:0 0 6px;color:#555}.metric strong{font-size:104px;line-height:1.45;letter-spacing:-2px;color:#1e2bfa;font-weight:700}.bar{height:13px;width:100%;background:rgba(30,43,250,.08);border-radius:6px;margin-top:12px;overflow:hidden}.bar i{display:block;height:100%;background:#1e2bfa;transform-origin:left center}.callout{font-size:32px;line-height:1.7;border-left:5px solid #1e2bfa;padding:12px 22px;margin:26px 0}.question{font-size:290px;color:#1e2bfa;line-height:1.25;text-align:center}.choices{display:flex;justify-content:center;gap:28px;margin-top:28px}.choices span{font-size:36px;padding:20px 42px;border:2px solid rgba(30,43,250,.2);border-radius:100px;background:rgba(30,43,250,.04)}.quiet{font-size:32px;color:#555;text-align:center;margin-top:38px}.steps{display:flex;flex-direction:column;gap:26px}.step{display:flex;gap:24px;align-items:center;min-height:142px;border:2px solid rgba(30,43,250,.2);border-radius:14px;padding:24px;background:rgba(30,43,250,.04)}.step b{font-size:39px;color:#1e2bfa;width:60px;flex-shrink:0}.step p{font-size:36px;line-height:1.7;margin:0;max-width:660px}.case-tag{position:absolute;left:84px;bottom:426px;font-size:24px;color:#555;margin:0}.caption{inset:auto 98px 286px 84px;height:150px;display:flex;align-items:center;justify-content:center}.caption span{font-size:42px;line-height:1.65;text-align:center;color:#fdfae7;background:#111;padding:13px 26px;border-radius:12px;max-width:880px;min-width:100px}.progress-track{position:absolute;left:84px;right:98px;bottom:250px;height:5px;background:rgba(30,43,250,.15)}.progress{height:100%;width:100%;background:#1e2bfa;transform-origin:left center}.network{width:860px;height:650px;position:relative}.network svg{position:absolute;inset:0;width:860px;height:650px}.node{position:absolute;width:340px;height:126px;left:260px;border:2px solid rgba(30,43,250,.2);background:#fdfae7;border-radius:14px;font-size:40px;display:flex;justify-content:center;align-items:center;flex-direction:column}.node span{font-size:26px;color:#1e2bfa}.n1{top:0}.n2{top:280px;background:#eae9e9}.n3{top:510px}.edge{position:absolute;font-size:26px;color:#1e2bfa;background:#fdfae7;padding:8px}.e1{top:177px;left:450px}.e2{top:190px;left:65px}.e3{top:433px;left:450px}.closing h1{font-size:76px}.closing .hero-mark{font-size:210px}.closing .graphic{margin-top:44px}'''
 # Reels 操作介面安全區：主要文字置於 x=120..920、y=270..1490。
 css+='''.scene{padding:270px 160px 600px 120px}.scene-body{padding-top:40px}.eyebrow{font-size:28px}h1,.closing h1{font-size:70px;max-width:800px}.sub{font-size:34px}.graphic,.closing .graphic{margin-top:40px}.hero-mark{font-size:260px}.hero-note{font-size:32px}.metric{padding:20px 26px}.metric p{font-size:28px}.metric strong{font-size:88px;line-height:1.3}.callout{font-size:30px}.case-tag{left:120px;bottom:620px;font-size:28px}.caption{left:120px;right:160px;bottom:430px;height:150px}.caption span{font-size:40px;max-width:800px}.progress-track{left:120px;right:160px;bottom:400px}.network{transform:scale(.88);transform-origin:top left}.node span,.edge{font-size:32px}.step p{font-size:34px}.step{padding:20px}.closing .hero-mark{font-size:190px}'''
 # network 同時是場景類別，縮放只能套到圖形容器，避免整個場景被縮小兩次。
 css+='''.scene.network{transform:none}.scene{padding-right:200px}.scene-body{padding-top:24px}.eyebrow{margin-bottom:16px}h1{margin-bottom:16px}.graphic,.closing .graphic{margin-top:24px}.hero-mark{font-size:180px}.closing .hero-mark{font-size:160px}.hero-note{margin:12px 0}.metrics{flex-direction:row;gap:20px}.metric{width:370px;padding:16px}.metric strong{font-size:84px;line-height:1.1}.metric p{min-height:74px}.callout{margin-top:22px}.step{min-height:100px;padding:14px 20px}.steps{gap:18px}.step p{font-size:32px;line-height:1.5}.case-tag{top:1200px;bottom:auto}.caption{right:200px;bottom:730px;height:160px}.caption span{max-width:760px}.progress-track{right:200px;bottom:660px}.graphic .network{transform:scale(.62);transform-origin:top left;margin-left:80px}.node{font-size:48px}.node span,.edge{font-size:46px}.network .node span{font-size:46px}.question{font-size:200px}.choices{margin-top:12px}.quiet{margin-top:24px}'''
 doc=f'<!doctype html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920"><title>Day {ep["day"]}｜{esc(ep["title"])}</title><script src="assets/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{dur}"><div id="background" class="clip bg" data-start="0" data-duration="{dur}" data-track-index="0"></div>{"".join(parts)}{"".join(captions)}<div class="progress-track"><div id="progress" class="progress"></div></div><audio id="narration" src="assets/narration.wav" data-start="0" data-duration="{dur}" data-track-index="5" data-volume="1"></audio></div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});{"".join(animations)}tl.fromTo("#progress",{{scaleX:0}},{{scaleX:1,duration:{dur},ease:"none"}},0);window.__timelines["main"]=tl;</script></body></html>'
 (folder/'index.html').write_text(doc,encoding='utf-8')
 (folder/'preview.html').write_text(f'''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>Day {ep['day']} 試作播放器</title><style>body{{background:#181818;color:white;font:16px system-ui;margin:0;display:flex;flex-direction:column;align-items:center}}#box{{width:360px;height:640px;overflow:hidden;margin:16px}}iframe{{width:1080px;height:1920px;transform:scale(.3333333);transform-origin:0 0;border:0}}button,input{{margin:8px}}p{{max-width:650px;padding:0 20px}}</style><h2>Day {ep['day']}｜{esc(ep['title'])}</h2><div id="box"><iframe id="film" src="index.html"></iframe></div><div><button id="play">播放／暫停</button><input id="seek" type="range" min="0" max="{dur}" step=".05" value="0"><span id="time">0 / {dur:.1f} 秒</span></div><p>本機試作：教學假設案例。播放時會有繁體中文合成旁白；按暫停可審查文字與圖解。</p><script>const f=document.getElementById('film'),seek=document.getElementById('seek');let playing=false,at=0,stamp=0;function update(t){{const w=f.contentWindow;if(!w.__timelines)return;w.__timelines.main.seek(t);w.document.querySelectorAll('.clip').forEach(e=>{{let s=+e.dataset.start,d=+e.dataset.duration;e.style.opacity=t>=s&&t<s+d?'1':'0'}});seek.value=t;document.getElementById('time').textContent=t.toFixed(1)+' / {dur:.1f} 秒'}}f.onload=()=>update(0);document.getElementById('play').onclick=()=>{{const a=f.contentDocument.getElementById('narration');playing=!playing;if(playing){{if(at>={dur}-.05)at=0;a.currentTime=at;a.play();stamp=performance.now()}}else a.pause()}};seek.oninput=()=>{{at=+seek.value;update(at);f.contentDocument.getElementById('narration').currentTime=at}};function tick(t){{if(playing){{at=f.contentDocument.getElementById('narration').currentTime;update(at);if(at>={dur}-.03)playing=false}}requestAnimationFrame(tick)}}requestAnimationFrame(tick);</script></html>''',encoding='utf-8')

if __name__=='__main__':
 import sys
 prepare() if '--prepare' in sys.argv else finalize()
