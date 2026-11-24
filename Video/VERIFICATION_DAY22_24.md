# Day 22～24 影片驗證紀錄

日期：2026-11-23。沿用案例判斷＋圖解、繁體字幕與 Microsoft Hanhan Desktop 本機合成旁白，無配樂。

| 影片 | 長度 | 尺寸 | 影音 |
|---|---|---|---|
| [Day22.mp4](Day22.mp4) | 58.12 秒 | 1080 × 1920 | H.264 / AAC、24 fps |
| [Day23.mp4](Day23.mp4) | 58.42 秒 | 1080 × 1920 | H.264 / AAC、24 fps |
| [Day24.mp4](Day24.mp4) | 58.67 秒 | 1080 × 1920 | H.264 / AAC、24 fps |

## 已完成檢查

- HyperFrames check：程式、版面、動態、對比、音訊；安全區涵蓋 Reels 與 Shorts。
- 每支六段的中間時間點均擷取並檢視畫面，見各集 snapshots/contact-sheet.jpg。
- MP4 全片解碼成功；包含視訊與音訊軌，且時長與 WAV 一致。
- WAV 有聲音訊號，字幕依序、無重疊且未超過影片長度。
- 每集保留 SCRIPT.md、STORYBOARD.md、NOTES.md、captions.srt 與可重製來源。
- 內容使用教學假設案例；本批採新編虛構案例。Day22 為賒銷批發情境，不代表所有零售業態。Day23 假設收入已依適用會計處理認列；合約資產仍附時間經過以外的收款條件。Day24 不把發票等同交易已全部查證，不宣告無追索權一律免責；責任依個案契約與適用程序確認。

## 限制與後續

合成語音尚待使用者聽取回饋；句內字幕按字數分配，未宣稱人工逐字校時。尚未代為上傳或發布。

### Day 22

- lint：0 錯誤、7 提示（nested_structure_needs_subcomposition、timeline_track_too_dense）。
- runtime：0 錯誤、0 提示。
- layout：0 錯誤、0 提示（content_overlap）。
- motion：0 錯誤、0 提示。
- contrast：0 錯誤、0 提示。
- craft：0 錯誤、0 提示。
- audio：0 錯誤、0 提示。
### Day 23

- lint：0 錯誤、7 提示（nested_structure_needs_subcomposition、timeline_track_too_dense）。
- runtime：0 錯誤、0 提示。
- layout：0 錯誤、0 提示。
- motion：0 錯誤、0 提示。
- contrast：0 錯誤、0 提示。
- craft：0 錯誤、0 提示。
- audio：0 錯誤、0 提示。
### Day 24

- lint：0 錯誤、7 提示（nested_structure_needs_subcomposition、timeline_track_too_dense）。
- runtime：0 錯誤、0 提示。
- layout：0 錯誤、0 提示。
- motion：0 錯誤、0 提示。
- contrast：0 錯誤、0 提示。
- craft：0 錯誤、0 提示。
- audio：0 錯誤、0 提示。

已檢視提示；單檔場景結構與字幕軌密度提示不影響本批輸出。
