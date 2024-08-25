from selenium import webdriver
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
driver = webdriver.Chrome()
driver.get('https://tenhou.net/2/?q=1m2s7s8s4z3p4m9m9m1p3p6p8p9p')
driver.implicitly_wait(10)
html = driver.page_source
driver.quit()

for line in html.splitlines():
    if line and line[0] == "打":
        print(line)