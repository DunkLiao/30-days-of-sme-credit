# Day 26～30 製作紀錄

日期：2026-11-24。延續既有奶油白與鈷藍、六段式案例判斷。觀眾為銀行徵授信新手；直式 1080 × 1920、24 fps、45～60 秒，繁體字幕、本機 Microsoft Hanhan Desktop 旁白，無配樂。

| 集數 | 核心問題 | 查核動作 |
|---|---|---|
| 26 | 股東往來，是誰借誰錢？ | 方向、用途、條件與回收 |
| 27 | 老闆說法不同，怎麼查？ | 時間與範圍對齊，分開說法、證據、待查 |
| 28 | 聯徵有變化，就下結論？ | 核對欄位、日期、額度、餘額與繳款趨勢 |
| 29 | 公司說滿載，現場怎麼查？ | 交叉核對、記錄觀察範圍與補查事項 |
| 30 | 資料齊了，結論怎麼寫？ | 串連用途、還款來源、風險與未確認事項 |

教材為根目錄 Day26.html～Day30.html。案例均為新編虛構情境；不宣告通用法規門檻、逐位信用代碼、准駁結論或自動免責。

## 重製

```powershell
python Video/build_day26_30.py --prepare
powershell -NoProfile -ExecutionPolicy Bypass -File Video/synthesize.ps1 -Manifest episodes26-30.json
python Video/build_day26_30.py
```

各集執行 `npm run check -- --json`，擷取並檢視各六段畫面後：

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File Video/render_day01_04.ps1 -Manifest episodes26-30.json
python Video/verify_day26_30.py
```

## 執行清單

- [x] 核對五日教材、規劃及 YouTube 文案，完成腳本。
- [x] 產生配音、繁體字幕及六段分鏡，確認片長。
- [x] 完成程式、版面、安全區、對比、音訊及字幕節奏檢查。
- [x] 擷取並檢視五集各六段畫面。
- [x] 輸出 Day26.mp4～Day30.mp4。
- [x] 完成全片解碼、影音格式、時長及字幕時間驗證。
- [x] 更新 TODO、播放入口、文案狀態與驗證紀錄。

Day28 縮短問句標題並調整提示間距，已重驗確認沒有遮擋。Day29～30 縮短換行不順的標題，重驗與畫面複核已完成。五支全片解碼、格式、時長與字幕時間均通過，詳見 [驗證紀錄](VERIFICATION_DAY26_30.md)。保留單檔場景結構與字幕軌密度提示，無檢查錯誤；合成語音與句內字幕仍待人工觀看回饋。
