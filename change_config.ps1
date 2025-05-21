$directoryPath = "configs/"

Get-ChildItem -Path $directoryPath -Filter *.json | ForEach-Object {
    $file = $_.FullName
    Write-Host "Updating: $file"

    $json = Get-Content $file -Raw | ConvertFrom-Json

    $json.forecast_days = Get-Random -Minimum 4 -Maximum 30

    if (-not (Get-Member -InputObject $json -Name "lookback_days" -MemberType Properties)) {
        $json | Add-Member -MemberType NoteProperty -Name "lookback_days" -Value $null
    }
    $json.lookback_days = Get-Random -Minimum 4 -Maximum 30

    $updatedJson = $json | ConvertTo-Json -Depth 10

    $updatedJson | Set-Content -Path $file -Encoding UTF8
}