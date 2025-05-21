$folderPath = "configs/"
Get-ChildItem -Path $folderPath -Filter *.json | ForEach-Object {
    $filePath = $_.FullName
    $jsonContent = Get-Content $filePath -Raw
    $json = $jsonContent | ConvertFrom-Json

    if (-not $json.PSObject.Properties.Match("estimator_strategy").Count -gt 0) {
        $choices = @("mom", "ml", "mse")
        $randomChoice = Get-Random -InputObject $choices
        $json | Add-Member -MemberType NoteProperty -Name "estimator_strategy" -Value $randomChoice
        $json | ConvertTo-Json -Depth 10 | Set-Content -Path $filePath
        Write-Host "Added estimator_strategy to: $filePath"
    } else {
        Write-Host "Already has max_age: $filePath"
    }
}
