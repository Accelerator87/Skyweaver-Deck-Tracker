import os
import json
import time
import requests
import pyautogui
from selenium import webdriver

requests.packages.urllib3.disable_warnings()

cardsList = {}
attachmentsList = {}
account = "jacksonscott25087@gmail.com"
password = "test0001"


def find_element(xpath):
    
    cnt = 1
    while True:
        try:
            return driver.find_element_by_xpath(xpath)
            break
        except:
            cnt += 1
            time.sleep(0.5)
        if cnt%100 == 0:
            print("Finding",xpath,"over",cnt,"times")


def login_fb():
    
    driver.switch_to_window(driver.window_handles[2])
    emt = find_element("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[1]/input")
    emt.send_keys(account)
    
    emt = find_element("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[2]/input")
    emt.send_keys(password)
    
    emt = find_element("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button")
    emt.click()
    time.sleep(40)


def login_SequenceWallet_by_fb():
    
    driver.switch_to_window(driver.window_handles[1])
    emt = find_element("/html/body/div[2]/div/div/div[1]/div[3]/a[2]")
    emt.click()
    login_fb()


def login_skyweaver():
    
    driver.get("https://play.skyweaver.net/")
    emt = find_element("/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div[3]/button")
    emt.click()
    login_SequenceWallet_by_fb()


def logout_SequenceWallet():
    
    driver.get("https://sequence.app/settings/sessions")
    
    emt = find_element("/html/body/div[2]/div/div/div[2]/div/a")
    emt.click()
    emt = find_element("/html/body/div[2]/div/div[1]/div[3]/div/div[1]/div/a")
    emt.click()
    emt = find_element("/html/body/div[1]/div[3]/div/div/div/a[1]")
    emt.click()


def get_html_url(inner):
    
    start = "https"
    end = "png"
    url = ""
    for i in range(0,len(inner)):
        tmpS = inner[i:i+5]
        if start == tmpS:
            for j in range(i+5,len(inner)):
                tmpE = inner[j:j+3]
                if end == tmpE:
                    url = inner[i:j+3]
                    return url
                    

def get_html_id(inner):
    
    start = "data-card-id=\""
    end = "\""
    ID = -1
    for i in range(0,len(inner)):
        tmpS = inner[i:i+14]
        if start == tmpS:
            for j in range(i+14,len(inner)):
                tmpE = inner[j]
                if end == tmpE:
                    ID = inner[i+14:j]
                    return ID
    

def get_cardslist():
    
    cardID = [line.strip() for line in open("skyweaver_cards_id.txt").readlines()]
    url = "https://play.skyweaver.net/items/cards//silver"
    cardURL = [ url[0:39] + str(ID) + url[39:] for ID in cardID ]
    
    for url in cardURL:
        
        driver.get(url)
        
        img = find_element("/html/body/div[2]/div[2]/div/div[5]/div")
        inner = str(img.get_attribute("innerHTML"))
        
        imgURL = get_html_url(inner)
        cardID = get_html_id(inner)
        
        Property = []
        Value = []
        cardInfo = {}
        i = 1
        while(i > 0):
            try:
                tmpP = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div[3]/div["+str(i)+"]/div[1]/div")
                tmpP = str(tmpP.get_attribute("innerHTML"))
                Property.append(tmpP)
                tmpV = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div[3]/div["+str(i)+"]/div[2]")
                tmpV = str(tmpV.get_attribute("innerHTML"))
                Value.append(tmpV)
                i += 1
            except:
                break
        i = 4
        while(i > 0):
            try:
                tmpP = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div["+str(i)+"]/div[2]/span[1]")
                tmpP = str(tmpP.get_attribute("innerHTML"))
                Property.append(tmpP[0:len(tmpP)-1])
                i += 1
            except:
                break
        
        if not os.path.exists("card_imgs"):
            os.mkdir("card_imgs")
        img = requests.get(imgURL)
        f = open("card_imgs//"+str(cardID)+".png", "wb")
        f.write(img.content)
        f.close()
            
        cardInfo["Id"] = cardInfo.get("Id",cardID)
        
        for i in range(0,len(Property)):
            s1 = Property[i][0:1]
            s2 = Property[i][1:]
            Property[i] = s1.upper() + s2.lower()
            if i < len(Value)-1:
                cardInfo[Property[i]] = cardInfo.get(Property[i],Value[i])
            elif i >= len(Value):
                cardInfo[Property[i]] = cardInfo.get(Property[i],True)
        
        cardsList[cardID] = cardsList.get(cardID,cardInfo)


