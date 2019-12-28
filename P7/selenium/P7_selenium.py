#１、seleium小测试
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# browser = webdriver.Chrome(chrome_options=chrome_options)
browser = webdriver.Chrome()

try:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser,10)
    wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    #print(browser.page_source)
finally:
    browser.close()




#2、查找单个节点
from selenium import webdriver
from selenium.webdriver.common.by import By
browser = webdriver.Chrome()
browser.get('https://world.taobao.com')
input_first =  browser.find_element_by_id('mq')
input_second = browser.find_element_by_css_selector('#mq')
input_third = browser.find_element_by_xpath('//*[@id="mq"]')
input_fourth = browser.find_element_by_name('q')
input_fifth = browser.find_element(By.NAME,'q')
print(input_fifth)
print(input_fourth)
print(input_first)
# print(input_third)
# print(input_second)




#3、多个节点
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get('https://world.taobao.com')

lis = browser.find_elements(By.CSS_SELECTOR,'.cat-iconfont,cat-icon i')
print(lis)




#4、节点交互
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
#browser.get('https://world.taobao.com')
browser.get('https://www.runoob.com/')
input_first =  browser.find_element_by_id('s')
input_first.send_keys('linux')
time.sleep(2)
input_first.clear()
input_first.send_keys('python')
#button = browser.find_element_by_css_selector('input[type="submit"]')
#button.click()
input_first.send_keys(Keys.ENTER)




#5、动作链
from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
source = browser.find_element_by_css_selector('#draggable')
target = browser.find_element_by_css_selector('#droppable')
actions = ActionChains(browser)
actions.drag_and_drop(source,target)
actions.perform()




#6、执行js
from selenium import webdriver

browser = webdriver.Chrome()
url = 'https:www.zhihu.com/explore'
browser.get(url)
browser.execute_script('window.scrollTo(0,document.scrollHeight)')
browser.execute_script('alert("To Bottom")')




#7、获取节点信息
from selenium import webdriver
import requests

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/signin?next=%2F'
browser.get(url)
logo = browser.find_element_by_css_selector('.SignFlowHomepage-logo')
req = requests.get(logo.get_attribute('src'))
with open('zhihu.png','wb') as f:
    f.write(req.content)
print('Successful!',logo.get_attribute('src'))



from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
browser.get(url)
lis = browser.find_elements(By.CSS_SELECTOR,'.ExploreSpecialCard-contentTag')
for i in lis:
    print(i.text)
    print(i.id)





#8、延时等待&异常处理
from selenium import webdriver

browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('https://www.zhihu.com/explore')
input_first = browser.find_element_by_class_name('ExploreSpecialCard-title')
print(input_first)



from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException

browser = webdriver.Chrome()

try:
    browser.get('https://world.taobao.com/')
    #input_first =  browser.find_element_by_id('mq')
    wait = WebDriverWait(browser,10)
    input_first = wait.until(EC.presence_of_element_located((By.ID,'hello world')))
    print(type(input_first))
except TimeoutException as e:
    print('Time out')
except NoSuchElementException as e:
    print('No such element')
finally:
    browser.close()



#9、前进和后退
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.get('https://www.zhihu.com/')
#browser.get('https://www.python.org/')
browser.back()
time.sleep(2)
browser.forward()
browser.close()




#10、Cookies
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())
browser.add_cookie({'name':'Kang','domain':'www.zhihu.com','value':'dmy'})
print(browser.get_cookies())
browser.delete_all_cookies()
print(browser.get_cookies())




#11、选项卡管理
from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.execute_script('window.open()')
print(browser.window_handles)
browser.switch_to_window(browser.window_handles[1])
browser.get('https://world.taobao.com')
time.sleep(2)
browser.switch_to_window(browser.window_handles[0])
browser.get('https://www.zhihu.com')
