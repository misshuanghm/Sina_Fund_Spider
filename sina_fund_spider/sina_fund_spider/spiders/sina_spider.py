# -*- coding: utf-8 -*-
"""
scrapy是模拟http请求，而selenium可以模拟浏览器进行抓取，两者结合可以抓取任何网站
"""

import time
import scrapy

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # 导入WebDriver提供的等待方法WebDriverWait类
from selenium.webdriver.support import expected_conditions as EC  # 导入expected_conditions类并重命名为EC
from sina_fund_spider.items import FundBasicItem

driver = webdriver.Chrome()



# driver.implicitly_wait(10)


# 判断是否存在某元素并返回元素;即显示等待
def is_exist(text_string, search_count='all'):
    # 在10秒内每隔0.5秒检测一次当前页面元素是否存在，如果超过设置时间检测不到则抛出异常；until：直到返回值为True
    if search_count == 'one':
        element = WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, text_string)))
        return element
    else:
        elements = WebDriverWait(driver, 10, 0.5).until(EC.presence_of_all_elements_located((By.XPATH, text_string)))
        return elements


# 保证获取元素
def retrying_find_elements(by, by_type):
    while True:
        try:
            if by_type == 'xpath':
                elements = driver.find_elements_by_xpath(by)
                return elements
            else:
                pass
            break
        except BaseException:
            time.sleep(3)


# 判断元素是否可见，不可见就刷新(这里写错了，这只能判断元素是否用户可见，并不能判断元素是否存在)
# def is_visible(xpath_string):
#     while True:
#         try:
#             element = driver.find_element_by_xpath(xpath_string)
#             if element.is_displayed():
#                 break
#         except BaseException:
#             driver.refresh()

# 判断元素是否不存在，不存在就刷新页面
def is_visible(xpath_string):
    while True:
        try:
            # 每隔0.5秒检查元素是否存在
            WebDriverWait(driver, 2, 0.5).until(EC.presence_of_element_located((By.XPATH, xpath_string)))
            break
        except BaseException:
            print('页面没加载完全')
            driver.refresh()


# 获取元素属性
def get_attr(xpath_string, attribute):
    # 获取一组元素
    # elements = driver.find_elements_by_xpath(xpath_string)
    while True:
        try:
            elements = retrying_find_elements(xpath_string, 'xpath')
            # 获取元素文本
            if attribute == 'text':
                elements_text = []  # 每页相同结构元素文本集合
                for each_element in elements:
                    # 获取单个元素文本并添加到总列表
                    print(each_element.text)
                    elements_text.append(each_element.text)
                    # 用get_attribute获取元素text时有的取不出来
                    # elements_text.append(each_element.get_attribute('text'))
                return elements_text
            # 获取元素连接
            elif attribute == 'href':
                elements_href = []
                for each_element in elements:
                    elements_href.append(each_element.get_attribute('href'))
                return elements_href
            else:
                print('False!!')
            break
        except BaseException:
            time.sleep(2)


# 讲页面抓取元素存进item中,注意能直接用FundBasicItem()作为形参，不会出错；碰到不可以的情况可以尝试用字符串代替解决
def get_item(item_type):
    if item_type == ():
        item = item_type
        item['fund_code'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/td[2]/a', 'text')
        item['fund_name'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/td[3]/a', 'text')
        item['net_worth'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/th[1]', 'text')
        item['accumulated_net_worth'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/th[2]', 'text')
        item['previous_net_worth'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/th[3]', 'text')
        item['rise_and_fall'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/th[4]', 'text')
        item['growth_rate'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/th[5]', 'text')
        item['subscription_status'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/td[4]', 'text')
        item['net_worth_date'] = get_attr('//*[@id="jjjzC"]/table/tbody/tr/td[5]', 'text')
        return item


# 解决Stale Element Reference Exception
def retrying_find_click(by, by_type):
    result = False
    attempts = 0
    while attempts < 5:
        try:
            if by_type == 'xpath':
                driver.find_element_by_xpath(by).click()
            elif by_type == 'link_text':
                driver.find_element_by_link_text(by).click()
            else:
                pass
            result = True
            break
        except BaseException:
            pass
        attempts = attempts + 1
    return result


# 继承spider基类
class SinaSpiderSpider(scrapy.Spider):
    # 每一个爬虫的唯一标识
    name = 'sina_spider'
    # 允许爬行的域名，不需要www前缀
    allowed_domains = ['sina.com']
    # 定义爬虫爬取的起始点，起始点可以是多个，这里只有一个
    start_urls = ['http://vip.stock.finance.sina.com.cn/fund_center/index.html#jzkfall']

    # 实现start_requests方法，替代start_urls属性
    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True)

    # 页面解析函数，提取页面中的数据以及链接
    def parse(self, response):
        # 获取首页url
        index_url = response.url + '#jzkfall'
        driver.get(index_url)
        # 判断元素是否可见，其实是想知道页面是否加载完全
        is_visible('//*[@id="jjjzC"]/table/tbody/tr[1]/td[1]')
        # 浏览器全屏显示
        driver.maximize_window()
        # 统计基金总页数,text为字符串需要转化为int类型
        page_count = int(is_exist('//p[@id="jjjzP"and @class="page"]/a[3]', 'one').get_attribute('text'))
        for i in range(0, page_count - 1):
            # 每页总连接
            # all_url_per_page = get_attr('//*[@id="jjjzC"]/table/tbody/tr/td[2]/a')
            # for each_fund_url in all_url_per_page:
            now_handle = driver.current_window_handle
            for each_page_number in range(0, 40):
                # time.sleep(2)
                # 每只基金的url
                each_page_url = '//*[@id="jjjzC"]/table/tbody/tr[' + str(each_page_number + 1) + ']/td[2]/a'
                # driver.find_element_by_xpath(each_page_url).click()
                # driver.find_elements_by_xpath('//*[@id="jjjzC"]/table/tbody/tr/td[2]/a').pop(each_page_number).click()
                retrying_find_click(each_page_url, 'xpath')
                # 转到单只基金所在页面
                driver.switch_to.window(driver.window_handles[1])
                # time.sleep(3)
                driver.close()  # 关闭页面
                driver.switch_to.window(now_handle)  # 回到主页面
            # 获取第一页最新数据
            if i == 0:
                time.sleep(10)
                yield get_item(FundBasicItem())
            # 进入下一页并获得最新数据
            # driver.find_element_by_link_text('下一页').click()
            retrying_find_click('下一页', 'link_text')
            # 这里必须要经过一点时间的等待，当点击下一页后，下一页可能实际上还没有跳转，这时候获取页面元素实际上获取的
            # 是前一页的，之后再取元素的text文本时就会出错，
            time.sleep(3)
            yield get_item(FundBasicItem())
        # 退出相关驱动程序并且关闭所有窗口-
        driver.quit()
