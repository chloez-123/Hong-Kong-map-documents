#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 22:05:53 2025

@author: chloezhao
"""

import pandas as pd

# 载入资料
df = pd.read_csv("/Users/chloezhao/Desktop/Hong Kong map documents./PublicO2OStore_with_district.csv")


# 建立英文 → 中文对照字典
district_dict = {
    "Central and Western District": "中西区",
    "Wan Chai District": "湾仔区",
    "Eastern District": "东区",
    "Southern District": "南区",
    "Yau Tsim Mong District": "油尖旺区",
    "Sham Shui Po District": "深水埗区",
    "Kowloon City District": "九龙城区",
    "Wong Tai Sin District": "黄大仙区",
    "Kwun Tong District": "观塘区",
    "Kwai Tsing District": "葵青区",
    "Tsuen Wan District": "荃湾区",
    "Tuen Mun District": "屯门区",
    "Yuen Long District": "元朗区",
    "North District": "北区",
    "Tai Po District": "大埔区",
    "Sha Tin District": "沙田区",
    "Sai Kung District": "西贡区",
    "Islands District": "离岛区"
}

# 新增 District_18_CH 中文栏位
df["District_18_CH"] = df["District_18"].map(district_dict)

# 储存成新文件
# 原本 CSV 写法（会乱码）
# df.to_csv("PublicO2OStore_with_district_bilingual.csv", index=False)

# ✅ 改成 Excel 写法（不会乱码）
df.to_excel("PublicO2OStore_with_district_bilingual.xlsx", index=False)


print("✅ 已成功加入 District_18_CH 中文字段并输出为 PublicO2OStore_with_district_bilingual.xlsx")
