# _*_ coding :utf-8 _*_
# @Time   : 2022/10/28 15:14
# @Author : ataobiu
# @File   : PHP+MySQL动态网站开发文档图片获取
# @Project: Spider-practice

import requests
import json


# 登录网站
def login(account, passwd):
    # post请求
    post_url = 'https://stu.ityxb.com/back/bxg_anon/login'
    # 定制past_date
    post_date = {
        'automaticLogon': 'false',
        'username': account,
        'password': passwd,
    }
    # 访问网站 使用session 携带cookie进行下一次访问
    session = requests.session()
    response = session.post(url=post_url, data=post_date)
    # 获取状态码 (200)
    # print(response.status_code)
    return session


def get_page(session, page):
    get_page_url = 'https://vip.ow365.cn/PW/GetPage?'
    # 解决起始接口img='',page='0'
    date = {
        'f': 'YXR0YWNobWVudC1jZW50ZXIuYm94dWVndS5jb20uODBcNDI4Zjk1MTg5MWIyNDE3NzkxNGRmMjZmN2FmNmFjNWUucGRm',
        'img': '',
        'isMobile': 'false',
        'vid': 'slbEvnyBDUYEtZr5*aw9VQ--',
        'dk': '0',
        'ver': '2',
        'sn': '0'
    }

    date2 = {
        'f': 'YXR0YWNobWVudC1jZW50ZXIuYm94dWVndS5jb20uODBcNDI4Zjk1MTg5MWIyNDE3NzkxNGRmMjZmN2FmNmFjNWUucGRm',
        'img': '',
        'isMobile': 'false',
        'vid': 'slbEvnyBDUYEtZr5*aw9VQ--',
        'dk': '0',
        'ver': '2',
        'sn': page
    }
    if page == 0:
        page_response = session.get(url=get_page_url, params=date)
    else:
        page_response = session.get(url=get_page_url, params=date2)
    # json 重载page_response，类型为dict
    page_response = json.loads(page_response.text)
    # 打印接口响应数据
    # print(page_response)

    # 获取img ID，pageCount 图片数量
    img = page_response['NextPage']
    pageCount = page_response['PageCount']
    # print(img)
    # print(pageCount)

    return img, pageCount


def down_img(session, img):
    img_url = 'https://vip.ow365.cn/img?'

    date3 = {
        'img': img,
        'tp': ''
    }

    img_down = session.get(url=img_url, params=date3)
    # 打印图片状态码
    # print(img_down.status_code)

    # 打印图片url地址
    print(img_down.url)

    # 下载图片,但是未成功，图片数据错误，
    with open('./Download/PHP+MySQL动态网站开发' + str(page + 1) + ".png", 'wb') as fp:
        fp.write(img_down.content)


if __name__ == '__main__':
    # 账号密码
    account = input('请输入账号：')
    passwd = input('请输入密码：')

    # 登录网站
    session = login(account, passwd)

    # 获取img数量
    pageCount = get_page(session, page=0)[1]
    # 根据page循环获取图片ID
    for page in range(0, pageCount):
        img = get_page(session, page)[0]

        # 下载图片
        # 打印当前图片page
        print(page)
        down_img(session, img)
