# Cybersecurity Endpoint Monitering Scripts

Note :  These scripts were made to simulate endpoint security software in an internship, and they were not meant for production.
[Full Summary of Internship](https://docs.google.com/document/d/1jhU9SXMGFf1c3Zz5HYHwbw_WAN03s8p0dzFoJHufkoE/edit?usp=sharing)

## PowerShell Scripts

For these scripts you will need powershell and you will have to enable running scripts when running.

Steps to enable running powershell scripts

1. Open powershell as administrator
2. Run the following command `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
3. Run script as follows ./'script_name'.ps1

### clipboard_scan.ps1

### datamasking.ps1

### lockout_script.ps1

This script was meant to lockout a person out of their account on an enterprise device, if they enter a wrong password a number of times. This event would be recorded in Event Viewer with event ID 4740 and logs this event in an text file. The number of tries for correct password was set in Windows Group Policy. As the log in Event Viewer is not verbose, I logged an verbose version in a txt file.

## Python Scripts