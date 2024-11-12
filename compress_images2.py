import os
from PIL import Image
import argparse
from tqdm import tqdm  # 進度條顯示
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import threading

# 加載 .env 文件
load_dotenv()

print_lock = threading.Lock()

def compress_image(image_path, dest_folder, max_size_kb, target_quality=90):
    """ 反覆壓縮圖片直到大小小於 max_size_kb """
    base_name = os.path.basename(image_path)
    webp_image_path = os.path.join(dest_folder, base_name.replace('.jpg', '.webp'))
    
    # 如果已經有符合條件的 WebP 文件，則跳過
    if os.path.exists(webp_image_path):
        file_size_kb = os.path.getsize(webp_image_path) / 1024
        if file_size_kb <= max_size_kb:
            print(f"檔案 {webp_image_path} 已經存在且大小小於 {max_size_kb} KB，跳過")
            return webp_image_path

    print(f"開始壓縮檔案: {image_path}")
    file_size_init = os.path.getsize(image_path) / 1024

    img = Image.open(image_path)
    img = img.convert("RGB")  # 若圖片有透明度（如PNG），轉換為RGB

    quality = target_quality
    while True:
        img.save(webp_image_path, "WEBP", quality=quality, optimize=True)
        file_size_kb = os.path.getsize(webp_image_path) / 1024
        with print_lock:
            print(f"檔案原始大小：{file_size_init:.2f} KB, 壓縮後大小: {file_size_kb:.2f} KB, 品質: {quality}")

        if file_size_kb <= max_size_kb or quality <= 10:
            break

        quality -= 10  # 每次降低品質10

    with print_lock:
        print(f"完成壓縮: {webp_image_path}\n")
    
    return webp_image_path

def get_all_images(directory):
    img_files = []
    for root, dirs, files in os.walk(directory):
        img_files.extend(files)
    return img_files

def compress_all_images(img_tmp_folder, img_folder, max_size_kb):
    """ 壓縮來源資料夾中的所有圖片，直到每張圖片大小小於 max_size_kb """
    image_paths = get_all_images(img_tmp_folder)
    compressed_images = []

    # 使用 ThreadPoolExecutor 並行處理圖片
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(compress_image, image_path, img_tmp_folder, max_size_kb) for image_path in image_paths]
        for future in tqdm(futures, desc="壓縮圖片中"):
            compressed_images.append(future.result())

    return [os.path.basename(img) for img in compressed_images]

def main():
    parser = argparse.ArgumentParser(description='壓縮指定資料夾中的圖片至指定大小')
    parser.add_argument('max_size_kb', type=int, help='壓縮圖片的最大大小（KB）')
    args = parser.parse_args()
    
    img_tmp_folder = os.getenv('IMG_TMP_FOLDER')
    img_folder = os.getenv('IMG_FOLDER')

    print(f'img_tmp_folder: {img_tmp_folder}')
    print(f'img_folder: {img_folder}\n')

    max_size_kb = args.max_size_kb

    # 確保目的資料夾存在
    for folder in [img_tmp_folder, img_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    # 壓縮圖片
    compressed_files = compress_all_images(img_tmp_folder, img_folder, max_size_kb)

    print(f"已壓縮 {len(compressed_files)} 張圖片，結果存儲於 {dest_folder}")

if __name__ == "__main__":
    main()
