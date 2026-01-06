import pytesseract as pyt 
import cv2

# We need to tell the path to the execuatble as its not the default path
pyt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# uses cv2 library to load a image


def get_text(image_path):
    """
    Function to get text from an image
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found at path: {image_path}")  
    return pyt.image_to_string(img)
    


def keyword_search(text,keywords):
    """"
    For keyword search in the text extracted
    """
    keywords = ["secret"]
    for keyword in keywords:
        if keyword in text:
            print(f"Keyword '{keyword}' found in the text.")
            return True
        else:
            print(f"Keyword '{keyword}' not found in the text.")
            return False
    
    
def regex_check(text):
    """
    For regex search in the text extracted
    """
    import re
    email_regex = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    email = re.findall(email_regex,text)
    print(f"Email: {email if email else 'Not found'}")
    IPV4_regex  = r'(?:\d{1,3}\.){3}\d{1,3}'
    IPV4 = re.findall(IPV4_regex, text)
    print(f"IPV4: {IPV4 if IPV4 else 'Not found'}")
    if email or IPV4:
        return True
    return False


def main(image_path):
    
    keywords = ["secret"]
    txt = get_text(image_path).lower()
    print(f"Extracted Text: {txt}")
    
    if keyword_search(txt, keywords) or regex_check(txt):
        return True
    return False

# main(<path to a file>)  # Example usage