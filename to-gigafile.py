from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException
from selenium.common.exceptions import InvalidSelectorException
from selenium.webdriver.support import expected_conditions
import sys
import pyperclip
from plyer import notification

print('connecting to remote browser...')

options = Options()

#必要に応じてoptionsを設定
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')

#ドライバのパスの指定は不要
driver = webdriver.Chrome(options=options)

#要素が見つかるまで最大10秒間待機する（暗黙的な待機）→必ずアップロードが3回行われる問題が解決
driver.implicitly_wait(10)

try:
    #ウェブサイトに移動
    driver.get('https://gigafile.nu/')
except WebDriverException as e:
    #エラー内容を表示
    t = e.__class__.__name__
    print(t)
    print('エラー。インターネットに接続できていない可能性があります。')
    sys.exit()

try:
    #ファイルのアップロードフィールドを見つける
    upload_field = driver.find_element(By.XPATH,'//*[@id="upload_panel_button"]/input')
except NoSuchElementException as e:
    #エラー内容を表示
    t = e.__class__.__name__
    print(t)
    print('エラー。アップロードフィールドが見つかりません。開発者に報告してください。')
    sys.exit()

filepath = sys.stdin.read().rstrip()

try:
    #ファイルのパスをアップロードフィールドに送信
    upload_field.send_keys(filepath)
except InvalidArgumentException as e:
    #エラー内容を表示
    t = e.__class__.__name__
    print(t)
    print('エラー。アップロードファイルが見つかりません。')
    sys.exit()

#アップロードするファイルのサイズが大きい場合は下記タイムスリープを有効にすることで解決する場合があります。
time.sleep(30)

try:
    #変数elemにCSSセレクタで.file_info_url_box及び.clearfixと指定された要素を格納
    elem = WebDriverWait(driver, 3600).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.file_info_url_box.clearfix')))
    #変数elemに格納された要素からaタグ要素を抽出し、変数elem_aに格納
    elem_a = elem.find_element(By.TAG_NAME, 'a')
except InvalidSelectorException as e:
    #エラー内容を表示
    t = e.__class__.__name__
    print(t)
    print('エラー。ダウンロードURLを取得するためのHTML要素を取得できませんでした。開発者に報告してください。')
    sys.exit()

#一旦1秒待機
time.sleep(1)

try:
    #更にその中にあるhrefの記述を変数elem_hrefに格納
    elem_href = elem_a.get_attribute('href')
    if elem_href == None:
        print('エラー。ダウンロードURLを取得するためのHTML属性を取得できませんでした。開発者に報告してください。')
        sys.exit()
except Exception as e:
    #エラー内容を表示
    t = e.__class__.__name__
    print(t)
    print('エラー。ダウンロードURLを取得するためのHTML属性を取得できませんでした。開発者に報告してください。')
    sys.exit()


#変数elem_hrefをクリップボードにコピー
pyperclip.copy(elem_href)

#通知の設定
if elem_href:
    notification.notify(
        title = filepath + 'のダウンロードURLをクリップボードにコピーしました。',
        message = elem_href,
        app_name = 'File-Sharer via ギガファイル便',
        timeout = 15
    )

#ドライバを停止する
driver.quit()