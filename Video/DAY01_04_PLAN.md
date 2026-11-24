# Day 01～04 製作紀錄與執行清單

日期：2026-11-22。依使用者要求製作四支影片並更新 TODO，沿用已選定的案例判斷＋圖解格式。

## 製作規格

1080 × 1920、直式 9:16、24 fps、目標 45～60 秒、繁體中文字幕與本機 Microsoft Hanhan Desktop 旁白。沿用奶油白、鈷藍及六段式案例結構，不加配樂。

## 本批主題與依據

| 集數 | 案例 | 核心動作 | 教材 |
|---|---|---|---|
| Day 01 | 有擔保品，仍需查交易與收款 | 核對用途、還款來源與時間 | Day01.html 的第一、第二還款來源與客觀揭露 |
| Day 02 | 客戶說已收款，業務要求刪除待查事項 | 分清事實、說法與待查，補證後更新 | Day02.html 公正平實與報告語句判讀 |
| Day 03 | 歸戶餘額 1,800 萬，加申請 200 萬 | 確認歸戶、案件性質與適用扣除條件 | Day03.html 歸戶計算與分級 |
| Day 04 | 經理持公司印章來送件 | 核對法人、存續與代表／授權文件 | Day04.html 企業登記與權責歸屬 |

所有案件為新編教學假設。Day03 假設無適用扣除項，2,000 萬元僅為加總結果，不代表法定門檻。其他集數也不加入未核實的法律時效或文件豁免斷言。

## 檔案與執行

- `build_day01_04.py`：四集內容與本批產生器，使用既有 `build_trials.py` 的畫面與時間軸工具。
- `episodes01-04.json`：本批旁白輸入，與原三集的 episodes.json 分開。
- `day01-credit-principles/` 至 `day04-corporate-identity/`：各集畫面、旁白、分鏡、來源、字幕與檢查產物。
- `Day01.mp4` 至 `Day04.mp4`：交付影片。
- `verify_day01_04.py`、`VERIFICATION_DAY01_04.md`：本批輸出驗證與紀錄。

重製命令（在專案根目錄執行）：

```powershell
python Video/build_day01_04.py --prepare
powershell -NoProfile -ExecutionPolicy Bypass -File Video/synthesize.ps1 -Manifest episodes01-04.json
python Video/build_day01_04.py
```

接著在各集資料夾執行 `npm run check -- --json`，擷取六段中間畫面並檢視，再執行 `npm run render -- --quality draft --fps 24 --output ../DayXX.mp4`（XX 改為該集兩位數）。最後回專案根目錄執行 `python Video/verify_day01_04.py`。

## 執行清單

- [x] 查讀四日教材並對照已擬定的 YouTube 文案。
- [x] 完成四集案例、旁白與六段分鏡。
- [x] 產生逐句旁白、字幕及可編輯畫面來源。
- [x] 完成檢查與六段畫面檢視。
- [x] 輸出 Day01.mp4 至 Day04.mp4。
- [x] 驗證影片、音訊、字幕與時長，保存本批驗證紀錄。
- [x] 更新影片播放入口與 TODO，分開記錄影片完成及發布狀態。
