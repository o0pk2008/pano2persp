import cv2
import numpy as np
from PIL import Image
import py360convert
import os

def process_panorama(input_path, output_dir):
    # 读取全景图
    pano = cv2.imread(input_path)
    if pano is None:
        print(f"无法读取全景图像: {input_path}")
        return
    
    # 获取输入文件名（不含扩展名）作为前缀
    input_name = os.path.splitext(os.path.basename(input_path))[0]
    
    # 使用py360convert的e2c方法直接转换
    cube_h = py360convert.e2c(pano, face_w=1024)
    
    # 转换为字典格式，每个面单独存储
    cube_dict = py360convert.cube_h2dict(cube_h)
    
    # 保存每个面，对B和R面进行特殊处理
    for face_name, face_img in cube_dict.items():
        # 对B和R面进行水平翻转以修正镜像问题
        if face_name in ['B', 'R']:
            face_img = cv2.flip(face_img, 1)
            
        output_path = os.path.join(output_dir, f'{input_name}_cube_{face_name}.jpg')
        cv2.imwrite(output_path, face_img)
        print(f'已保存 {output_path}')

if __name__ == '__main__':
    input_dir = 'E:/PPT/20250326/insta360/04_grassland/input'  # 输入全景图目录
    output_dir = 'E:/PPT/20250326/insta360/04_grassland/output'  # 输出立方体贴图目录
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录中的所有图像文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            process_panorama(input_path, output_dir)