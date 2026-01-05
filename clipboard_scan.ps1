
# get regular expressions of various sensative info
$email = '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
$creditCard = '\b(?:\d[ -]*?){13,16}\b'
# specific keywords which could be data leak
$sensitiveKeywords = @(
    # credentials
    "password", "pass", "passwd", "secret", "token", "key", "apikey", "api_key", "auth", "authorization", "sessionid", "access_token", "cookie_value"
    # Financial Information
    "creditcard", "ccnum", "cardnumber", "iban number", "routing", "ifsc", 
    # encryption
    "privatekey", "publickey", "certificate", "pem", "pfx", "keystore", "rsa", "aes", "encryption", "private key",
    # Buisness secrets
    "internal", "confidential", "restricted", "do not share", "classified", "root"
)
# test to 
$ReplacemnetText = "Sensitive Information detected and redacted"

while ($true){
    #get contents of clipboard
    $contents = Get-Clipboard
    # to store previous clipboard entry so we dont keep checking again
    $previous = ""
    # if contents were already redacted skip iteration
    if ($contents -eq $ReplacemnetText) { continue }
    # if there are contents and have changed
    if ($contents -ne $null -and $content -ne $previous){
        # if content match email or credit card info
        if ($contents -match $email -or $contents -match $creditCard){
            Set-Clipboard -value $ReplacemnetText
        }
        # if they contain any sensative info words
        foreach ($word in $sensitiveKeywords){
            if ($contents -match "(?i)\b$pattern\b"){
                Set-Clipboard -value $ReplacemnetText
                break
            }
        }
        $previous = $contents
    }
    Start-Sleep -seconds 1
}