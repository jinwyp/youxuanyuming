import os
import requests

def get_ip_list(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.strip().split('\n')

def get_cloudflare_zone(api_token):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    response.raise_for_status()
    zones = response.json().get('result', [])
    if not zones:
        raise Exception("No zones found")
    return zones[0]['id'], zones[0]['name']

def delete_existing_dns_records(api_token, zone_id, subdomain, domain):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    record_name = domain if subdomain == '@' else f'{subdomain}.{domain}'
    while True:
        response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={record_name}', headers=headers)
        response.raise_for_status()
        records = response.json().get('result', [])
        if not records:
            break
        for record in records:
            delete_response = requests.delete(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record["id"]}', headers=headers)
            delete_response.raise_for_status()
            print(f"Del {subdomain}:{record['id']}")

def update_cloudflare_dns(ip_list, api_token, zone_id, subdomain, domain):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    record_name = domain if subdomain == '@' else f'{subdomain}.{domain}'

    tempCounter = 0
    for ip in ip_list:
        tempCounter += 1
        # 每个子域名只添加一条A记录
        if tempCounter < 2:
            data = {
                "type": "A",
                "name": record_name,
                "content": ip,
                "ttl": 1,
                "proxied": False
            }
            print(f"Prepare to add {record_name}:{ip}")
            response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', json=data, headers=headers)
            if response.status_code == 200:
                print(f"Added {record_name}:{ip}")
            else:
                print(f"Failed to add A record for IP {ip} to subdomain {subdomain}: {response.status_code} {response.text}")

if __name__ == "__main__":
    api_token = os.getenv('CF_API_TOKEN')
    # print(f"CF_API_TOKEN: {api_token}")

    # 示例URL和子域名对应的IP列表
    subdomain_ip_mapping = {
        'cfsite1cmx1': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site1_CM.txt',
        'cfsite1cmx2': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site1_CM.txt',
        'cfsite1ctx1': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site1_CT.txt',
        'cfsite1ctx2': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site1_CT.txt',
        'cfsite1cux1': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site1_CU.txt',
        'cfsite1cux2': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site1_CU.txt',

        'cfsite2cmx1': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site2_CM.txt',
        'cfsite2cmx2': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site2_CM.txt',
        'cfsite2ctx1': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site2_CT.txt',
        'cfsite2ctx2': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site2_CT.txt',

        'cfsite3x1': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site3.txt',
        'cfsite3x2': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site3.txt',

        'cfsite4x1': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site4.txt',
        'cfsite4x2': 'https://raw.githubusercontent.com/jinwyp/youxuanyuming/refs/heads/main/ip_site4.txt',

        # 添加更多子域名和对应的IP列表URL
    }
    
    try:
        # 获取Cloudflare域区ID和域名
        zone_id, domain = get_cloudflare_zone(api_token)
        
        # print(f"Zone ID: {zone_id}, Domain: {domain}")

        for subdomain, url in subdomain_ip_mapping.items():
            # 获取IP列表
            ip_list = get_ip_list(url)

            last_char = subdomain[-1]
            if last_char.isdigit():
                print(f"last_char: {last_char}")
                num_to_reduce = int(last_char)
                
                if num_to_reduce < len(ip_list):
                    ip_list = ip_list[num_to_reduce:]  # 从头部减少 num_to_reduce 个元素

            # 删除现有的DNS记录
            delete_existing_dns_records(api_token, zone_id, subdomain, domain)
            # 更新Cloudflare DNS记录
            update_cloudflare_dns(ip_list, api_token, zone_id, subdomain, domain)

    except Exception as e:
        print(f"Error: {e}")
