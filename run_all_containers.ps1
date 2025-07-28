$collections = Get-ChildItem -Directory | Where-Object { $_.Name -like "Collection *" }

foreach ($folder in $collections) {
    $containerPath = "/app/$($folder.Name)"
    Write-Host "🔄 Processing $($folder.Name)..."
    
    docker run --rm `
        -v "$($folder.FullName):$containerPath" `
        adobe1b
}

Write-Host "✅ Done processing all collections."
