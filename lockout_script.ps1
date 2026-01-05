# Getting the event based on Event Id  4740 which is the id for lockout event
# event is variable, Get-WinEvent gets and event, 
#Filters by security log and log with id 4740 and lists max of 1 entries
$event = Get-WinEvent -MaxEvents 1 -FilterHashTable @{LogName="Security";Id=4740}

$message = $event.message
$time = $event.TimeCreated

# using regular epression as two Account name fields
if ($message -match "Account That Was Locked Out:\s+.*\n.*Account Name:\s+(\S+)" ) {
    $username = $matches[1]

    # Disabling the user
    Disable-LocalUser -Name $username 

    # log message 
    $log = @"
[$time]
Lockout Event for user: $username
Action Taken: Account disabled
Event Message:
$message
-----------------------------------------------------
"@

    # Write to Documents/lockout_log.txt
    $logPath = "$env:USERPROFILE\Documents\lockout_log.txt"
    Add-Content -Path $logPath -Value $log
}
else {
    $log = @"
[$time]
Lockout Event for user: Could not be determined
Action Taken: None (Immediately Take action)
Event Message:
$message
-----------------------------------------------------
"@

    # Write to Documents/lockout_log.txt
    $logPath = "$env:USERPROFILE\Documents\lockout_log.txt"
    Add-Content -Path $logPath -Value $log
}