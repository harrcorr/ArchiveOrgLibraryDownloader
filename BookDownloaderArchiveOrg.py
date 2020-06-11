from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import os
chrome_options = Options()
email = input("The email for your Archive.org account: ")
password = input("And the password: ")
url = input("Url of book you want to download: ")
dir = input("Where do you want to save the books pages (relative to current directory) : ")
pages = input("How many pages do you want to download: ")
pages = int(pages)
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome("./chromedriver.exe",chrome_options=chrome_options)
driver.get("https://archive.org/account/login")
user = driver.find_element_by_name("username")
pwd = driver.find_element_by_name("password")
user.send_keys(email)
pwd.send_keys(password+"\n")
time.sleep(0.5)

def Download(url,directory,bookname,pagenum):
    if(os.path.exists(directory)):
        pass
    else:
        os.mkdir(directory)
    print("Downloading Page: " + str(pagenum))
    driver.get(url)
    image = driver.find_element_by_tag_name("img").screenshot_as_png
    im = Image.open(BytesIO(image))
    name = directory + "/" + str(pagenum)+r".png"
    im.save(name)

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

def GetPagesArray(srcurl,maxpages):
    pages = []
    srcul = srcurl.split(".jp2")
    for i in range(0,maxpages):
        for c in range(0,len(str(i))):
            srcul[0] = split(srcul[0])
            srcul[0][(len(srcul[0])-1)-(c)]=split(str(i))[c]
            new = join(srcul[0])
        pages.append(new+".jp2"+srcul[1])
        srcul=srcurl.split(".jp2")
    return pages
def GetBaseUrl(bookurl,num = 0):
    success = 0
    while(success != 1):
        if(num == 0):
            driver.get(bookurl)
        try:
            base = driver.find_elements_by_class_name("BRpageimage")[1].get_attribute("src")

            success = 1
        except:
            num=num+1
            pass
    print(base)
    return base
print("Finding pages....")
download = GetPagesArray(GetBaseUrl(url),pages)
print("Downloading pages....")
for i in range(0,len(download)):
    Download(download[i],dir,"",i)