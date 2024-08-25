from selenium import webdriver
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

driver_path = "C:\Program Files (x86)\Microsoft\Edge\Application\chromedriver.exe"
driver = webdriver.Chrome(driver_path)
driver.get('https://tenhou.net/2/?q=1m2s7s8s4z3p4m9m9m1p3p6p8p9p')
driver.implicitly_wait(10)
html = driver.page_source
driver.quit()

print(html)
