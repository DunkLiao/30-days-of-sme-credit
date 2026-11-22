---
name: maintain-course-site
description: Use when changing this project's index and Day01–Day30 course navigation, home links, favicon, web app manifest, or PWA offline behavior.
---

# 維護 30 天課程網站

靜態網站。入口為 `index.html`，課程頁為 `Day01.html` 至 `Day30.html`；PWA 資源是 `favicon.svg`、`manifest.webmanifest`、`service-worker.js`。先檢查目前檔案，再依使用者當次要求修改，不要假設每個課程頁採用相同 HTML 結構。

## 導覽與外觀

- 首頁課程卡片由 `index.html` 的 JavaScript 產生。標題連結使用兩位數編號對應 `DayXX.html`，保留卡片原有字體與配色，並提供 hover、鍵盤焦點狀態。
- 課程頁的「回首頁」連至同層 `index.html`。目前偏好放在頁腳；使用者若改變位置，以最新要求為準。頁腳結構不一，有些頁面沒有 `.footer-inner`，逐頁確認實際插入位置。
- 導覽文字採用當頁既有的字級和色彩變數。若使用絕對定位，檢查長標題、頁首標籤及窄螢幕是否重疊；能用正常版面流時優先使用。勿把 PowerShell 的字面 `` `r`n `` 寫進 CSS。
- 批次修改前檢查 31 頁的差異；修改後確認每個目標頁面只出現預期數量的連結，且瀏覽器實際呈現與目標位置、顏色相符。文字搜尋無法證明 CSS 正常生效。

## Favicon 與 PWA

- 所有 31 個 HTML 的 `<head>` 都應引用 `favicon.svg`、`manifest.webmanifest`，並在 HTTPS 或 localhost 註冊 `service-worker.js`。保持相對路徑，方便部署在子路徑。
- Manifest 的 `start_url`、`scope`、主題色與圖示須和檔案及站點一致；調整圖示時同步檢查 manifest 和頁面引用。若要提高跨瀏覽器安裝相容性，可依需求補 192/512 px PNG 圖示。
- `service-worker.js` 預先快取首頁、30 頁及本地 PWA 資源。更新離線內容時提升 `CACHE_NAME` 版本，讓既有安裝取得新的預快取；不要讓單一缺失檔案使 `cache.addAll` 的安裝失敗。外部字型或 CDN 依賴不保證離線可用，宣稱完整離線功能前應在瀏覽器檢查。
- 用本地 HTTP 伺服器或正式 HTTPS 網址檢查安裝與離線導覽；`file://` 無法驗證 Service Worker。確認首頁與至少一個課程頁可離線開啟，並在連線恢復後載入更新內容。

完成時簡述修改的頁面範圍、實際驗證結果，以及未驗證的瀏覽器或離線情況。