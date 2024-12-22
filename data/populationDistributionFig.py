import rasterio
import numpy as np

# 打开 TIFF 文件
with rasterio.open(r'ppp_2020_1km_Aggregated.tif') as src:
    data = src.read(1)

threshold = 500
greater_equal_250 = data[data >= threshold]
sum_greater_equal_250 = np.sum(greater_equal_250)

less_250 = data[(data >= 0) & (data < threshold)]
sum_less_250 = np.sum(less_250)

# 打印结果
print("sum of pixels values more than", threshold, ":", sum_greater_equal_250)
print("sum of pixels values more than", threshold, ":", sum_less_250)
print(np.round(sum_greater_equal_250/(sum_greater_equal_250+sum_less_250),4))
