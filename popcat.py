import os, sys, shutil, time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
         return False   

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def get_chrome_main_version():
    return chromedriver_autoinstaller.get_chrome_version().split('.')[0]

def update_chromedriver(path):
    chrome_main_version = get_chrome_main_version()
    for p in os.listdir(path):
        try:
            if int(p) < int(chrome_main_version):
                shutil.rmtree(os.path.join(path, p), ignore_errors=False)
        except:
            pass
    chromedriver_autoinstaller.install(path="./chromedriver")
    

#%% Main code
while True:
    click_end_number = input("Please enter the number of clicks you want: ")
    if click_end_number == '':
         if query_yes_no("Do you want to continue running the programming until you close it?"):
             click_end_number = float("inf")
             break
         else:
             continue
    elif not is_number(click_end_number):
        sys.stdout.write("Input contains illegal characters!")
    elif float(click_end_number) < 0 or float(click_end_number)%1 != 0:
        sys.stdout.write("Please enter a positive integer!")
    else:
        click_end_number = float(click_end_number)
        break

print("Programming starts...")
path_chromedriver = "./chromedriver"
update_chromedriver(path_chromedriver)
driver = webdriver.Chrome(service=Service(os.path.join(path_chromedriver, get_chrome_main_version(), "chromedriver.exe")))
driver.get("https://popcat.click/")
popcat = driver.find_element(By.ID, "app")
count = 0
web_existed = False
while count < click_end_number:
    popcat.click()
    count += 1
    time.sleep(0.0375)
    if driver is not None:
        try:
            driver.execute_script('javascript:void(0);')
            web_existed = True
        except:
            driver = None
            web_existed = False
    if not web_existed:
        break
print("Popcat {} clicks done.".format(count))
