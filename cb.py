#coding=utf-8
import os
import time
import random
import emailDemo

USER_AGENT_LIST = [ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1", \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"
]

URL = 'https://medium.com/_/api/collections/c114225aeaf7/stream\?to\=\{timestamp\}\&page\=4'

def comm():
    clock = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) 
    file_name = 'cb_' + clock + '.html'
    index = random.randint(0, len(USER_AGENT_LIST))
    commend = 'wget --user-agent=\"' + USER_AGENT_LIST[index] + '\" ' + URL + ' -qO ' + file_name
    print(commend)
    os.system(commend)
    return file_name

def load_file(file_name):
    f = open(file_name,'r')
    Text = f.readlines()
    res = []
    for line in Text:
        titles = line.split("\"text\":\"")
        for title in titles:
            if title is titles[0]:
                continue
            index = title.find("\"") 
            if index != 0 and "launching on" in title[:index]:
                res.append(title[:index])
    f.close()
    return res

#提取单条标题的币种
def extract_sig(title):
    res = []
    data = title.split(",")
    for it in data:
        l_index = it.find("(")
        r_index = it.find(")")
        res.append(it[l_index + 1 : r_index])
    return res

#提取所有标题的币种
def extract(titles):
    res = []
    for title in titles:
        res_sig = extract_sig(title)
        for it in res_sig:
            if it not in res:
                res.append(it)
    return res

def get_ori_coins():
    f = open('cb.txt','r')
    ori_coins = []
    cbtxt = f.readlines()
    for line in cbtxt:
        res = line.strip().split(",")
        ori_coins.extend(res)
    return ori_coins

#比较新旧币种，获取新币种
def get_new_coin(coins, ori_coins):
    new_coins = []
    for coin in coins:
        if coin not in ori_coins:
            new_coins.append(coin)
    return new_coins

#更新cb.txt文件
def update_coins(coins):
    f = open('cb.txt','w+')
    f.write(",".join(coins))
    f.close()

#发出上币警报
def warn():
    print("发出上币警报")

    


#主流程
def run():
    file_name = comm()
    #file_name = 'cb_2021-08-13-18-16-30.html'
    titles = load_file(file_name)
    coins = extract(titles)
    #print(titles)
    #print(",".join(coins))
    os.remove(file_name)
    ori_coins = get_ori_coins()
    new_coins = get_new_coin(coins, ori_coins)
    print(coins)
    print(ori_coins)
    print(new_coins)
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if len(new_coins) > 0:
        update_coins(coins)
        emailDemo.send_email(now,new_coins)
        commend = 'echo "' + now + '|new coins (' + ",".join(new_coins) + ')" >> cb.log'
    else:
        commend = 'echo "' + now + '|no new coins(' + ",".join(ori_coins) + ')" >> cb.log'
    #print(commend)
    os.system(commend)

def main():
    while True:
        now_hour = int(time.strftime("%H", time.localtime()))
        interval_sec = random.randint(200, 300)
        if now_hour >= 21 or now_hour <= 8:
            interval_sec = random.randint(40, 60)
        time.sleep(interval_sec)
        run()

if __name__ == '__main__':
    main()
