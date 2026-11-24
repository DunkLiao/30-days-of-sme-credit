param([string]$Manifest = 'episodes01-04.json')
$ErrorActionPreference = 'Stop'
$taskEpisodes = Get-Content -Raw -Encoding utf8 (Join-Path $PSScriptRoot $Manifest) | ConvertFrom-Json
if (Test-Path -LiteralPath 'C:/Program Files/Google/Chrome/Application/chrome.exe') {
  $env:HYPERFRAMES_BROWSER_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
}
foreach ($taskEpisode in $taskEpisodes) {
  $taskFolder = Join-Path $PSScriptRoot $taskEpisode.slug
  $taskReportFile = Get-ChildItem -LiteralPath (Join-Path $taskFolder '.hyperframes/artifacts/checks') -Filter '*.json' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if (-not $taskReportFile) { throw ('Missing check report: Day ' + $taskEpisode.day) }
  $taskReport = Get-Content -Raw -Encoding utf8 $taskReportFile.FullName | ConvertFrom-Json
  if (-not $taskReport.ok -or $taskReportFile.LastWriteTime -le (Get-Item -LiteralPath (Join-Path $taskFolder 'index.html')).LastWriteTime) {
    throw ('Check not current or not passing: Day ' + $taskEpisode.day)
  }
  Push-Location -LiteralPath $taskFolder
  try {
    $taskPreviousPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    npm run render -- --quality draft --fps 24 --output ('../Day' + $taskEpisode.day + '.mp4') *> render.log
    $taskRenderExit = $LASTEXITCODE
    $ErrorActionPreference = $taskPreviousPreference
    if ($taskRenderExit -ne 0) { Get-Content render.log -Tail 20; throw ('Render failed: Day ' + $taskEpisode.day) }
    Write-Output ('Rendered Day ' + $taskEpisode.day)
  } finally { Pop-Location }
}
