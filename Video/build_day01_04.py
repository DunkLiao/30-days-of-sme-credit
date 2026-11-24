"""沿用既有視覺與旁白流程，只建立 Day 01～04，不重製先前三支影片。"""
from pathlib import Path
import json, shutil, sys
import build_trials as base

ROOT=Path(__file__).resolve().parent
EPISODES=[
 dict(day='01',slug='day01-credit-principles',title='有擔保品，還要問什麼？',topic='資金用途與還款來源',source='Day01.html',anchors=['chapters-heading'],thesis='先問錢用在哪裡，再問靠什麼還回來。',post='有擔保品，仍要查清資金用途與還款來源。把借款需求接回營運與收款，才知道下一步要查什麼。',scenes=[
  dict(label='案件疑問',title='有擔保品',sub='接下來，你會問什麼？',visual='hook',lines=['客戶拿房子作擔保，你就能放心了嗎？接下來要問什麼？']),
  dict(label='教學案例',title='明川公司來借款',sub='以下為虛構教學情境',visual='steps',items=['用途：支付進貨款','還款：等待客戶付款','擔保：提供不動產'],lines=['假設明川公司要借款進貨，說收到客戶貨款就會還錢。','老闆也願意提供不動產擔保。你會先看擔保品，還是先查交易？']),
  dict(label='停一下，先判斷',title='貨款，收得回來嗎？',sub='擔保品之外，還要找什麼證據？',visual='question',lines=['先想一想。預計收回的貨款，什麼時候進來，有什麼依據？']),
  dict(label='拆解觀念',title='把用途接回還款',sub='交易、收款與借款期間要對得上',visual='steps',items=['資金用途：付給誰、做什麼？','還款來源：靠哪筆收入？','時間安排：何時收款還款？'],lines=['先確認錢要付給誰、用在哪筆交易，再查預計還款的來源。','把訂單、出貨與收款條件接起來，核對借款期間是否配合。']),
  dict(label='明天接件就能做',title='讓說法有資料支持',sub='文件核對 → 收款紀錄 → 待查事項',visual='steps',items=['索取採購與銷售文件','核對歷來及預計收款','記錄疑點，依職責交辦'],lines=['索取採購與銷售文件，比對歷來收款紀錄和預計付款日期。','徵信人員客觀揭露疑點，讓權責單位綜合評估。']),
  dict(label='今天帶走一句話',title='先問錢用在哪裡',sub='再問：靠什麼還回來？',visual='closing',lines=['今天記住：先問錢用在哪裡，再問靠什麼還回來。完整練習看第一天課程。'])
 ]),
 dict(day='02',slug='day02-independent-review',title='這句刪掉就好？',topic='徵信報告的客觀與獨立',source='Day02.html',anchors=['sec-drill-title'],thesis='分清事實與說法，重要敘述要有依據。',post='被要求刪掉徵信報告的疑點時，先分清已查證事實、客戶說法與待查事項。重要敘述要有依據。',scenes=[
  dict(label='案件疑問',title='這句，刪掉就好？',sub='遇到報告修改要求，你怎麼做？',visual='hook',lines=['業務說，客戶已經收款，報告裡這句疑點刪掉就好。你會怎麼做？']),
  dict(label='教學案例',title='說法，還沒有佐證',sub='明川公司｜虛構教學情境',visual='steps',items=['報告記載：收款仍待核對','客戶說法：款項已經收到','目前資料：未取得銀行流水'],lines=['假設明川公司說貨款已經收到，但還沒提供銀行流水。','業務希望把收款待核對這句刪掉，讓案件快點往下走。']),
  dict(label='停一下，先判斷',title='說收到，就算確認？',sub='哪個資訊還需要查證？',visual='question',lines=['先停一下。客戶說已收款，和你已核對收款，是同一件事嗎？']),
  dict(label='拆解觀念',title='把資訊分清楚',sub='查證狀態也要如實呈現',visual='steps',items=['事實：手上資料顯示什麼？','說法：誰提供了什麼說明？','待查：還缺哪些佐證？'],lines=['把已查證事實、他人說法與待查事項分開，避免混在一起。','可以補充客戶說明，但取得佐證前，不能寫成已經確認。']),
  dict(label='明天接件就能做',title='先補證，再更新',sub='核對依據，保留修改紀錄',visual='steps',items=['取得收款憑證與銀行流水','核對付款人、金額與日期','更新報告並留下依據'],lines=['請補收款憑證與銀行流水，核對付款人、金額和日期。','依結果更新報告，留存查核與修改依據，並依內部程序處理爭議。']),
  dict(label='今天帶走一句話',title='分清事實與說法',sub='重要敘述，要有依據',visual='closing',lines=['今天記住：分清事實與說法，重要敘述要有依據。完整練習看第二天課程。'])
 ]),
 dict(day='03',slug='day03-credit-aggregation',title='只借一小筆，資料能少收？',topic='歸戶計算與資料表分級',source='Day03.html',anchors=['sec-overview-title','sec-calc-title'],thesis='先確認歸戶範圍，再判斷資料分級。',post='資料表分級先確認歸戶範圍與計算口徑，不能只看本次申請金額。影片算例為教學假設，未設定任何法定門檻。',scenes=[
  dict(label='案件疑問',title='只借一小筆',sub='資料就能少收嗎？',visual='hook',lines=['客戶這次只申請兩百萬元，你就可以直接選最簡單的資料表嗎？']),
  dict(label='教學案例',title='把金額放在一起',sub='明川公司｜假設無適用扣除項',visual='steps',items=['全體金融機構歸戶餘額：1,800 萬','本次申請額度：200 萬','算例合計：2,000 萬元'],lines=['假設明川公司全體金融機構歸戶餘額一千八百萬元，這次申請兩百萬元。','本例假設沒有適用扣除項，合計是兩千萬元。']),
  dict(label='停一下，先判斷',title='這次申請，就是全部？',sub='先找出應計入的範圍',visual='question',lines=['先想一想。你查到的是單一銀行資料，還是完整歸戶範圍？']),
  dict(label='拆解觀念',title='先釐清計算口徑',sub='算清楚，才有分級依據',visual='steps',items=['確認歸戶餘額與查詢時點','核對本次申請及案件性質','逐項確認適用扣除條件'],lines=['先核對歸戶餘額的範圍與查詢時點，再確認本次申請及案件性質。','扣除項要逐項確認適用條件，不能憑印象自行減掉。']),
  dict(label='明天接件就能做',title='算完，再對照分級',sub='本例金額不是法定分級門檻',visual='steps',items=['留存金額與計算依據','對照適用分級及文件要求','疑義依內部程序確認'],lines=['留下金額與計算依據，再對照適用分級和文件要求。','本例只示範加總，不代表兩千萬元就是分級門檻。']),
  dict(label='今天帶走一句話',title='先確認歸戶範圍',sub='再判斷資料分級',visual='closing',lines=['今天記住：先確認歸戶範圍，再判斷資料分級。完整練習看第三天課程。'])
 ]),
 dict(day='04',slug='day04-corporate-identity',title='名稱對了，主體就對了？',topic='法人身分與代表權查核',source='Day04.html',anchors=['overview-heading','chapters-heading'],thesis='查清楚是哪個法人，也查清楚誰能代表它。',post='公司名稱相同，仍需核對法人識別資料、存續狀態與代表權。查清楚是誰借款，也查清楚誰能代表它。',scenes=[
  dict(label='案件疑問',title='公司名稱對了',sub='借款主體，就確認了嗎？',visual='hook',lines=['申請書和文件上的公司名稱一樣，借款主體就確認了嗎？']),
  dict(label='教學案例',title='文件，還差幾個確認',sub='明川公司｜虛構教學情境',visual='steps',items=['名稱：文件上看起來一致','身分：登記識別資料待核對','簽署：經理持有公司印章'],lines=['假設明川公司由經理來送件，帶著公司印章和一份登記資料。','名稱看起來一致，但身分資料與經理的代表權還沒核對。']),
  dict(label='停一下，先判斷',title='有印章，就能代表？',sub='還需要什麼文件支持？',visual='question',lines=['先想一想。拿著印章的人，就一定有權代表公司嗎？']),
  dict(label='拆解觀念',title='分開確認三件事',sub='法人身分、存續狀態、代表權',visual='steps',items=['身分：是哪一個法人？','存續：目前登記狀態如何？','權限：誰能代表或受託？'],lines=['先核對法人識別資料，再查目前登記與存續狀態。','接著確認代表人、授權範圍與相關文件，不能只憑公司名稱或印章。']),
  dict(label='明天接件就能做',title='把文件逐項對上',sub='依註冊地及案件情況確認',visual='steps',items=['核對登記資料與文件日期','確認代表權及授權文件','記錄來源、查核日與缺件'],lines=['依註冊地和案件情況，核對登記、代表權與授權文件。','境外法人另確認適用文件，並記錄查核日期與尚待補齊的項目。']),
  dict(label='今天帶走一句話',title='查清楚是哪個法人',sub='也查清楚誰能代表它',visual='closing',lines=['今天記住：查清楚是哪個法人，也查清楚誰能代表它。完整練習看第四天課程。'])
 ])
]

