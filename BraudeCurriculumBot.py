import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import timeit
NUMBER_OF_OPTIONS_PER_COURSE = 16

# User Info:
user_name = "Israel-israeli"
user_pass = "Israel2022"

# courses:
course1 = ['61758', ['הרצאה', ' א ', 'רון איתן', '15:50', '18:50'], ['מעבדה', ' ה ', 'מינישין מרינה', '08:30', '10:30'], ['תרגיל', ' ד ', 'מרינה', '09:30', '10:30']]
course2 = ['11375', ['הרצאה', ' ה ', 'תמר', '10:30', '12:20']]
course3 = ['11158', ['הרצאה', ' ד ', 'סעיד', '12:50', '14:50'], ['מעבדה', ' ד ', 'רומן', '10:30', '12:20'], ['תרגיל', ' ג ', 'יורם', '08:30', '10:30']]
course4 = ['61761', ['הרצאה', ' א ', 'וולקוביץ ולדימיר', '12:50', '15:50'], ['תרגיל', ' א ', 'כהן ראובן', '10:30', '12:20']]
course5 = ['61759', ['הרצאה', ' ב ', 'שינולד שרי', '10:30', '12:20'], ['תרגיל', ' ג ', 'שינולד שרי', '08:30', '10:30']]

# arranged in importance order
courses = [course1, course2, course4, course3, course5]


def open_driver():
    # Open driver
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    return webdriver.Chrome(chrome_options=options)


def open_braude():
    # login to Braude
    driver.get("https://info.braude.ac.il/yedion/fireflyweb.aspx?prgname=LoginValidation")
    WebDriverWait(driver, 100).until(ec.element_to_be_clickable((By.ID, 'otpmanualentry')))
    login_box = driver.find_element(By.ID, 'login')
    password_box = driver.find_element(By.ID, 'passwd')
    otp_check_box = driver.find_element(By.ID, "otpmanualentry")
    otp_check_box.click()
    otp_box = driver.find_element(By.ID, 'passwd1')
    login_box.send_keys(user_name)
    password_box.send_keys(user_pass)
    otp_box.send_keys(insert_otp_password())
    driver.find_element(By.ID, 'Logon').click()

    # signing to courses:
    WebDriverWait(driver, 100).until(ec.element_to_be_clickable((By.ID, 'kt_body')))

    driver.execute_script("javascript:send_form('MenuCall','-N,-N,-N20,-A','');")
    for i in range(1, 41):
        try:
            WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.ID, 'SubjectCode')))
            break
        except TimeoutException:
            print(f"try number {i}")
            driver.refresh()
            continue

    start = timeit.default_timer()
    for course in courses:
        subject_box = driver.find_element(By.ID, 'SubjectCode')
        subject_box.send_keys(course[0])
        #
        driver.find_element(By.ID, 'searchButton').click()
        WebDriverWait(driver, 100).until(ec.element_to_be_clickable((By.ID, 'divmsg11')))
        for i in range(1, len(course)):
            for index in range(1, NUMBER_OF_OPTIONS_PER_COURSE):
                try:
                    father_element = driver.find_element(By.ID, f'MyFather{index}')
                    description = father_element.text
                    for detail in course[i]:
                        if not description.__contains__(detail):
                            raise ValueError
                    if description.__contains__('הנך רשום לקבוצה זו'):
                        break
                    java_script = father_element.find_element(By.ID, f'REG{index}').get_attribute('href')
                    driver.execute_script(java_script)
                    print(f"נרשם ל {course[0]}, {course[i][0]} ")

                    break
                except NoSuchElementException:
                    type_of_element = 'מעבדה/תרגול'
                    if i == 1:
                        type_of_element = 'הרצאה'
                    print(f"קורס מספר {course[0]} : לא נמצא {type_of_element}.")
                    break
                except ValueError:
                    continue
        driver.execute_script("javascript:send_form('MenuCall','-N,-N,-N20,-A','');")
        WebDriverWait(driver, 100).until(ec.element_to_be_clickable((By.ID, 'SubjectCode')))

    stop = timeit.default_timer()
    print('Time: ', stop - start)


def insert_otp_password():
    return input('Enter otp password: ')


driver = open_driver()
if __name__ == '__main__':
    open_braude()


