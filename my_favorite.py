# -*- coding:utf-8 -*-
# !/usr/bin/python2.7
# FileName: my_favorite
# DateTime: 2019年02月01日11时36分45秒

import time
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import json



def favorite():
    # 定义1个浏览器
    browser = webdriver.PhantomJS(executable_path="/opt/phantomjs/bin/phantomjs")
    browser.get("https://graph.qq.com/oauth2.0/show?which=Login&display=pc&client_id=100290348"
                "&response_type=code&state=ab183433jKFQqXF6b25lX3Nuc6FToKFO2UxodHRwczovL3Nzby50"
                "b3V0aWFvLmNvbS9hdXRoL2xvZ2luX3N1Y2Nlc3MvP3NlcnZpY2U9aHR0cHM6Ly93d3cudG91dGlhby5"
                "jb20voVYBoUkAoUQAoUEYoU0YoUivd3d3LnRvdXRpYW8uY29toVIEolBMAKZBQ1RJT06g&redirect_u"
                "ri=http%3A%2F%2Fapi.snssdk.com%2Fauth%2Flogin_success%2F&scope=get_user_info,add_"
                "share,add_t,add_pic_t,get_info,get_other_info,get_fanslist,get_idollist,add_idol,g"
                "et_repost_list")
    # 设置等待加载时间
    wait = WebDriverWait(browser, 10)

    # 判断frame是否可以switch进去，如果可以的话，返回True并且switch进去
    wait.until(ec.frame_to_be_available_and_switch_to_it("ptlogin_iframe"))
    # 判断元素是否可见并且是可点击的
    wait.until(ec.element_to_be_clickable((By.ID, "switcher_plogin"))).click()
    # 输入账号、密码
    wait.until(ec.presence_of_element_located((By.NAME, "u"))).send_keys("QQ号码")
    wait.until(ec.presence_of_element_located((By.NAME, "p"))).send_keys("QQ密码")
    # 点击登陆
    wait.until(ec.element_to_be_clickable((By.ID, "login_button"))).click()

    # 点击进入包含【文章】【视频】【微头条】【收藏】栏目的 用户个人页面
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "head"))).click()

    # 切换到在最新标签打开的 用户个人页面 窗口
    latest_window = browser.window_handles[-1]
    browser.switch_to.window(latest_window)

    def load():
        print("正在加载第 1 页...")
        try:
            # 点击切换到【收藏】目录
            wait.until(ec.element_to_be_clickable((By.XPATH, '//li[@idx="3"]'))).click()

            # 等待开始20条收藏加载完毕
            wait.until(ec.visibility_of_element_located((By.XPATH, '//a[@href="/item/6528282665982886404/"]')))
        except TimeoutException:
            print("TimeoutException|Retry")
            load()
    load()

    # 下拉滚动条至窗口底部
    js = "window.scrollTo(0, document.body.scrollHeight);"
    # 总共有1236条收藏，(1236-20)/20，循环下拉滚动条至窗口底部61次，每次等待1秒保证内容加载完
    for i in range(2, 63):
        browser.execute_script(js)
        print("正在加载第 %d 页..." % i)
        time.sleep(2)

    soup = Bs(browser.page_source, "xml")
    # 获取到所有收藏的a标签（text为收藏标题）列表
    title_list1 = soup.select('a[class="link title"]')

    # 打印收藏的数量
    print(u"爬取总数为："+str(len(title_list1)))
    f = open("my_favorite_list", "w")
    title_dict = {}
    for each in title_list1:
        title_dict[each.get_text()] = "https://www.toutiao.com"+each['href']
    title_list2 = json.dumps({"titles": title_dict}, ensure_ascii=False)
    f.write(title_list2.encode("utf-8"))
    f.close()
    # 退出浏览器
    print("已退出浏览器")
    browser.quit()

if __name__ == "__main__":
    favorite()
