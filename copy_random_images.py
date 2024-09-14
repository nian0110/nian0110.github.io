import os
import random
import shutil
import argparse
from tqdm import tqdm
from dotenv import load_dotenv

# 加載 .env 文件
load_dotenv()

def clear_directory(directory):
    """ 清空指定的資料夾 """
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_all_images(directory):
    """ 獲取指定資料夾中所有圖片的完整路徑 """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_paths.append(os.path.join(root, file))
    return image_paths

def copy_images(src_folder, dest_folder, num_images):
    """ 複製指定數量的圖片到目的資料夾，若 num_images 為 'all' 則複製所有圖片 """
    all_images = get_all_images(src_folder)
    
    if num_images == 'all':
        selected_images = all_images
    else:
        num_images = int(num_images)
        selected_images = random.sample(all_images, min(num_images, len(all_images)))
    
    clear_directory(dest_folder)
    
    # 使用 tqdm 進度條顯示複製進度
    for image_path in tqdm(selected_images, desc="複製圖片", unit="張"):
        shutil.copy(image_path, dest_folder)
    
    return [os.path.basename(img) for img in selected_images]

def main():
    parser = argparse.ArgumentParser(description='隨機挑選圖片並複製到指定資料夾')
    parser.add_argument('num_images', type=str, help='要隨機挑選的圖片數量，或指定為 \'all\' 以複製所有圖片')
    args = parser.parse_args()
    
    # 從環境變數中讀取資料夾路徑
    src_folder = os.getenv('SRC_FOLDER')
    dest_folder = os.getenv('COPY_DEST_FOLDER')
    num_images = args.num_images

    # 確保目的資料夾存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # 複製圖片
    copied_files = copy_images(src_folder, dest_folder, num_images)
    
    print(f"已複製 {len(copied_files)} 張圖片，存入 {dest_folder}")

if __name__ == "__main__":
    main()
