# Cybersecurity Endpoint Monitering Scripts

Note :  These scripts were made to simulate endpoint security software in an internship, and they were not meant for production.
[Full Summary of Internship](https://docs.google.com/document/d/1jhU9SXMGFf1c3Zz5HYHwbw_WAN03s8p0dzFoJHufkoE/edit?usp=sharing)

## PowerShell Scripts

For these scripts you will need powershell and you will have to enable running scripts when running.

Steps to enable running powershell scripts

1. Open powershell as administrator
2. Run the following command (allows execution of script on that instance of powershell only) `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
3. Run script as follows ./'script_name'.ps1

### clipboard_scan.ps1

Leaking sensative information can be as easy as copying it from one place and pasting it in another location. Any copied file is first stored in clipboard then pasted to the location. Hence, this scripts tries to prevent sharing of emails, credit card nubers and some copied text with keywords in an effort to stop leakage of data. The script will have check clipboard every second and if sensative information is detected, it will be replaced. This scripts will have false positives especially in sensative keyword match.

### datamasking.ps1

This works in the same fashion as the clipboard_scan script but it masks data instead of replacing with a text. This is for reducing the number of false positives in a way that data would be copied, but improtant part would be redacted.

### lockout_script.ps1

This script was meant to log when a person is locked out of their account on an enterprise device, if they enter a wrong password a number of times. This event would be recorded in Event Viewer with event ID 4740 and logs this event in an text file. The number of tries for correct password was set in Windows Group Policy. As the log in Event Viewer is not verbose, I logged an verbose version in a txt file.

## Python Scripts (Scripts for DLP(Data Loss Prevention))

These scripts were made to more deeply understand how DLP softwares prevent data loss.

### app_denylist.py

### context_aware.py

### local_monitering.py

### metadata_analaysis.py

### OCR_Detection.py

Sometimes text data is in PDF or photo files, which makes search of sensative information on it hard. Hence we use an Optical Character Recognization (OCR) software to extract all text from files and check for keywords and regex match in that text.

### upload_monitering.py