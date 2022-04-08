from PIL import Image
import pytesseract
import os
import re

def img_to_word(pic_name):

    path = os.path.dirname(__file__)# 讀取絕對路徑 
    pytesseract.pytesseract.tesseract_cmd = path+'\\tesseract\\tesseract.exe'#指定tesseract.exe執行檔位置

    img = Image.open(path + '\img\\'+pic_name) #圖片檔案位置
    im = img.crop((60,550,515,730)) #裁切圖片至內容區

    text = pytesseract.image_to_string(im, lang='eng') #讀英文
    Line = str() 

    for line in text.splitlines():
        traitRegex = r"(GUARD)|(BANNER)|(STEALTH)|(WITHER)|(LIFESTEAL)|(ARMOR)"  #用正規表達確認是否有trait
        check_trait = re.search(traitRegex,line) 
        if check_trait == None:
            Line = Line + ' ' + line

    Line = Line.lstrip() 

    triggerRegex = r"([A-za-z]+):" #用正規表達確認是否有trigger 
    check_trigger = re.search(triggerRegex,Line)

    return check_trigger,Line

if __name__ == '__main__':
    
    trigger,text = img_to_word("42-silver.png")
    
    if trigger != None:
        print(trigger[1])

    print(text)


