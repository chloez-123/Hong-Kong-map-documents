#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 11 00:21:14 2025

@author: chloezhao
"""

import pandas as pd
import requests
import time
import re

# ✅ 替换成你的 Google Maps API Key
API_KEY = 'AIzaSyCY9XjhoehieRMx6tt18UH2qIUFJfcxJII'

# 清理括号内容与无用说明文字
def clean_address(address):
    address = re.sub(r"\(.*?\)", "", address)
    address = re.sub(r"(?i)pick[- ]?up", "", address)
    return address.strip()

# 判断是否在香港地理范围
def is_valid_hk_location(lat, lon):
    return 22 <= lat <= 23 and 113.8 <= lon <= 114.4

# 读取 CSV 文件
df = pd.read_csv("PublicO2oStore.csv")

latitudes = []
longitudes = []
failed_addresses = []

for i, row in df.iterrows():
    shop_name = row['o2o_shop_name']
    address = row['address_en']

    # 改进版地址组合：商店名 + 地址 + Hong Kong
    full_query = f"{shop_name}, {clean_address(address)}, Hong Kong"

    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {'address': full_query, 'key': API_KEY}
        response = requests.get(url, params=params)
        result = response.json()

        if result['status'] == 'OK':
            location = result['results'][0]['geometry']['location']
            lat = location['lat']
            lon = location['lng']
            latitudes.append(lat)
            longitudes.append(lon)

            if not is_valid_hk_location(lat, lon):
                print(f"⚠️ Suspicious: {full_query} → ({lat}, {lon})")
        else:
            latitudes.append(None)
            longitudes.append(None)
            failed_addresses.append(full_query)
            print(f"❌ Failed: {full_query} - Status: {result['status']}")

        time.sleep(0.1)

    except Exception as e:
        latitudes.append(None)
        longitudes.append(None)
        failed_addresses.append(full_query)
        print(f"⚠️ Error: {full_query} - {e}")

# 添加经纬度与有效性列
df['latitude'] = latitudes
df['longitude'] = longitudes
df['valid_location'] = df.apply(
    lambda row: is_valid_hk_location(row['latitude'], row['longitude']) if pd.notnull(row['latitude']) else False,
    axis=1
)

# 输出正常数据
valid_df = df[df['valid_location'] == True]
valid_df.to_csv("PublicO2oStore_cleaned.csv", index=False)
print("✅ 已保存正确地址：PublicO2oStore_cleaned.csv")

# 输出异常数据
invalid_df = df[df['valid_location'] == False]
invalid_df.to_csv("PublicO2oStore_invalid_coords.csv", index=False)
print("⚠️ 已保存异常地址：PublicO2oStore_invalid_coords.csv")