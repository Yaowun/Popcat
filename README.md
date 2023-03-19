# Popcat

## 專案介紹
本專案使用 Python 程式語言實作網路爬蟲，利用 Selenium 套件進行網路爬蟲，透過 ChromeDriver 開啟 POPCAT 網站並自動執行點擊指令。

## 專案技術
Python 3.9、Selenium 4.8.2

## 資料夾說明
* chromedriver - ChromeDriver 放置處，依照其版本放置於對應子目錄中
  * nnn - ChromeDriver 主版號 nnn 的主程式放置處
* fig - 圖片放置處

## 實作
### ChromeDriver
ChromeDriver 需要與用戶的 Chrome 瀏覽器版本相同才能以執行，但由於 Chrome 瀏覽器會自動更新，因此使用 chromedriver_autoinstaller 套件讓 ChromeDriver 可以自動更新到與用戶的 Chrome 瀏覽器相符的版本。
由於使用 chromedriver_autoinstaller 下載的 ChromeDriver 會放置在名稱為 nnn （主版號）的資料夾中，因此我們首先定義能查詢主版號的函式
``` python
def get_chrome_main_version():
    return chromedriver_autoinstaller.get_chrome_version().split('.')[0]
```
接著定義更新 ChromeDriver 的函式
``` python
def update_chromedriver(path):
    chrome_main_version = get_chrome_main_version()
    for p in os.listdir(path):
        try:
            if int(p) < int(chrome_main_version):
                shutil.rmtree(os.path.join(path, p), ignore_errors=False)
        except:
            pass
    chromedriver_autoinstaller.install(path="./chromedriver")
```

### 點擊次數設定
本專案透過與程式互動設定點擊次數，根據用戶可能的輸入進行條件判斷並給予適當回應，最後依據所得到輸入執行爬蟲程式。
根據用戶不同的輸入，設定給予的回應為：
* 空值 - 確認是否直接執行爬蟲程式直到關閉網頁，要求輸入 Yes 或 No
* 含有不是數字的非法法字元 - 提示輸入包含非法字元，要求重新輸入
* 非正整數 - 提示輸入需為正整數，要求重新輸入
``` python
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
```
其中 `query_yes_no` 與 `is_number` 函示定義如下
``` python
def query_yes_no(question, default="yes"):
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
```
``` python
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
         return False 
```
底下為實際執行結果
```
Please enter the number of clicks you want: 
Do you want to continue running the programming until you close it? [Y/n] 
test
Please respond with 'yes' or 'no' (or 'y' or 'n').
Do you want to continue running the programming until you close it? [Y/n] 
n

Please enter the number of clicks you want: test
Input contains illegal characters!
Please enter the number of clicks you want: -5
Please enter a positive integer!
Please enter the number of clicks you want: 3.14
Please enter a positive integer!
Please enter the number of clicks you want: 100
Programming starts...
Popcat 100 clicks done.
```


