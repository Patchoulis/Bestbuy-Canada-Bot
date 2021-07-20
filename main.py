import PySimpleGUIQt as sg
import bs4
import sys
import time
import getpass
import _thread as th
import os
from secret import * 

#Test Comment

from selenium.webdriver.common.keys import Keys
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Define the window's contents
frame_layout1 = [[sg.Text("Put URL Search link in here!",justification='center',font=("Helvetica", 10))],
          [sg.Input(key='-URL-',justification='left')]]

frame_layout2 = [[sg.Text("  Month",justification='left'),sg.Text("  Year",justification='left'),sg.Text("  Address",justification='left')],
                [sg.Input(key='-MONTH-',justification='left'),sg.Input(key='-YEAR-',justification='left'),sg.Input(key='-ADDRESS-',justification='left')]]

frame_layout3 = [[sg.Text("  Email",justification='left'),sg.Text("  First Name",justification='left'),sg.Text("  Last Name",justification='left')],
                [sg.Input(key='-EMAIL-',justification='left'),sg.Input(key='-FIRSTNAME-',justification='left'),sg.Input(key='-LASTNAME-',justification='left')]]

frame_layout4 = [[sg.Text("  Phone Number",justification='left'),sg.Text("  City",justification='left'),sg.Text("  Postal Code",justification='left')],
                [sg.Input(key='-PHONE-',justification='left'),sg.Input(key='-CITY-',justification='left'),sg.Input(key='-POSTAL-',justification='left')]]

frame_layout5 = [[sg.Text("  CVV",justification='left'),sg.Text("  Card Number",justification='left'),sg.Text("  Password",justification='left')],
                [sg.Input(key='-CVV-',justification='left'),sg.Input(key='-CARD-',justification='left'),sg.Input(key='-PASSWORD-',justification='left')]]


layout = [[sg.Text("Bestbuy.ca Bot",justification='center',background_color=0,font=("Helvetica", 15))],
          [sg.Frame("",frame_layout1)],
          [sg.Frame("",frame_layout2)],
          [sg.Frame("",frame_layout3)],
          [sg.Frame("",frame_layout4)],
          [sg.Frame("",frame_layout5)],
          [sg.Text(key='-OUTPUT1-',background_color=0,text_color="black",font=("Helvetica", 13))],
          [sg.Button('Start',size=(70,30)), sg.Button('Pause',size=(70,30)), sg.Button('Ready!',size=(70,30))]]

checkuser = getpass.getuser()

# Create the window
window = sg.Window('Bestbuy.ca Bot', layout,size=(588,402),background_image="C:\\Users\\" + checkuser + "\\Documents\\Python\\Background.png",alpha_channel=0.9)

# Twilio configuration

client = Client(accountSid, authToken)

# Display and interact with the Window using an Event Loop
def ReadUI():
    while True:
        event, values = window.read()
        global OnOrOff
        OnOrOff = True
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            OnOrOff = False
            break
        if event == 'Start':
            OnOrOff = True
            window['-OUTPUT1-'].update("Starting up the bot, a window should appear shortly")
            StartUp(values)
            
        if event == 'Pause':
            OnOrOff = False
            window['-OUTPUT1-'].update("The program is pausing")
        #values['-SEARCH-']

def timeSleep(x, driver):
    for i in range(x, -1, -1):
        sys.stdout.write('\r')
        sys.stdout.write('{:2d} seconds'.format(i))
        window['-OUTPUT1-'].update('{:2d} seconds'.format(i))
        sys.stdout.flush()
        time.sleep(1)
    driver.refresh()
    sys.stdout.write('\r')
    sys.stdout.write('Page refreshed\n')
    window['-OUTPUT1-'].update('Page refreshed')
    sys.stdout.flush()

def createDriver():
    """Creating driver."""
    options = Options()
    # Change To False if you want to see Firefox Browser Again.
    options.headless = False
    
    # Enter Firefox Profile Here in quotes.
    Path = "C:\\Users\\" + checkuser + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\986fblri.default-release"
    print(Path)
    
    Options2 = webdriver.FirefoxOptions()
    Options2.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")

    profile = webdriver.FirefoxProfile(Path)
    driver = webdriver.Firefox(firefox_profile = profile, options=options, executable_path=GeckoDriverManager().install())
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def driverWait(driver, findType, selector):
    """Driver Wait Settings."""
    while True:
        if findType == 'css':
            try:
                driver.find_element_by_css_selector(selector).send_keys(Keys.RETURN)
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)
        elif findType == 'name':
            try:
                driver.find_element_by_name(selector).send_keys(Keys.RETURN)
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)
        elif findType == 'xpath':
            try:
                driver.find_element_by_xpath(selector).send_keys(Keys.RETURN)
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)
        elif findType == 'execute':
            try:
                driver.find_element_by_css_selector(selector).click()
                break
            except NoSuchElementException:
                driver.implicitly_wait(0.2)

