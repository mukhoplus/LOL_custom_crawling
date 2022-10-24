# ... Made By Mukho
# ... 2022-10-24 MON
# ... Last Update : 2022-10-24 MON

#-*-coding: utf-8 -*-
import bs4
import urllib.parse as parse
import urllib.request as request
import csv
import os
import time
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class Application:
    def __init__(self):
        # Testcase
        # self.data = [['ups', 'made by google', 'itx 청춘', '', '묵호']]
        
        # data = [team_name, leader, user1, user2, user3, user4, user5, user6, user7]
        self.data = []
        self.output = [['팀명', '닉네임', '현재 티어', '2021 티어', '2020 티어', '모스트1', '모스트2', '모스트3', '모스트4', '모스트5']]
    
    def run(self):
        self.load()
        #self.makeURLs()
        #self.openURLs()
        self.crawling()
        #self.save()
        
    def crawling(self):
        i = 0
        while i < len(self.data):     
            num = 1
            while num < len(self.data[i]):
                if self.data[i][num] == '':
                    continue
    
                out = [self.data[i][0]]
                #time.sleep(0.6)
                try:
                    # url로 크롤링
                    url = "https://www.op.gg/summoner/userName=" + parse.quote(self.data[i][num])
                    req = request.urlopen(url)
                    soup = bs4.BeautifulSoup(req, 'html.parser')
                    isError = False # 잘못된 아이디인가

                    if soup.find('h2').text == "This summoner is not registered at OP.GG. Please check spelling.": # 등록이 안되어 있는가?
                        continue
                    
                    user_info = list(str(soup.find_all('meta')[-2])[15:-29].split(' / '))
                    temp_most_list = []
                    if len(user_info) > 3:
                        temp_most = list(user_info[3].split(', '))
                        for m in temp_most:
                            m = m.split(' - ')[0]
                            temp_most_list.append(m)

                    # 닉네임, 현재 시즌 티어
                    out.append(user_info[0])
                    tier_info = "Unranked" if user_info[1].find('Lv') == 0 else " ".join(list(user_info[1].split())[:2]).replace(' ', '')
                    out.append(tier_info)
                    
                    # 직접 정규화
                    pre_season_html = str(soup.find("div", "css-1d2nav3 eioz3425").find_all("li"))[1:-1]
                    while(True):
                        if '<div class="" style="position:relative">' in pre_season_html:
                            s = pre_season_html.find('<div class="" style="position:relative">')
                            pre_season_html = pre_season_html[:s] + pre_season_html[s+40:]
                        else:
                            break
                    while(True):
                        if '<!-- -->' in pre_season_html:
                            s = pre_season_html.find('<!-- -->')
                            pre_season_html = pre_season_html[:s] + pre_season_html[s+8:]
                        else:
                            break
                    while(True):
                        if '<b>' in pre_season_html:
                            s = pre_season_html.find('<b>')
                            pre_season_html = pre_season_html[:s] + pre_season_html[s+3:]
                        else:
                            break
                    while(True):
                        if '</b>' in pre_season_html:
                            s = pre_season_html.find('</b>')
                            pre_season_html = pre_season_html[:s] + pre_season_html[s+4:]
                        else:
                            break
                    while(True):
                        if '<li>' in pre_season_html:
                            s = pre_season_html.find('<li>')
                            pre_season_html = pre_season_html[:s] + pre_season_html[s+4:]
                        else:
                            break
                    while(True):
                        if '</li>' in pre_season_html:
                            s = pre_season_html.find('</li>')
                            pre_season_html = pre_season_html[:s] + pre_season_html[s+5:]
                        else:
                            break
                    while(True):
                        if '</div>' in pre_season_html:
                            s = pre_season_html.find('</div>')
                            pre_season_html = pre_season_html[:s] + pre_season_html[s+6:]
                        else:
                            break

                    pre_tier = list(pre_season_html.split(', '))
                    s21 = 'Unranked'
                    s20 = 'Unranked'
                    for tier in pre_tier:
                        if 'S2021' in tier:
                            tier = tier.replace('  ', '')
                            s21 = tier.split(' ')[1].capitalize()
                        if 'S2020' in tier:
                            tier = tier.replace('  ', '')
                            s20 = tier.split(' ')[1].capitalize()

                    out.append(s21)
                    out.append(s20)
                    for j in range(5):
                        try:
                            out.append(temp_most_list[j])
                        except:
                            out.append('')
                    print(out)
                    num += 1
                except Exception as e:
                    print(e)
            i += 1

    def save(self):
        try:
            with open("output.csv", "w", encoding='utf-8-sig', newline='') as f:
                wr = csv.writer(f)
                for i in range(len(self.output)):
                    wr.writerow(self.output[i])
        except:
            print("저장하지 못했습니다.")

    def load(self):
        try:
            f = open('data.csv', 'r', encoding='utf-8')
            rd = csv.reader(f)
            for i in rd:
                if rd.line_num < 5:
                    continue
                self.data.append(i[0:7])
            f.close()
        except:
            print("불러오지 못했습니다.")

    def openURLs(self):
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(executable_path='./chromedriver/chromedriver.exe', chrome_options=chrome_options)

        for team in self.data:
            tabs = driver.window_handles
            users = team[1:]

            team_url = 'http://fow.kr/multi#'
            for i in range(len(users)):
                if i != 0:
                    team_url += ','
                team_url += parse.quote(users[i])
            
            driver.switch_to.window(tabs[-1])
            driver.get(team_url)
            driver.execute_script('window.open("about:blank", "_blank");')
        os.system("pause")

    def makeURLs(self):
        with open("output.csv", "w", encoding='utf-8-sig', newline='') as f:
            for team in self.data:
                users = team[1:]

                team_url = '=hyperlink("http://fow.kr/multi#'
                for i in range(len(users)):
                    if i != 0:
                        team_url += ','
                    #parse.quote(users[i])
                    team_url += users[i]
                team_url += '", "' + team[0] + '")'
                try:
                    wr = csv.writer(f)
                    team_url = [team_url]
                    wr.writerow(team_url+users)
                except:
                    print("저장하지 못했습니다.")

# Main Process
app = Application()
app.run()