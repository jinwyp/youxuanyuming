import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://ip.164746.xyz/ipTop10.html', 
        'https://cf.090227.xyz'
        ]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

ip_matches = []
for url in urls:
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 根据网站的不同结构找到包含IP地址的元素
    if url == 'https://ip.164746.xyz/ipTop10.html':
        elements = response.text.split(',')
    elif url == 'https://cf.090227.xyz':
        elements = soup.find_all('tr')
    else:
        elements = soup.find_all('li')
    
    # print(f'URL: {url} ')
    # print(f'Html: {elements} ')
    
    # 遍历所有元素,查找IP地址

    for element in elements:
        if hasattr(element, 'get_text'):
            for tdone in element.find_all('td'):
                td_text = tdone.get_text()
                if re.match(ip_pattern, td_text):
                    ip_matches.append(td_text)
                    # print(f'IP地址: {td_text}')
        else:
            if re.match(ip_pattern, element):
                ip_matches.append(element)
                # print(f'IP地址: {element}')


# 创建一个文件来存储IP地址
with open('ip.txt', 'w') as file:
    
    # 如果找到IP地址,则写入文件
    for ip in ip_matches:
        file.write(ip + '\n')


print('IP地址已保存到ip.txt文件中。')