def prepare():
 base.EPISODES=EPISODES
 base.prepare(ROOT/'episodes01-04.json')
 for ep in EPISODES:
  folder=ROOT/ep['slug']
  for name in ['hyperframes.json','frame.md']:
   shutil.copy2(ROOT/'day05-tax-reconciliation'/name,folder/name)
  package=json.loads((ROOT/'day05-tax-reconciliation/package.json').read_text(encoding='utf-8'))
  package['name']=ep['slug']
  package['scripts']['check']='npx --yes hyperframes@0.9.80 check --safe-zone shorts'
  base.save_json(folder/'package.json',package)

def finalize():
 base.EPISODES=EPISODES; base.finalize()
 for ep in EPISODES:
  folder=ROOT/ep['slug']; notes=folder/'NOTES.md'; text=notes.read_text(encoding='utf-8')
  text=text.replace('明川公司、控股公司、貿易公司及影片所有數字均為新編教學假設，不是真實客戶資料，也不是教材原案例的逐字重現。','本集公司、人物說法、事件及金額均為新編教學假設，不是真實客戶資料，也不是教材原案例的逐字重現。')
  text=text.replace('完整課程：Day'+ep['day']+'.html（實際發布時換成正式網站當日網址）。','完整課程：https://30-days-of-sme-credit.killysss123.workers.dev/Day'+ep['day'])
  source_notes={
   '01':'依據 Day01 第一、第二還款來源與公正平實揭露的課程重點；案例僅示範採購、銷售與收款查證，不宣稱抵押品足夠即可核貸。',
   '02':'依據 Day02 公正平實、徵授信分工及報告語句判讀；本片聚焦事實、客戶說法與待查事項的區分，不替案件表示准駁意見。',
   '03':'依據 Day03 歸戶計算與資料表分級。1,800＋200＝2,000 萬元為虛構新申請算例，假設無適用扣除項；不將算例金額宣稱為法定門檻，也不涵蓋續約借新還舊等特殊處理。',
   '04':'依據 Day04 企業登記事項、法人存續及權責歸屬；補充代表或授權文件的查核問題。不採用未經現行法規驗證的文件時效、費用、境外證書替代或准駁規定。'
  }
  text+='\n## 本集內容依據\n\n'+source_notes[ep['day']]+'\n'
  notes.write_text(text,encoding='utf-8')
  # 延伸既有模板，避免 question 類別把整段場景字體和對齊方式一併套用。
  path=folder/'index.html'; doc=path.read_text(encoding='utf-8')
  doc=doc.replace('class="clip scene question"','class="clip scene question-scene"')
  doc=doc.replace('</style>','.scene{padding-top:300px}.scene-body{padding-top:12px}</style>')
  path.write_text(doc,encoding='utf-8')

if __name__=='__main__':
 prepare() if '--prepare' in sys.argv else finalize()
