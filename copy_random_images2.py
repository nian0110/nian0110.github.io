import os
import shutil
import argparse
from tqdm import tqdm
from dotenv import load_dotenv
import pandas as pd

# 加載 .env 文件
load_dotenv()

def copy_images(df, img_tmp_folder, img_folder):

    df['filename_webp'] = df['filename'].str.replace('.JPG', '.webp', case=False)

    img_files = []
    for root, dirs, files in os.walk(img_folder):
        img_files.extend(files)

    df['exists_in_images'] = df['filename_webp'].apply(lambda x: x in img_files)

    selected_images = list(df[~df['exists_in_images']]['full_path'])

    for image_path in tqdm(selected_images, desc="複製圖片", unit="張"):
        shutil.copy(image_path, img_tmp_folder)

    return selected_images

def main():
    parser = argparse.ArgumentParser(description='隨機挑選圖片並複製到指定資料夾')
    parser.add_argument('num_images', type=str, help='要隨機挑選的圖片數量，或指定為 \'all\' 以複製所有圖片')
    args = parser.parse_args()
    
    img_tmp_folder = os.getenv('IMG_TMP_FOLDER')
    img_folder = os.getenv('IMG_FOLDER')

    print(f'img_tmp_folder: {img_tmp_folder}')
    print(f'img_folder: {img_folder}\n')

    num_images = args.num_images
    df = pd.read_excel('photo_data_notion.xlsx')

    # 確保目的資料夾存在
    for folder in [img_tmp_folder, img_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    # 複製圖片
    copied_files = copy_images(df, img_tmp_folder, img_folder)
    print(f"已複製 {len(copied_files)} 張圖片，存入 {img_tmp_folder}\n")

if __name__ == "__main__":
    main()
