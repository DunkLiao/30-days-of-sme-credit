# Day 11～15 製作紀錄

日期：2026-11-23。延續案例判斷＋圖解、奶油白與鈷藍、繁體字幕與本機合成旁白；直式 1080 × 1920、24 fps、目標 45～60 秒，無配樂。

## 主題與查核重點

| 集數 | 重點 | 教材與編輯範圍 |
|---|---|---|
| 11 | 先對版本與範圍，再追數字差異 | Day11 正副本比對、期間、版本、個體與合併範圍；差異不直接等同造假 |
| 12 | 先確認資格，再確認簡化範圍 | Day12 適用資格及必要文件；不宣告通用門檻或豁免 |
| 13 | 串連實數、比率與比較 | Day13 三鏈分析；回到資金用途、收款與待查事項 |
| 14 | 比較營收與應收的不相稱變動 | Day14 前後期年增率；核對口徑、帳齡、合約與期後收款 |
| 15 | 檢查資產品質及可用時點 | Day15 應收、存貨、受限資金及付款安排；不一律剔除特定科目 |

Day14 的假設為兩年全年營收 1,000→1,200 萬元、兩年各期末應收 200→400 萬元，年增率分別為 20% 與 100%。這是相鄰兩期的變動比較，不稱為固定基期的多年趨勢，亦不是准駁門檻。

## 製作與重製

內容來源為 `episodes11_15_source.json`。`build_day11_15.py` 使用已驗證的共用建置與字幕流程，不重製既有影片。

在專案根目錄執行：

```powershell
python Video/build_day11_15.py --prepare
powershell -NoProfile -ExecutionPolicy Bypass -File Video/synthesize.ps1 -Manifest episodes11-15.json
python Video/build_day11_15.py
```

在各集資料夾執行 `npm run check -- --json`，擷取並檢視六段中間畫面後，再從根目錄執行：

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File Video/render_day01_04.ps1 -Manifest episodes11-15.json
python Video/verify_day11_15.py
```

各集保留來源紀錄、SCRIPT.md、STORYBOARD.md、captions.srt、配音、畫面與檢查產物。

## 執行清單

- [x] 核對教材、系列規劃與 YouTube 文案，完成五集腳本。
- [x] 產生配音、繁體字幕與六段分鏡，片長落在一分鐘內。
- [x] 完成程式、版面、動態、字級、對比、音訊與 Shorts 安全區檢查。
- [x] 擷取並檢視五集各六段畫面。
- [x] 輸出 Day11.mp4 至 Day15.mp4。
- [x] 完成全片解碼、影音格式、時長與字幕時間驗證。
- [x] 更新 TODO、播放入口、文案狀態與本批驗證紀錄。

Day 11 已合併停留過短的字幕，重驗後 craft 無提示。五支最終輸出均通過解碼、格式、時長與字幕檢查，詳見 [驗證紀錄](VERIFICATION_DAY11_15.md)。
