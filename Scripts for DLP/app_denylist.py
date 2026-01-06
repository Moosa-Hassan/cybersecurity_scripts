import psutil
import time
import os
import signal # signal constants to send signals to os
from winotify import Notification # for alerts
import hashlib # for hashing files

TARGETS = ["notepad.exe","msiexec.exe"]
TARGETS_WITH_ARGS = [["msedge.exe","inprivate"]]

TARGET_HASHES = ["9F18169DEC88597AB59FF216B308A6C303F58814A545872A82966168E1AC616C","F87BF57756049015686B7769B5A8DB32026D310BF853E7D132424F7513FE316C","CF378B9BF51F692844584C3B2689D36DCB0CB8BD3769B122DACDF492A44CED1D","BAAAE8DD14A26D827E0E8E6CFD953858E0BB2E556D295543D0B1E3DB86FFAA13"]
all_targets  = TARGETS + [t[0] for t in TARGETS_WITH_ARGS] # flatten list of targets with args to just exe names
print(f"Monitoring for {all_targets}... Press Ctrl+C to stop.")

def notify(target):
    """ Sends a Windows notification that target was blocked """
    toast = Notification(
        app_id="App Denylist",
        title="Process Blocked",
        msg=f"{target} was blocked and terminated.",
    )
    toast.show()
    
def hash_file(filepath):
    """
    Returns SHA256 hash of the file passed into it
    """
    try :
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(4096):
                file_hash.update(chunk)
            return file_hash.hexdigest().upper()
    except Exception as e:
        # print(f"Error hashing file: {e}")
        return None

def substring_sreach(substring, string):
    """
    Returns True if substring is found in string, else False
    Case insensitive
    """
    print(substring.lower())
    print(string.lower())
    return substring.lower() in string.lower()

def cmdline_compare(target_hash,cmdlist):
    """
    Compares each item in cmdlist to see if its hash matches target_hash
    """
    if cmdlist:
        for item in cmdlist:
            if os.path.exists(item):
                if target_hash == hash_file(item):
                    return True
    return False


try:
    while True:
        for proc in psutil.process_iter(['pid', 'name','exe','cmdline']):# gets all processes with their name and PID
            if proc.info['name'] not in all_targets: # if a process is not a target,
                continue
            for HASH in TARGET_HASHES: # compares hashes
                if proc.info['name'] and (HASH == hash_file(proc.info['exe']) or cmdline_compare(HASH,proc.info['cmdline'])): # if target is running and compare via hash
                    name = proc.info['name']
                    if name  and name.lower() in (t.lower() for t in TARGETS):# first checks no argument targets
                        # print(f"[BLOCKED] {name} detected, killing PID {proc.info['pid']}")
                        os.kill(proc.info['pid'], signal.SIGTERM) # killed the process
                        notify(name) 
                    else: 
                        for target in TARGETS_WITH_ARGS:
                            if name and name.lower() == target[0].lower():
                                cmd_string = ' '.join(proc.info['cmdline']).lower()
                                for arg in target[1:]: # skips the exe name
                                    if substring_sreach(arg, cmd_string):
                                        # print(f"[BLOCKED] {name} with argument {arg} detected, killing PID {proc.info['pid']}")
                                        os.kill(proc.info['pid'], signal.SIGTERM) 
                                        notify(name)                             
        time.sleep(1)
except KeyboardInterrupt: # to stop the script
    print("Stopped monitoring.")
except Exception as e: # to see any other errors
    print(f"Error Encountered: {e}")
