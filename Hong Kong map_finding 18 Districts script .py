#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 12 21:50:17 2025

@author: chloezhao
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import fiona

# 📍 设置路径
folder_path = "/Users/chloezhao/Desktop/Hong Kong map documents./"
geojson_path = folder_path + "HK18Districts.geojson"
store_csv = folder_path + "PublicO2OStore_cleaned.csv"

# ➊ 读取店铺 CSV 并转为 GeoDataFrame（记得经纬度）
df = pd.read_csv(store_csv)
df = df.dropna(subset=["latitude", "longitude"])

gdf_points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
    crs="EPSG:4326"  # 原始 GPS WGS84
)

# ➋ 读取香港18区 GeoJSON
with fiona.open(geojson_path) as src:
    records = list(src)

gdf_districts = gpd.GeoDataFrame.from_features(records)
gdf_districts.set_crs(epsg=2326, inplace=True)

# ➌ 坐标转换：WGS84 → EPSG:2326（与18区一致）
gdf_points = gdf_points.to_crs(epsg=2326)

# ➍ 判断包含关系（spatial join）
district_col = "NAME_EN" if "NAME_EN" in gdf_districts.columns else gdf_districts.columns[-1]
gdf_districts = gdf_districts[[district_col, "geometry"]]

merged = gpd.sjoin(gdf_points, gdf_districts, how="left", predicate="within")

# ➎ 改名 + 保存
merged = merged.rename(columns={district_col: "District_18"})
merged.drop(columns="geometry").to_csv(folder_path + "PublicO2OStore_with_district.csv", index=False)

print("✅ 成功输出：PublicO2OStore_with_district.csv，包含 District_18 字段")

