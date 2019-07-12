from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
from time import sleep
import time
import random
import re


class FictionSearch(object):
    def __init__(self, readname='ids.txt', savename='info.csv'):
        # 传入两个参数，分别是网页翻页ID，和保存内容
        self.readname = readname
        self.savename = savename
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        self.get_csv()

    def get_csv(self):
        # 创建一个表格，并且给表格添加标题行
        with open(self.savename, 'w', newline='')as file:
            filednames = ['fiction', 'author', 'infomation']
            write = csv.DictWriter(file, fieldnames=filednames)
            write.writeheader()

    def write_info(self, info_dic):
        # 写入单个信息，传入的参数是一个字典，字典的key跟表格的标题对应
        with open(self.savename, 'a', newline='') as file:
            filednmaes = ['fiction', 'author', 'infomation']
            write = csv.DictWriter(file, fieldnames=filednmaes)
            write.writerow(info_dic)

    def get_ids(self):
        with open(self.readname, 'r') as f:
            lines = f.readlines()
        ids = [k.replace('\n', '').strip() for k in lines]
        return ids

    def get_info(self, id):
        element_num = 0
        element_flag = True
        dic = {}
        url = "http://book.sfacg.com/List/default.aspx?tid=21&PageIndex={}".format(id)
        self.driver.get(url)
        while element_flag:
            element_num += 1

            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                'body > div:nth-child(3) > div > div.bsubcon > div.comic_cover.Blue_link3 > ul:nth-child({})'.format(
                                                                    element_num))))

                about_btn = self.driver.find_element(By.CSS_SELECTOR,
                                                     'body > div:nth-child(3) > div > div.bsubcon > div.comic_cover.Blue_link3 > ul:nth-child({})'.format(
                                                         element_num))
                about = about_btn.text.expandtabs(tabsize=0).replace('\n', '').replace('\r', '').replace(' ', '')

                # 截取书名
                dic['fiction'] = about.split('作')[0]
                # 截取作者
                str = '者'
                str1 = '综'
                author_str = re.findall(r"{}(.+?){}".format(str, str1), about)
                dic['author'] = author_str[0].replace('：', '')
                # 截取基本信息
                str2 = "综合信息"
                str3 = "。"
                infomation_str = re.findall(r"{}(.+?){}".format(str2, str3),about)
                try:
                    dic['infomation'] = infomation_str[0].replace('：', '')
                except:
                    print("没有：")
                    dic['infomation'] = infomation_str
                print("书名：{}\n作者：{}\n信息：{}".format(dic['fiction'],dic['author'],dic['infomation'] ))
                self.write_info(dic)

            except TimeoutException as e:
                print(e)
                break

    def main(self):
        # 循环爬取、并且打印相应的操作过程
        sleep(10)
        print("准备爬取")
        ids = self.get_ids()
        counter = len(ids)
        i = 1
        for id in ids:
            self.get_info(id)
            sleep(random.choice([3, 2]))
            print('总计{}个页面，已经爬取{}个'.format(counter, i))
            i += 1


if __name__ == '__main__':
    start = time.time()
    fc = FictionSearch()
    fc.main()
    fc.driver.close()
    end = time.time()
    print('运行结束，总耗时：{:.2f}秒'.format(end - start))
