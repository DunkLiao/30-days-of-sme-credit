# 試作驗證結果

日期：2026-11-22。實際讀取 MP4、WAV、SRT 及最新 HyperFrames 檢查報告。

| 試作 | 影片長度 | 尺寸 | 聲音 | 檔案大小 |
|---|---|---|---|---|
| Day 05 | 59.46 秒 | 1080 × 1920 | 有 | 2.18 MB |
| Day 16 | 57.54 秒 | 1080 × 1920 | 有 | 2.17 MB |
| Day 25 | 55.12 秒 | 1080 × 1920 | 有 | 2.16 MB |

## 驗證範圍

- 三支最新 HyperFrames check 均通過，檢查涵蓋程式、版面、對比、動態及音訊。安全區以本案指定的 Instagram Reels 為準。
- 逐句音訊非靜音；字幕依序且未超出音訊，影片包含視訊與音訊軌。
- 影片長度與旁白時間軸一致；皆為 45～60 秒。
- 已抽查每支多個時間點的畫面，聯絡表置於各專案 snapshots/contact-sheet.jpg；另抽查 MP4 實際輸出畫面。
- MP4 為本輪 draft 試作輸出，1080 × 1920、24 fps、H.264 / AAC。
- 本輪配音為本機合成語音，字幕句內時間依字數估計；未做人工聽打逐字校時。

## 檢查提示

### Day 05

- lint：0 錯誤、7 提示（nested_structure_needs_subcomposition、timeline_track_too_dense）。
- runtime：0 錯誤、0 提示。
- layout：0 錯誤、0 提示。
- motion：0 錯誤、0 提示。
- contrast：0 錯誤、0 提示。
- craft：0 錯誤、0 提示。
- audio：0 錯誤、0 提示。
### Day 16

- lint：0 錯誤、7 提示（nested_structure_needs_subcomposition、timeline_track_too_dense）。
- runtime：0 錯誤、0 提示。
- layout：0 錯誤、0 提示。
- motion：0 錯誤、0 提示。
- contrast：0 錯誤、0 提示。
- craft：0 錯誤、0 提示。
- audio：0 錯誤、0 提示。
### Day 25

- lint：0 錯誤、7 提示（nested_structure_needs_subcomposition、timeline_track_too_dense）。
- runtime：0 錯誤、0 提示。
- layout：0 錯誤、0 提示。
- motion：0 錯誤、0 提示。
- contrast：0 錯誤、0 提示。
- craft：0 錯誤、0 提示。
- audio：0 錯誤、0 提示。

提示已逐類檢視。單一 HTML 的場景結構與字幕軌較密，仍可完整播放與修改；如有 safe-zone 提示，應以各平台實際發布介面再預覽。原課程頁未修改。
