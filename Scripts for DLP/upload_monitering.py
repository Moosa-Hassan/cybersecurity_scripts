import win32gui
import win32con
import win32api
import ctypes
import time
import os, glob
import OCR_Detection as ocr

# Windows API call to get text from a control
def get_window_text(hwnd):
    length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0) # gets length of content
    buf = ctypes.create_unicode_buffer(length + 1) # makes a buffer to hold the text
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, length + 1, buf)# stores the text in the buffer
    return buf.value

def enum_child_windows(parent):
    """Returns a list of child window handles for the given parent window."""
    result = []
    def callback(hwnd, _):
        result.append(hwnd)
    win32gui.EnumChildWindows(parent, callback, None)
    return result

def enum_handler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        # Get the window title and class name
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        full_path = None

        if class_name == "#32770":  # filters so only file dialog is worked on
            print(f"[UPLOAD SIGNAL] File dialog detected: '{title}'")

            # Find children (like Edit boxes, buttons)
            children = enum_child_windows(hwnd)
            folder_path = None
            file_name = None
            for child in children:
                # print(f"Child HWND: {child}, Class: {win32gui.GetClassName(child)}, Text: {get_window_text(child)}")
                try : 
                    # Get text and class name of the child window
                    child_text = get_window_text(child)
                    child_class = win32gui.GetClassName(child)

                    # File name
                    if child_class == "Edit" and child_text:
                        # print(f"[SELECTED FILE] {child_text}")
                        file_name = child_text

                    # Folder path these are multiple of toolbarwindows32 but only one has the address
                    if child_class == "ToolbarWindow32" and child_text.startswith("Address: "):
                        folder_path = child_text.replace("Address: ", "").strip()
                        # print(f"[CURRENT FOLDER] {folder_path}")
                
                except Exception as e:
                    # some childs do not contain values which cause expections
                    print(f"[ERROR] {e}")
                    continue
                    
            if folder_path and file_name:
                # path without extension
                tentative = os.path.join(folder_path, file_name)
                # if a folder
                if os.path.exists(tentative):
                    full_path = tentative
                else:
                    # Try to resolve with any extension (A bug here)
                    matches = glob.glob(tentative + ".*")
                    # print(f"[TENTATIVE PATH] {matches}")
                    if matches:
                        full_path = matches[0] # take the first match (may be muktiple match)
                    else:
                        full_path = tentative  # fallback

                print(f"[FULL PATH] {full_path}")

        if full_path and os.path.exists(full_path):
            if ocr.main(full_path):  # Call OCR detection with the full path
                print("[BLOCKED] Sensitive file detected!")
        
                # Find the Edit control (filename box) again
                for child in children:
                    if win32gui.GetClassName(child) == "Edit":
                        # Clear the text in the Edit control which unselects the file
                        win32gui.SendMessage(child, win32con.WM_SETTEXT, 0, "")
                        break

while True:
    win32gui.EnumWindows(enum_handler, None)
    time.sleep(1)

