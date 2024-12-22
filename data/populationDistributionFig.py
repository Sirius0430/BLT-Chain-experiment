import rasterio
import numpy as np

# 打开 TIFF 文件
with rasterio.open(r'ppp_2020_1km_Aggregated.tif') as src:
    # 读取图像数据到一个 numpy 数组
    data = src.read(1)  # 假设读取的是第一波段

# 将负值设为 0，因为负值不参与计算
# data[data < 0] = 0

# 选择所有大于等于 250 的像素
threshold = 500
greater_equal_250 = data[data >= threshold]
sum_greater_equal_250 = np.sum(greater_equal_250)

# 选择所有小于 250 的像素
less_250 = data[(data >= 0) & (data < threshold)]
sum_less_250 = np.sum(less_250)

# 打印结果
print("大于等于", threshold, "的像素总和:", sum_greater_equal_250)
print("小于", threshold, "的像素总和:", sum_less_250)
print(np.round(sum_greater_equal_250/(sum_greater_equal_250+sum_less_250),4))
