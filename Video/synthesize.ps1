param([string]$Manifest = 'episodes.json')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$taskEpisodes = Get-Content -Raw -Encoding utf8 (Join-Path $PSScriptRoot $Manifest) | ConvertFrom-Json
$taskSynth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$taskSynth.SelectVoice('Microsoft Hanhan Desktop')
$taskSynth.Rate = 2
$taskFormat = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(24000, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
foreach ($taskEpisode in $taskEpisodes) {
  for ($taskSceneIndex = 0; $taskSceneIndex -lt $taskEpisode.scenes.Count; $taskSceneIndex++) {
    $taskLines = $taskEpisode.scenes[$taskSceneIndex].lines
    for ($taskLineIndex = 0; $taskLineIndex -lt $taskLines.Count; $taskLineIndex++) {
      $taskName = '{0:D2}-{1:D2}.wav' -f ($taskSceneIndex + 1), ($taskLineIndex + 1)
      $taskOutput = Join-Path $PSScriptRoot ($taskEpisode.slug + '/assets/audio/' + $taskName)
      $taskSynth.SetOutputToWaveFile($taskOutput, $taskFormat)
      $taskSynth.Speak($taskLines[$taskLineIndex])
      $taskSynth.SetOutputToNull()
    }
  }
  Write-Output ('已產生 Day ' + $taskEpisode.day + ' 試作旁白')
}
$taskSynth.Dispose()
