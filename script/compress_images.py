import os
from PIL import Image
import argparse
from tqdm import tqdm
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import threading

# 加載 .env 文件
load_dotenv()

print_lock = threading.Lock()

def resize_and_compress_image(image_path, img_tmp_folder, dest_folder, max_size_kb=300, max_width=800, max_height=1200):
    """ 
    先縮小圖片尺寸，然後如果大小超過 max_size_kb 則進行壓縮
    
    參數:
    - image_path: 原始圖片路徑
    - img_tmp_folder: 臨時圖片資料夾
    - dest_folder: 目標輸出資料夾
    - max_size_kb: 最大檔案大小（KB）
    - max_width: 圖片最大寬度
    - max_height: 圖片最大高度
    """
    # 生成 WebP 檔案路徑
    relative_path = os.path.relpath(image_path, img_tmp_folder)
    webp_image_path = os.path.join(dest_folder, os.path.splitext(relative_path)[0] + '.webp')
    
    # 確保目標目錄存在
    os.makedirs(os.path.dirname(webp_image_path), exist_ok=True)
    
    # 如果已經有符合條件的 WebP 文件，則跳過
    if os.path.exists(webp_image_path):
        file_size_kb = os.path.getsize(webp_image_path) / 1024
        if file_size_kb <= max_size_kb:
            with print_lock:
                print(f"檔案 {webp_image_path} 已經存在且大小小於 {max_size_kb} KB，跳過")
            return webp_image_path

    with print_lock:
        print(f"開始處理檔案: {image_path}")
    
    # 開啟並轉換圖片
    img = Image.open(image_path)
    img = img.convert("RGB")  # 處理透明度

    # 第一步：縮小圖片尺寸
    img.thumbnail((max_width, max_height), Image.LANCZOS)
    
    # 先以預設高品質儲存
    img.save(webp_image_path, "WEBP", quality=90, optimize=True)
    
    # 檢查檔案大小
    file_size_kb = os.path.getsize(webp_image_path) / 1024
    
    with print_lock:
        print(f"縮小尺寸後大小: {file_size_kb:.2f} KB")

    # 第二步：如果檔案大小仍然超過 max_size_kb，則進行壓縮
    if file_size_kb > max_size_kb:
        quality = 90
        while file_size_kb > max_size_kb and quality > 10:
            quality -= 10
            img.save(webp_image_path, "WEBP", quality=quality, optimize=True)
            file_size_kb = os.path.getsize(webp_image_path) / 1024
            
            with print_lock:
                print(f"壓縮中 - 品質: {quality}, 檔案大小: {file_size_kb:.2f} KB")

    with print_lock:
        print(f"完成處理: {webp_image_path}, 最終大小: {file_size_kb:.2f} KB\n")
    
    return webp_image_path

def get_all_images(directory):
    """ 遞迴獲取指定目錄下的所有圖片 """
    img_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', 'webp')):
                full_path = os.path.join(root, file)
                img_files.append(full_path)
    return img_files

def compress_all_images(img_tmp_folder, img_folder, max_size_kb, max_width=800, max_height=1200):
    """ 
    壓縮來源資料夾中的所有圖片，直到每張圖片大小小於 max_size_kb 
    """
    image_paths = get_all_images(img_tmp_folder)
    compressed_images = []

    # 使用 ThreadPoolExecutor 並行處理圖片
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                resize_and_compress_image, 
                image_path, 
                img_tmp_folder, 
                img_folder, 
                max_size_kb, 
                max_width, 
                max_height
            ) for image_path in image_paths
        ]
        
        for future in tqdm(futures, desc="處理圖片中"):
            compressed_images.append(future.result())

    return [os.path.basename(img) for img in compressed_images]

def main():
    parser = argparse.ArgumentParser(description='壓縮指定資料夾中的圖片至指定大小')
    parser.add_argument('max_size_kb', type=int, help='壓縮圖片的最大大小（KB）')
    parser.add_argument('img_tmp_folder', type=str, help='原始圖片資料夾')
    parser.add_argument('img_folder', type=str, help='輸出圖片資料夾')
    parser.add_argument('--max_width', type=int, default=800, help='圖片最大寬度（預設 800）')
    parser.add_argument('--max_height', type=int, default=1200, help='圖片最大高度（預設 1200）')

    args = parser.parse_args()
    
    print(f'max_size_kb: {args.max_size_kb}')
    print(f'img_tmp_folder: {args.img_tmp_folder}')
    print(f'img_folder: {args.img_folder}')
    print(f'max_width: {args.max_width}')
    print(f'max_height: {args.max_height}\n')

    # 確保目的資料夾存在
    os.makedirs(args.img_folder, exist_ok=True)
    
    # 壓縮圖片
    compressed_files = compress_all_images(
        args.img_tmp_folder, 
        args.img_folder, 
        args.max_size_kb, 
        args.max_width, 
        args.max_height
    )

    print(f"已處理 {len(compressed_files)} 張圖片，結果存儲於 {args.img_folder}")

if __name__ == "__main__":
    main()