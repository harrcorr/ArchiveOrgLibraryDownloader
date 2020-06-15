from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import requests
import os
import threading
import shutil
chrome_options = Options()
email = input("The email for your Archive.org account: ")
password = input("And the password: ")
url = input("Url of book you want to download: ")
dir = input("Where do you want to save the books pages (relative to current directory) : ")
pages = input("How many pages do you want to download: ")
quality = input("What scale do you want the images 1-10 (lower is better res): ")
print("Starting.. btw because of multi threading dont exit the program until it says PRESS ANY KEY TO CONTINUE that means all threads are completed")
quality = int(quality)
pages = int(pages)
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome("./chromedriver.exe",chrome_options=chrome_options)
driver.get("https://archive.org/account/login")
user = driver.find_element_by_name("username")
pwd = driver.find_element_by_name("password")
cookies_dict = {}
user.send_keys(email)
pwd.send_keys(password+"\n")
time.sleep(0.5)
s = requests.Session()
def Download(url,directory,bookname,pagenum):
    if(os.path.exists(directory)):
        pass
    else:
        os.mkdir(directory)
    print("Downloading Page: " + str(pagenum))
    r = requests.get(url, stream=True,cookies=cookies_dict)
    r.raw.decode_content = True
    with open(directory+"/"+str(pagenum)+".jpg", 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
def split(string):
    splitstring = []
    for i in string:
        splitstring.append(i)
    return splitstring

def join(array):
    result = ""
    for i in array:
        result+=str(i)
    return result
def FloatToString(float,digits):
    float = split(str(float))[1:digits]
    float = "".join(float)
    float = float.replace(".","")
    if(len(split(float)) != 4):
        float = "0"+float
    return float
def GetPagesArray(srcurl,maxpages):
    pages = []
    srcurl = srcurl.split("&scale=4")
    tmp = split(srcurl[0])
    tmp[len(tmp)-1]="2&scale="+str(quality)
    tmp = "".join(tmp)
    srcurl = str("".join(tmp)+"".join(srcurl[1]))
    modurl = srcurl
    i=0.0001
    while(len(split(str(maxpages))) != 4):
        maxpages = "0"+str(maxpages)
    if(len(split(maxpages)) == 4):
        maxpages = "0."+maxpages
    maxpages = float(maxpages)
    while(i < maxpages):
        modurl = modurl.split(".jp2")
        spliturl = split(modurl[0])
        spliturl = spliturl[:len(spliturl)-4]
        value = split(FloatToString(i,6))
        spliturl+=value
        modurl = "".join(spliturl)+".jp2&"+modurl[1]
        modurl = "".join(modurl)
        pages.append(modurl)
        modurl=srcurl
        i+=0.0001
    return pages
def GetBaseUrl(bookurl,num = 0):
    success = 0
    while(success != 1):
        if(num == 0):
            driver.get(bookurl)
        try:
            base = driver.find_elements_by_class_name("BRpageimage")[1].get_attribute("src")

            success = 1
        except Exception as e:
            num=num+1
            pass
    cookies = driver.get_cookies()
    for cookie in cookies:
       cookies_dict[cookie['name']] = cookie['value']
    return base
print("Finding pages....")
download = GetPagesArray(GetBaseUrl(url),pages)
print("Downloading pages....")
for i in range(0,len(download)):
    threading.Thread(target=Download,args=(download[i],dir,"",i)).start()