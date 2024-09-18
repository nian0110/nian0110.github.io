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

def get_all_images(directory, image_extensions):
    """ 獲取指定資料夾中所有圖片的完整路徑 """
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_paths.append(os.path.join(root, file))
    return image_paths

def copy_images(src_folder, dest_folder, num_images):
    """ 複製指定數量的圖片到目的資料夾，若 num_images 為 'all' 則複製所有圖片 """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    all_images = get_all_images(src_folder, image_extensions)
    
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

def clean_unwanted_webp_files(dest_org_folder, dest_folder):
    """ 檢查 dest_folder 中的 WebP 檔案，如果它們不存在於 dest_org_folder，則刪除 """
    webp_files = {os.path.splitext(file)[0] for file in os.listdir(dest_folder) if file.endswith('.webp')}
    jpg_files = {os.path.splitext(file)[0] for file in os.listdir(dest_org_folder) if file.endswith('.jpg') or file.endswith('.jpeg')}
    
    # 找出在 dest_folder 中存在，但在 dest_org_folder 中不存在的 WebP 文件
    unwanted_files = [file for file in os.listdir(dest_folder) 
                      if file.endswith('.webp') and os.path.splitext(file)[0] not in jpg_files]
    
    # 刪除這些不需要的 WebP 文件
    deleted_count = 0
    for file in unwanted_files:
        os.remove(os.path.join(dest_folder, file))
        deleted_count += 1
        # print(f"刪除檔案: {file}")

    print(f"\n從{dest_folder}，總共刪除了 {deleted_count} 個檔案")

def main():
    parser = argparse.ArgumentParser(description='隨機挑選圖片並複製到指定資料夾')
    parser.add_argument('num_images', type=str, help='要隨機挑選的圖片數量，或指定為 \'all\' 以複製所有圖片')
    args = parser.parse_args()
    
    # 從環境變數中讀取資料夾路徑
    src_folder = os.getenv('SRC_FOLDER')
    dest_org_folder = os.getenv('DEST_ORG_FOLDER')
    dest_folder = os.getenv('DEST_FOLDER')

    print(f'src_folder: {src_folder}')
    print(f'dest_org_folder: {dest_org_folder}')
    print(f'dest_folder: {dest_folder}\n')

    num_images = args.num_images

    # 確保目的資料夾存在
    if not os.path.exists(dest_org_folder):
        os.makedirs(dest_org_folder)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # 複製圖片
    copied_files = copy_images(src_folder, dest_org_folder, num_images)
    print(f"已複製 {len(copied_files)} 張圖片，存入 {dest_org_folder}\n")

    # 檢查並刪除不需要的 WebP 檔案
    clean_unwanted_webp_files(dest_org_folder, dest_folder)

if __name__ == "__main__":
    main()