def get_attachment():
    
    driver.get("https://play.skyweaver.net/market/cards/buy")
    
    cardTotal = find_element("/html/body/div[2]/div[2]/div/div[2]/div[2]/div[1]")
    cardTotal = int(str(cardTotal.get_attribute("innerHTML"))[0:3])
    
    time.sleep(5)
    pyautogui.moveTo(182,409)
        
    cnt = 0
    while cnt < cardTotal:
        
        time.sleep(0.2)
        
        pyautogui.moveRel(10,214)
        preID = -1
        cardID = -1
        firstCardId = -1
        
        while True:
            time.sleep(0.1)
            pyautogui.moveRel(31,0)
            if pyautogui.position().x >= 1885:
                break
            try:
                xpath = "//*[contains(@class,'cardHovered')]/parent::div"
                html = str(driver.find_element_by_xpath(xpath).get_attribute("outerHTML"))
                cardID = get_html_id(html)
            except:
                pass
            
            if cardID != preID:
                preID = cardID
                cnt += 1
            
            if cnt%6 == 1:
                firstCardId = cardID
            
            imgID = -1
            imgURL = "?"
            
            try:
                html = driver.find_element_by_xpath("/html/body/div[1]/div[last()]/div/div/div[3]/div/div[1]/div/div")
                html = str(html.get_attribute("innerHTML"))
                imgID = get_html_id(html)
                imgURL = get_html_url(html)
            except:
                pass
            
            if (imgID != -1) and (imgURL != "?") :
                
                cardsList[cardID]["Attachment_id"] = cardsList[cardID].get("Attachment_id",imgID)
                attachmentsList[imgID] = attachmentsList.get(imgID,{})
                attachmentsList[imgID]["img_des"] = attachmentsList[imgID].get("img_des",imgURL)
        
        pyautogui.moveTo(182,409)
        time.sleep(1.5)
        
        while True:
            pyautogui.scroll(-10)
            if pyautogui.position().y >= 1050:
                break
            try:
                pyautogui.moveRel(10,0)
                pyautogui.moveRel(-10,0)
                xpath = "//*[contains(@class,'cardHovered')]/parent::div"
                html = str(driver.find_element_by_xpath(xpath).get_attribute("outerHTML"))
                cardID = get_html_id(html)
            except:
                pass
        
            if cardID != firstCardId:
                break


def get_attachmentsList():
    
    url = "https://play.skyweaver.net/items/cards//silver"
    for ID in attachmentsList:
        
        driver.get(url[0:39] + str(ID) + url[39:])
        
        Property = []
        Value = []
        i = 1
        while(i > 0):
            try:
                tmpP = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div[3]/div["+str(i)+"]/div[1]/div")
                tmpP = str(tmpP.get_attribute("innerHTML"))
                Property.append(tmpP)
                tmpV = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div[3]/div["+str(i)+"]/div[2]")
                tmpV = str(tmpV.get_attribute("innerHTML"))
                Value.append(tmpV)
                i += 1
            except:
                break
        i = 4
        while(i > 0):
            try:
                tmpP = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[6]/div["+str(i)+"]/div[2]/span[1]")
                tmpP = str(tmpP.get_attribute("innerHTML"))
                Property.append(tmpP[0:len(tmpP)-1])
                i += 1
            except:
                break
        
        if not os.path.exists("attachment_imgs"):
            os.mkdir("attachment_imgs")
        img = requests.get(attachmentsList[ID]["img_des"])
        f = open("attachment_imgs//"+str(ID)+".png", "wb")
        f.write(img.content)
        f.close()
        
        del attachmentsList[ID]["img_des"]
            
        attachmentsList[ID]["Id"] = attachmentsList[ID].get("Id",ID)
        for i in range(0,len(Property)):
            s1 = Property[i][0:1]
            s2 = Property[i][1:]
            Property[i] = s1.upper() + s2.lower()
            if i < len(Value)-1:
                attachmentsList[ID][Property[i]] = attachmentsList[ID].get(Property[i],Value[i])
            elif i >= len(Value):
                attachmentsList[ID][Property[i]] = attachmentsList[ID].get(Property[i],True)
    

    
if __name__ == "__main__":
    
    driver = webdriver.Chrome("chromedriver.exe")
    driver.maximize_window()
    
    #login_skyweaver()
    #driver.switch_to_window(driver.window_handles[0])
    #driver.get("https://play.skyweaver.net/play/tutorial")
    
    get_cardslist()
    get_attachment()
    get_attachmentsList()
    
    f = open("cardsList.json","w")
    json.dump(cardsList,f)
    f.close()
    
    f = open("attachmentsList.json","w")
    json.dump(attachmentsList,f)
    f.close()
    
    #logout_SequenceWallet()
    #time.sleep(30)
    #driver.quit()
