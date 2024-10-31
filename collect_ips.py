import requests
from bs4 import BeautifulSoup

import pyppeteer
import re
import os
import asyncio


# 目标URL列表
urls = [
        'https://stock.hostmonit.com/CloudFlareYes',
        'https://cf.090227.xyz',
        'https://ip.164746.xyz/ipTop10.html', 
        'https://ipdb.030101.xyz/api/bestcf.txt',
        ]


# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')


async def fetch_dynamic_content(url):
    browser = await pyppeteer.launch(
        executablePath="/usr/bin/google-chrome-stable",  # 替换为 Chromium 可执行文件的路径
        executablePath="D:/github/chrome/chrome-win/chrome.exe",  # 替换为 Chromium 可执行文件的路径
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )

    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(5)  # 等待5秒钟
    content = await page.content()
    await browser.close()
    return content


async def main():
    ip_ListAll = []
    for index, url in enumerate(urls):

        if url == 'https://stock.hostmonit.com/CloudFlareYes':
            html_content = await fetch_dynamic_content(url)
            # print(html_content)
        else:
            # 发送HTTP请求获取网页内容
            response = requests.get(url)
            html_content = response.text

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        elements = []
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://cf.090227.xyz':
            elements = soup.find_all('tr')
        elif url == 'https://stock.hostmonit.com/CloudFlareYes':
            elements = soup.find_all('tr')

        elif url == 'https://ip.164746.xyz/ipTop10.html' :
            elements = html_content.split(',')
        elif url == 'https://ipdb.030101.xyz/api/bestcf.txt':
            elements = html_content.split('\n')
        else:
            elements = soup.find_all('li')


        print(f'\n URL: {url} ')
        # print(f'Html: {elements} ')
        
        # 遍历所有元素,查找IP地址
        ip_ListSingleUrl = []
        ip_ListCM = []
        ip_ListCU = []
        ip_ListCT = []
        for element in elements:
            if hasattr(element, 'get_text'):
                tdsOneRow = element.find_all('td')
                for tdone in tdsOneRow:
                    td_text = tdone.get_text()
                    # print(f'IP地址td: {td_text}')
                    if re.match(ip_pattern, td_text):
                        ip_ListAll.append(td_text)
                        ip_ListSingleUrl.append(td_text)

                if len(tdsOneRow) > 1:
                    if tdsOneRow[0].get_text() == '移动':
                        ip_ListCM.append(tdsOneRow[1].get_text())
                    if tdsOneRow[0].get_text() == '联通':
                        ip_ListCU.append(tdsOneRow[1].get_text())
                    if tdsOneRow[0].get_text() == '电信':
                        ip_ListCT.append(tdsOneRow[1].get_text())

            else:
                if re.match(ip_pattern, element):
                    ip_ListAll.append(element)
                    ip_ListSingleUrl.append(element)
                    print(f'IP地址text: {element}')

        if len(ip_ListCM) > 0:
            with open(f'ip_site{index + 1}_CM.txt', 'w', encoding='utf-8') as file:
                for ip in ip_ListCM:
                        file.write(ip + '\n')

        if len(ip_ListCU) > 0:
            with open(f'ip_site{index + 1}_CU.txt', 'w', encoding='utf-8') as file:
                for ip in ip_ListCU:
                        file.write(ip + '\n')

        if len(ip_ListCT) > 0:
            with open(f'ip_site{index + 1}_CT.txt', 'w', encoding='utf-8') as file:
                for ip in ip_ListCT:
                        file.write(ip + '\n')

        if len(ip_ListSingleUrl) > 0:
            with open(f'ip_site{index + 1}.txt', 'w', encoding='utf-8') as file:
                for ip in ip_ListSingleUrl:
                        file.write(ip + '\n')

    # 创建一个文件来存储IP地址
    with open('ip.txt', 'w', encoding='utf-8') as file:
        for ip in ip_ListAll:
            file.write(ip + '\n')


    print('\n IP地址已保存到ip.txt文件中 \n')

# 运行主函数
asyncio.get_event_loop().run_until_complete(main())
