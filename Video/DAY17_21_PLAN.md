# Day 17～21 製作紀錄

日期：2026-11-23。延續既有奶油白與鈷藍、六段式案例判斷，銀行徵授信新手為觀眾。直式 1080 × 1920、24 fps、45～60 秒、繁體字幕、Microsoft Hanhan Desktop 本機合成旁白，無配樂。

| 集數 | 核心問題 | 查核動作 |
|---|---|---|
| 17 | 加回折舊等於現金到帳嗎？ | 指標接回營運資金、設備支出與本息時點 |
| 18 | 營業現金流全部能還債嗎？ | 明列扣資本支出及股利的口徑，避免利息重複扣減 |
| 19 | 同業基準選對了嗎？ | 核對行業、規模、年度、準則與報表範圍 |
| 20 | 高於平均就安全嗎？ | 分布落點接回帳齡、回收、受限及商業模式 |
| 21 | 長週轉等於滯銷嗎？ | 追查設備位置、交付驗收條件與收款進度 |

教材為根目錄 Day17.html～Day21.html；不引用通用准駁門檻或未驗證的最新統計。所有案例均為新編虛構情境。

## 重製

```powershell
python Video/build_day17_21.py --prepare
powershell -NoProfile -ExecutionPolicy Bypass -File Video/synthesize.ps1 -Manifest episodes17-21.json
python Video/build_day17_21.py
```

各集執行 `npm run check -- --json`，擷取六段中間畫面並檢視後：

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File Video/render_day01_04.ps1 -Manifest episodes17-21.json
python Video/verify_day17_21.py
```

## 執行清單

- [x] 核對五日教材、既有規劃與文案，完成腳本。
- [x] 產生配音、字幕與六段分鏡，確認時長。
- [x] 完成程式、版面、對比、安全區、音訊及字幕節奏檢查。
- [x] 擷取並檢視五集六段畫面。
- [x] 輸出 Day17.mp4～Day21.mp4。
- [x] 驗證全片解碼、影音格式、時長及字幕時間。
- [x] 更新 TODO、播放入口、文案狀態與驗證紀錄。

五支均已完成各六段畫面檢視；全片解碼、H.264／AAC、1080 × 1920、24 fps、時長及字幕時間驗證均通過。詳見 [本批驗證紀錄](VERIFICATION_DAY17_21.md)。保留單檔場景結構與字幕軌密度提示，無檢查錯誤；合成語音與句內字幕仍待人工觀看回饋。
