import datetime
import platform
import random
import subprocess
import sys
import time

try:
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from tqdm import tqdm
    from webdriver_manager.chrome import ChromeDriverManager
except ModuleNotFoundError:
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed.")
    print("Please restart the program.")
    exit(1)

class TaiGiTranslator:

    def __init__(self, timeout: int = 30):
        self.options = Options()
        self.options.add_argument("--enable-javascript")
        self.options.add_argument("--incognito")
        self.options.add_argument("--lang=zh-TW")
        self.options.add_argument("--headless")
        self.timeout = timeout
        self.browser = self.get_browser()
        self.base_url = "https://itaigi.tw/k/"

    def get_browser(self) -> webdriver:
        service = None
        if platform.system() == "Windows": # Windows
            print("Windows detected.")
            service = Service(ChromeDriverManager(os_type="win32").install())
        elif platform.system() == "Linux": # Linux
            print("Linux detected.")
            service = Service(ChromeDriverManager(os_type="linux64").install())
        elif platform.system() == "Darwin": # MacOS
            print("MacOS detected.")
            try:
                from get_chrome_driver import GetChromeDriver
            except ModuleNotFoundError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "get-chrome-driver"])
                from get_chrome_driver import GetChromeDriver
            service = GetChromeDriver().install()
        else:
            print("OS not supported.")
            exit(1)

        browser = webdriver.Chrome(service=service, options=self.options)
        browser.command_executor.set_timeout(self.timeout)
        return browser

    def parse(self, soup: BeautifulSoup) -> list:
        '''
            Param:
                soup: BeautifulSoup object
            Return:
                candidates: a list of candidates
        '''
        candidates = list()
        cards = soup.find_all('div', {'class': 'su ui card'})
        for card in cards:
            content = card.find('div', {'class': 'content'})
            title = content.find('div', {'class': 'left floated'}).h2.text.strip()
            description = content.find('div', {'class': 'description'})
            tai_lo = description.text.strip().split('出處：')[0].split('/')
            come_from = description.find('div', {'class': 'content'}).text.strip()[3:]
            chinese_list = description.find_all('a', {'class': 'item'})
            chinese_list = [x.text.strip() for x in chinese_list]
            votes = content.find('div', {'class': 'menu'}).find('a', {'class': 'item'}).find('span', {'class': 'label'}).text.strip()
            candidates.append({
                'title': title,
                'tai_lo': tai_lo,
                'come_from': come_from,
                'chinese_list': chinese_list,
                'votes': votes
            })
        return candidates

    def make_a_pick(self, candidates: dict) -> dict:
        '''
        # Param:
        #     candidates: a list of candidates
        # Return:
        #     a candidate
        '''
        from_where = ["臺灣閩南語常用詞辭典", "台文華文線頂辭典"]
        list_of_candidates = list()
        for candidate in candidates:
            if candidate['come_from'] in from_where:
                list_of_candidates.append(candidate)
        if len(list_of_candidates) > 0:
            max_votes_candidate = list_of_candidates[0]
            for candidate in list_of_candidates:
                if self.query in candidate['chinese_list']:
                    return candidate
                if candidate['votes'] > max_votes_candidate['votes']:
                    max_votes_candidate = candidate
            return max_votes_candidate
        for candidate in candidates:
            if self.query in candidate['chinese_list']:
                return candidate
        list_of_candidates.sort(key=lambda x: x['votes'], reverse=True)
        return list_of_candidates[0]

    def checkoutput(self, output: dict) -> tuple:
        if not any('\u4e00' <= c <= '\u9fff' for c in output['title']):
            return (output['chinese_list'][0], output['title'])
        else: return (output['title'], output['tai_lo'][0])

    def log(self):
        with open('log.txt', 'a', encoding='utf8') as f:
            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f'[{time_stamp}] Query: {self.query} Random int: {self.ran_time} Results: {self.candidates}\n')

    def translate(self, query: str) -> tuple:
        '''
            Param:
                query: 中文詞
            Return:
                cands: 台文與台羅
        '''
        self.query = query.strip()
        if not self.query or self.query == "": return (None, None)
        if not all('\u4e00' <= c <= '\u9fff' for c in self.query): return (None, None)

        self.browser.get(self.base_url + self.query)
        self.ran_time = random.randint(5, 10)
        time.sleep(self.ran_time)

        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        self.candidates = self.parse(soup)
        self.log()

        if len(self.candidates) == 0: return (None, None)
        candidate = self.make_a_pick(self.candidates)
        return self.checkoutput(candidate)

    def batch_translate(self, query_list: list) -> list:
        '''
            Param:
                query_list: 中文詞列表
            Return:
                cands: 台文與台羅列表
        '''
        Progressbar = tqdm(query_list)
        cands = list()
        for query in query_list:
            cands.append(self.translate(query))
            Progressbar.update(1)
        return cands

    def close(self):
        self.browser.quit()


if __name__ == '__main__':
    translator = TaiGiTranslator()
    print(translator.translate('醫院'))
    translator.close()
