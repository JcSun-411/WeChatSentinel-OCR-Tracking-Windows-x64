$ErrorActionPreference = 'Stop'
$key = 'HKCU:\Software\Classes\AppUserModelId\Local.WeChatSentinel'
New-Item -Path $key -Force | Out-Null
New-ItemProperty -Path $key -Name DisplayName -PropertyType String -Value 'WeChat Sentinel' -Force | Out-Null
Write-Host 'WeChat Sentinel notification identity registered for the current user.'
