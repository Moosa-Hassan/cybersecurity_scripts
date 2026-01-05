import subprocess, json , os

PDF = "metadata_files/DLPTEST.pdf"
PNG = "metadata_files/image1.png"
MP3 = "metadata_files/output.mp3"
TXT = "metadata_files/test1.txt"
JPG = "metadata_files/1.jpg"
TEX = "metadata_files/some.tex"

file_metadata = {}

def run_exiftool(file_path):
    """
    Run exiftool on the given file and return the output.
    """
    try:
        result = subprocess.run(['exiftool', '-j',file_path], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)[0] # return as dictionary
    except Exception as e:
        return f"An error occurred: {e}"
  
  
# extract metadata for a file  
  
# for file in [PNG, MP3, TXT, JPG, PDF]:
#     metadata = run_exiftool(file)
#     file_name = os.path.basename(file)
#     if metadata.get('Label',None):
#         if metadata['Label'] == 'Confidential':
#             print(f"File: {file_name} is marked as Confidential")
#         else:
#             print(f"File: {file_name} has Label: {metadata['Label']}")
#     else:
#         print(f"File: {file_name} has no Label metadata")


MAGIC_BYTES = {
    b"PDF": "application/pdf",
    b"JFIF": "image/jpeg",
    b"PNG": "image/png",
    b"ID3": "audio/mpeg",  
}

EXTENSION_MAP = {
    ".pdf": "application/pdf",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".mp3": "audio/mpeg",
    ".tex": "text/plain"
}

def file_check(file_path):
    """
    Check if the file mime matches its extension and magic bytes
    """
    if os.path.exists(file_path):
        metadata = run_exiftool(file_path)
        extension = os.path.splitext(file_path)[1].lower()
        print(f"Extension: {extension}")
        mime_type = metadata.get('MIMEType', None)
        print(f"MIME Type from metadata: {mime_type}")
        test1 = test2 = False
        with open(file_path, 'rb') as f:
            file_start = f.read(50)
            for magic, mime in MAGIC_BYTES.items():
                if magic in file_start:
                    print(f"Detected MIME Type from magic bytes: {mime}")
                    if mime_type != mime:
                        print(f"Mismatch detected for {file_path}: Metadata MIME Type {mime_type} does not match Magic Bytes MIME Type {mime}")
                        test1 = True
                    else:
                        print(f"MIME Type matches for {file_path}: {mime_type}")
                    break
        for ext,mime in EXTENSION_MAP.items():
            if ext == extension:
                print(f"Detected MIME Type from extension: {mime}")
                if mime_type != mime:
                    print(f"Mismatch detected for {file_path}: Metadata MIME Type {mime_type} does not match Extension MIME Type {mime}")
                    test2 = True
                else:
                    print(f"MIME Type matches for {file_path}: {mime_type}")
                break
        if test1 or test2:
            return f"Mismatch detected for {file_path}. File is suspecious.\n"
        else : 
            return f"MIME Type matches for {file_path}. File is not suspecious.\n"
        
    else:
        return f"File {file_path} does not exist\n"
    
print(file_check(PDF))
print(file_check(TEX))  
print(file_check(MP3))