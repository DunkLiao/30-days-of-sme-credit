# Day 22～24 製作紀錄

日期：2026-11-23。沿用奶油白與鈷藍、六段式案例判斷；觀眾為銀行徵授信新手。直式 1080 × 1920、24 fps、45～60 秒、繁體字幕、本機 Microsoft Hanhan Desktop 旁白，無配樂。

| 集數 | 核心問題 | 查核重點 |
|---|---|---|
| 22 | 每天有生意，為何仍缺錢？ | 進貨付款、庫存與賒銷收款的時間差 |
| 23 | 工程收入有了，何時收到錢？ | 收款條件、工程進度、驗收、請款與期後收款 |
| 24 | 只有發票，承購還要查誰？ | 真實交易、履約、買方付款與契約追索安排 |

以根目錄 Day22.html～Day24.html 為教材，案例均為新編虛構情境。Day22 不引入教材未提供的 POS／電子支付細則；Day23 不將所有施工直接等同可認列收入；Day24 不宣告無追索權一律免責或統一追索結果。

## 重製

```powershell
python Video/build_day22_24.py --prepare
powershell -NoProfile -ExecutionPolicy Bypass -File Video/synthesize.ps1 -Manifest episodes22-24.json
python Video/build_day22_24.py
```

各集執行 `npm run check -- --json`，擷取並檢視六段畫面後：

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File Video/render_day01_04.ps1 -Manifest episodes22-24.json
python Video/verify_day22_24.py
```

## 執行清單

- [x] 核對教材、規劃與文案，完成三集腳本。
- [x] 產生旁白、字幕與分鏡，確認片長。
- [x] 完成程式、版面、安全區、對比、音訊與字幕節奏檢查。
- [x] 擷取並檢視各集六段畫面。
- [x] 輸出 Day22.mp4、Day23.mp4、Day24.mp4。
- [x] 完成全片解碼、影音格式、時長及字幕時間驗證。
- [x] 更新 TODO、播放入口、文案狀態與驗證紀錄。

Day23 已合併短字幕，Day24 買方標示修為「付款義務人」，兩集重驗及畫面複核均完成。三支全片解碼、H.264／AAC、1080 × 1920、24 fps、片長及字幕時間檢查均通過；詳見 [驗證紀錄](VERIFICATION_DAY22_24.md)。保留單檔場景結構與字幕軌密度提示，無檢查錯誤；合成語音與句內字幕節奏仍待人工觀看回饋。