def findingCards(driver,InterValues):
    """Scanning all cards."""

    driver.get(InterValues['-URL-'])
    while OnOrOff:
        time.sleep(2)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, 'html.parser')
        wait = WebDriverWait(driver, 15)
        wait2 = WebDriverWait(driver, 2)
        try:
            findAllCards = soup.find('span', string=['Available online only', 'Available to ship', 'Available at nearby stores'], attrs={'class': 'container_3LC03'})
            if findAllCards:

                #Go to link
                driver.get(f"https://www.bestbuy.ca{findAllCards.find_previous('a').get('href')}")
                

                # Clicking Add to Cart.
                driverWait(driver, 'css', ".addToCartButton")

                time.sleep(2)
                driver.get('https://www.bestbuy.ca/checkout/?qit=1#/en-ca/review')
                time.sleep(3)
                driverWait(driver, 'css', "button.continue-to-payment")
                time.sleep(3)

                #Address inputs
                try:
                    security_code = driver.find_element_by_id("email")
                    security_code.send_keys(InterValues['-EMAIL-'])

                    security_code = driver.find_element_by_id("lastName")
                    security_code.send_keys(InterValues['-LASTNAME-'])

                    security_code = driver.find_element_by_id("firstName")
                    security_code.send_keys(InterValues['-FIRSTNAME-'])

                    security_code = driver.find_element_by_id("addressLine")
                    security_code.send_keys(InterValues['-ADDRESS-'])

                    security_code = driver.find_element_by_id("city")
                    security_code.send_keys(InterValues['-CITY-'])

                    security_code = driver.find_element_by_id("postalCode")
                    security_code.send_keys(InterValues['-POSTAL-'])

                    security_code = driver.find_element_by_id("phone")
                    security_code.send_keys(InterValues['-PHONE-'])

                    time.sleep(3)
                except (NoSuchElementException, TimeoutException):
                    print("Item is not in cart anymore. Retrying..")
                    findingCards(driver,InterValues)
                    timeSleep(3, driver)
                    pass


                #CVV input/Payments
                try:
                    print("Trying CVV Number.")
                    window['-OUTPUT1-'].update("Trying CVV Number")

                    security_code = driver.find_element_by_id("cvv")
                    security_code.send_keys(InterValues['-CVV-'])

                    security_code = driver.find_element_by_id("shownCardNumber")
                    security_code.send_keys(InterValues['-CARD-'])

                    if int(InterValues['-MONTH-']) >= 10:
                        driver.find_element_by_xpath('//*[@id="expirationMonth"]').send_keys("1"*(int(InterValues['-MONTH-'])-9))
                    else:
                        driver.find_element_by_xpath('//*[@id="expirationMonth"]').send_keys("0"*(int(InterValues['-MONTH-'])))

                    driver.find_element_by_xpath('//*[@id="expirationYear"]').send_keys("2"*(int(InterValues['-CARD-'])-2020))

                    driverWait(driver, 'css', "button.continue-to-review")
                    time.sleep(3)
                    driverWait(driver, 'execute', "button.order-now")
                except (NoSuchElementException, TimeoutException):
                    print("Item is not in cart anymore. Retrying..")
                    window['-OUTPUT1-'].update("Item is not in cart anymore. Retrying..")
                    findingCards(driver,InterValues)
                    pass

                # Completed Checkout. Sending message with Twilio.
                print('Order Placed!')
                window['-OUTPUT1-'].update("Order Placed!")
                try:
                    toNumber = "+1" + InterValues['-PHONE-'] #Phone Number
                    client.messages.create(to=toNumber, from_=fromNumber, body='ORDER PLACED!')
                except (NameError, TwilioRestException):
                    pass
                for i in range(3):
                    print('\a')
                    time.sleep(1)
                time.sleep(1800)
                driver.quit()
                return
            else:
                pass

        # Refresh Page Timer
        except NoSuchElementException:
            pass
        timeSleep(3, driver)

def SignIn(driver,Values):
    driver.get("https://www.bestbuy.ca/identity/en-ca/signin?tid=uODGrxl3ROVyVIsbtYNoHN3VHkF28IQrE%252BxRun%252BNXsRN2dvycIeFXeE7rD%252BiLkYi72Zwpv8eAphGf%252F%252FunUFvLstXknbJVrwwTQEc6eCogTvOypStB%252BbVOhjAW6URTdpFHKwD8UPWRUACRHfDuwizoar0sYVhxgBCrxmNox0cjcCe1UNLLg%252FRWhICMT9%252F7Rx%252FfFEZViC%252BlX2vJgiNLRPvtv79eqpkruhzC8rs8FoV2p3zwTTKYKfDHb5GixS9IceqA0hANSs1vT2pT7DJYBkmxUA4TZohel1Qsdi%252Fvw%252BPr9vlPulCZPYUmE1lGl%252BoXmEQ")
    
    time.sleep(4)
    security_code = driver.find_element_by_id("username")
    security_code.send_keys(Values['-EMAIL-'])

    security_code = driver.find_element_by_id("password")
    security_code.send_keys(Values['-PASSWORD-'])

    driverWait(driver, 'css', ".signin-form-button")

    window['-OUTPUT1-'].update("Please solve the captcha and press 'Ready' when finished!")


        

def StartUp(Values):
    driver = createDriver()
    SignIn(driver,Values)

    while True:
        event, values = window.read()
        if event == 'Ready!':
            window['-OUTPUT1-'].update("Starting up purchases!")
            break
        time.sleep(1)

    global OnOrOff
    th.start_new_thread(findingCards,(driver,Values,))


#Starts Program
ReadUI()

# Finish up by removing from the screen
window.close()