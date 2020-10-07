from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import glob
import csv
import calendar
import re
from balance.models import History_info
import openpyxl
from  django.utils.timezone import now


print("Скрипт не резкий, требует пару минут на каждый кабинет")
option = Options()
#  безвголовый
option.add_argument('headless')
#
# option.add_argument("--disable-infobars")
# option.add_argument("start-maximized")
# option.add_argument("--disable-extensions")

option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1,
    "download.default_directory": '/home/user/megafon_parser/',
})


def login(lk, driver):
    #driver.implicitly_wait(300)
    time.sleep(120)
    #авторизация
    driver.get('https://szf.b2blk.megafon.ru/b2b/login')
    time.sleep(120)

    login = driver.find_element_by_css_selector('[name="username"]')
    password = driver.find_element_by_css_selector('[name="password"]')
    submit = driver.find_element_by_css_selector('[data-button="buttonSubmitAuthform"]')


    login.send_keys(lk.login)
    password.send_keys(lk.password)
    submit.click()

def logout(driver):
    driver.get('https://szf.b2blk.megafon.ru/b2b/logout')
    time.sleep(120)
    #закрываем webdriver
    driver.delete_all_cookies()
    driver.quit()


def get_balance(lk, driver):
    #driver.implicitly_wait(300)
    driver.get('https://b2blk.megafon.ru/accounts')
    time.sleep(60)
    balance_el = driver.find_element_by_xpath('//*[@id="accountTabs"]/li[2]/a')
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    def find_balance():
        link = soup.find(string=re.compile("Текущий баланс"))
        link = link.next_element
        desc = list(link.descendants)
        return desc[1].text
    def find_expenses():
        link = soup.find(string=re.compile("Начислено по всем абонентам с начала периода"))
        link = link.next_element
        desc = list(link.descendants)
        return desc[1].text
    def find_credit_limit():
        link = soup.find(string=re.compile("Размер кредитного лимита"))
        link = link.next_element
        desc = list(link.descendants)
        return desc[1].text

    balance= find_balance()
    expenses = find_expenses()
    try:
        credit_limit = find_credit_limit()
    except:
        print("не найдена графа кредитного лимита")
        credit_limit = 0


    def val_format(value):
        value = str(value)
        value = value[:-5]
        value = value.replace(' ', '')
        value = value.replace(',', '.')
        return value


    balance=val_format(balance)
    print('balance = ', balance)

    expenses=val_format(expenses)
    print('expenses =', expenses)

    if credit_limit!=0:
        credit_limit=val_format(credit_limit)
        print('credit_limit = ', credit_limit)

    lk.company_info.balance = float(balance)
    lk.company_info.expenses = float(expenses)
    lk.company_info.credit_limit = float(credit_limit)

    lk.company_info.save()

##   ( Расходы абонентов + расходы абонентов/26 *(31-26) ) - текущий баланс
def to_pay(lk):
    expenses=lk.company_info.expenses
    balance = lk.company_info.balance
    updated = lk.company_info.updated
    current_info_day = updated.day
    days_of_month = calendar.monthrange(updated.year, updated.month)[1]
    days_left = days_of_month - current_info_day

    #дорогая формула
    #payment = (expenses + expenses/current_info_day*days_left)*2-balance
    #

    payment = (expenses + expenses / current_info_day * days_left) - balance

    payment = round(payment, 2)
    print('payment =',payment)
    lk.company_info.payment = payment
    lk.company_info.save()

def save_to_history(lk):
    History_info.objects.create(
        company_key=lk.key,
        company_name = lk.name,
        balance = lk.company_info.balance,
        expenses = lk.company_info.expenses,
        payment = lk.company_info.payment,
    )

'''
def get_all_try_mode(companies):
    driver = webdriver.Chrome(options=option, executable_path='/home/user/megafon_parser/chromedriver')
    try_counter=0
    while True | try_counter<20:
        try:
            get_all(companies, driver)
        except:
            driver.quit()
            print("Неудачная попытка парсинга, timeout на час")
            time.sleep(3600)
            try_counter=try_counter+1
        else:
            print("с первого раза!")
            break
'''

def get_all(companies):
    for lk in companies:
        driver = webdriver.Chrome(options=option, executable_path='/home/user/megafon_parser/chromedriver')
        if lk.company_info.updated.strftime('%d-%m-%y') == now().strftime('%d-%m-%y'):
            continue
        print('\nparsing from '+ lk.name)

        print('попытка логина...')
        login(lk, driver)
        print('ok!')
        get_balance(lk, driver)
        print('логаут...')
        logout(driver)
        print('ok!')
        to_pay(lk)
        save_to_history(lk)




def get_all_payment(companies):
    for lk in companies:
        to_pay(lk)

def dots_to_commas(value):
        value = str(value)
        value = value.replace('.', ',')
        return value

def get_table(companies):
    updated= companies[0].company_info.updated.strftime('%d-%m')
    with open('./payment.csv', 'w', encoding='windows-1251') as csvfile:
        file_writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_NONE, escapechar= '\\')
        data = []
        data.append([ 'Компания', 'балланс на {0}'.format(updated), 'расходы абонентов на {0}'.format(updated), 'К оплате'])
        for lk in companies:
            #data.append([ lk.name, lk.company_info.balance, lk.company_info.expenses, lk.company_info.payment])
            data.append([ lk.name, dots_to_commas(lk.company_info.balance), dots_to_commas(lk.company_info.expenses), dots_to_commas(lk.company_info.payment)])
        print(data)
        file_writer.writerows(data)
