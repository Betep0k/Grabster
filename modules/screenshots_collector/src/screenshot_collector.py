from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
import os
import sys
import functools

from core.queue_jobs import OutputJob, ScreenshotJob


class ScreenshotCollector:

    def __init__(self, settings, modules, coloring):
        self.settings = settings
        self.modules = modules
        self.coloring = coloring
        self.save_dir = 'web-screenshots/'  # todo: get from settings
        self.total_targets = 0
        if not os.path.exists(self.save_dir):  # todo: create only if flag set
            os.makedirs(self.save_dir)

    def check_availability(self):
        return

    def collect_screenshots(self, global_state):
        for service in global_state.state['services']:
            self.get_screenshot(service['service'])
            print(' - %s://%s:%s/ (%s)' % (service['service']['proto'], service['service']['host'], service['service']['port'], service['service']['vhost']))

    def get_screenshot(self, service):
        proto = service['proto']
        ip = service['host']
        port = service['port']
        vhost = service['vhost']
        DRIVER = 'chromedriver'
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--start-maximized")
        # https://stackoverflow.com/questions/48450594/selenium-timed-out-receiving-message-from-renderer/52340526#52340526

        # if vhost is None:
        #    vhost = ''

        if vhost != '':
            # todo: тут потенциально возможна ошибка
            # если на входе IP это на самом деле домен
            # в этом случае MAP будет из домена в домен
            # хз как он это обрабатывает
            chrome_options.add_argument("--host-resolver-rules=MAP %s %s" % (vhost, ip))
            driver = webdriver.Chrome(DRIVER, options=chrome_options)
            driver.set_window_position(0, 0)
            driver.set_window_size(1920, 1080)
            driver.set_page_load_timeout(10)
            try:
                driver.get('%s://%s:%s/' % (proto, vhost, port))
            except TimeoutException:
                return
            except Exception as e:
                return
        else:
            driver = webdriver.Chrome(DRIVER, options=chrome_options)
            driver.set_window_position(0, 0)
            driver.set_window_size(1920, 1080)
            driver.set_page_load_timeout(10)
            try:
                driver.get('%s://%s:%s/' % (proto, ip, port))
            except TimeoutException:
                return
            except Exception as e:
                # print(proto, ip, port)
                # print(e)
                return

        try:
            # try:
            # 	WebDriverWait(driver, 1).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            # except Exception as e:
            # 	print(e)
            # 	pass
            sleep(2)  # должно быть динамически
            screenshot = driver.save_screenshot('web-screenshots/%s_%s_%s.png' % (ip, port, vhost))
        except UnexpectedAlertPresentException:
            # todo
            # Handle alerts
            pass

        # todo: добавить работу с vhost
        # брать delay из настроек
        # time.sleep(2)
        driver.quit()
