# week1/failed_logons.ps1
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 500 -ErrorAction SilentlyContinue |
ForEach-Object {
    $x = [xml]$_.ToXml()
    $d = @{}
    $x.Event.EventData.Data | ForEach-Object { $d[$_.Name] = $_.'#text' }
    [pscustomobject]@{ Time = $_.TimeCreated; User = $d['TargetUserName']; IP = $d['IpAddress'] }
} | Group-Object IP | Sort-Object Count -Descending |
  Select-Object Count, Name -First 10