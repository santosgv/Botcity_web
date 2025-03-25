$exclude = @("venv", "BotWeb.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "BotWeb.zip" -Force