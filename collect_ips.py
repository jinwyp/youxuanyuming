import requests
from bs4 import BeautifulSoup
import pyppeteer
import re
import os
import sys
import asyncio



# 目标URL列表
urls = [
        'https://stock.hostmonit.com/CloudFlareYes',
        'https://cf.090227.xyz',
        'https://ip.164746.xyz/ipTop10.html', 
        'https://ipdb.api.030101.xyz/?type=bestcf&country=true',
        ]


# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它

def cleanup_files():
    try:
        if os.path.exists('ip.txt'):
            os.remove('ip.txt')
        
        for index, url in enumerate(urls):
            if os.path.exists(f'ip_site{index + 1}.txt'):
                os.remove(f'ip_site{index + 1}.txt')
            if os.path.exists(f'ip_site{index + 1}_CM.txt'):
                os.remove(f'ip_site{index + 1}_CM.txt')
            if os.path.exists(f'ip_site{index + 1}_CU.txt'):
                os.remove(f'ip_site{index + 1}_CU.txt')
            if os.path.exists(f'ip_site{index + 1}_CT.txt'):
                os.remove(f'ip_site{index + 1}_CT.txt')
            
    except OSError as e:
        print(f"Error cleaning up files: {str(e)}")

async def fetch_dynamic_content(url: str):
    browser = None

    chromeExecutablePath="/usr/bin/google-chrome-stable"
    if sys.platform == "win32":
        chromeExecutablePath="D:/github/chrome/chrome-win/chrome.exe"
    elif sys.platform == "darwin":
        chromeExecutablePath="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    try:
        browser = await pyppeteer.launch(
            executablePath=chromeExecutablePath,  # 替换为 Chromium 可执行文件的路径
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )

        page = await browser.newPage()
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        await page.goto(url, {'waitUntil': 'networkidle2', 'timeout': 60000})
        await asyncio.sleep(10)  # 等待10秒钟

        content = await page.content()
        return content
    
    except Exception as e:
        print(f"Error fetching content from {url}: {str(e)}")
        return None
    
    finally:
        if browser:
            await browser.close()

async def main():
    ip_ListAll = []
    for index, url in enumerate(urls):

        if url == 'https://stock.hostmonit.com/CloudFlareYes':
            html_content = await fetch_dynamic_content(url)
            print(html_content)
        else:
            # 发送HTTP请求获取网页内容
            response = requests.get(url)
            html_content = response.text

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        elements = []
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://stock.hostmonit.com/CloudFlareYes':
            elements = soup.find_all('tr')
        elif url == 'https://cf.090227.xyz':
            elements = soup.find_all('tr')

        elif url == 'https://ip.164746.xyz/ipTop10.html' :
            elements = html_content.split(',')
        elif url == 'https://ipdb.api.030101.xyz/?type=bestcf&country=true':
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
                # element 是 BeautifulSoup 对象，可以使用 get_text() 方法
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
                # element 是纯字符串，直接进行正则匹配
                if re.match(ip_pattern, element):
                    ip_ListAll.append(element)
                    ip_ListSingleUrl.append(element)
                    print(f'IP地址 (纯字符串): {element}')

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
