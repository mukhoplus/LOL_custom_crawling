# ... Made By Mukho
# ... 2022-10-24 MON
# ... Last Update : 2022-10-24 MON

#-*-coding: utf-8 -*-
import csv

class Application:
    def __init__(self):
        # Testcase
        # self.data = [['ups', 'made by google', 'itx 청춘', '', '묵호']]
        
        # data = [team_name, leader, user1, user2, user3, user4, user5, user6, user7]
        self.data = []
        self.output = [['팀명', '닉네임', '현재 티어', '2021 티어', '2020 티어', '모스트1', '모스트2', '모스트3', '모스트4', '모스트5']]
    
    def run(self):
        self.load()
        self.makeURLs()

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

    def makeURLs(self):
        with open("output.csv", "w", encoding='utf-8-sig', newline='') as f:
            for team in self.data:
                users = team[1:]

                team_url = '=hyperlink("http://fow.kr/multi#'
                for i in range(len(users)):
                    if i != 0:
                        team_url += ','

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