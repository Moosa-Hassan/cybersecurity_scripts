Write-Output "Running...."
# get regular expressions of various sensative info
$email = '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
$creditCard = '\b(?:\d{4}-\d{4}-\d{4}-\d{4}|\d{16})\b'
$creditCard2 = '\b(?:\d{4})\b'
# specific keywords which could be data leak


$previous = ""
while ($true){
    #get contents of clipboard
    $contents = Get-Clipboard
    # to store previous clipboard entry so we dont keep checking again
    # if contents were already redacted skip iteration
    # if there are contents and have changed
    if ($null -ne $contents -and $contents -ne $previous){
       # Split by newline characters but keep them intact
        $lines = $contents -split "`r`n|`n|`r"
        $redactedLines = @()
        foreach ($line in $lines){
            $parts = [regex]::Split($line, "(\s+)")
            for ($i = 0 ; $i -lt  $parts.Count; $i++){
                if ($parts[$i] -match $email){
                    $emailPart = $parts[$i].Split('@')
                    #this masks the email
                    if ($emailPart[0].Length -gt 1){
                        $maskedLocal = $emailPart[0][0] + ('*' * ($emailPart[0].Length-1))
                        $parts[$i] = "$maskedLocal@$($emailPart[1])"
                    }
                    elseif ($emailPart[0].Length -eq 1){
                        $maskedLocal = "****"
                        $parts[$i] = "$maskedLocal@$($emailPart[1])"
                    }
                }
                if ($parts[$i] -match $creditCard){
                    #removes all spaces and alphabets then extracts last4 digits and then creates replacement text
                    $digits = $parts[$i] -replace '\D',''
                    $last4 = $digits.Substring($digits.Length-4)
                    $ReplacemnetText = 'XXXX XXXX XXXX '+ $last4
                    $parts[$i] = $ReplacemnetText
                }
                if ($parts[$i] -match $creditCard2){
                    if ($parts[$i+2] -match $creditCard2 -and $parts[$i+4] -match $creditCard2 -and $parts[$i+6] -match $creditCard2){
                        $parts[$i+4] = "XXXX"
                        $parts[$i+2] = "XXXX"
                        $parts[$i] = "XXXX"
                        $i = $i + 6
                    }
                }
            }
            $redactedLines += ($parts -join '')
        }
        $newText = $redactedLines -join "`n"
        Set-Clipboard -Value $newText
        $previous = $contents
    }
    Start-Sleep -seconds 1
}