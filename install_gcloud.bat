@echo off

REM Check if gcloud is installed
where gcloud > nul
if %errorlevel% NEQ 0 (
  REM Download the Google Cloud SDK installer
  powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe', 'gcloud-installer.exe')"

  REM Run the Google Cloud SDK installer
  gcloud-installer.exe /S

  REM Add the Google Cloud SDK to the PATH
  setx PATH "%PATH%;%ProgramFiles(x86)%\Google\Cloud SDK\google-cloud-sdk\bin"
)
