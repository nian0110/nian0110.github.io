import os
import shutil
import random
import pandas as pd
import argparse

def clear_directory(directory):
    """ 清空指定的資料夾 """
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_all_images(directory):
    """ 獲取指定資料夾中所有圖片的完整路徑 """
    image_extensions = {'.JPG', '.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_paths.append(os.path.join(root, file))
    return image_paths

def copy_random_images(src_folder, dest_folder, num_images):
    """ 隨機挑選圖片並複製到目的資料夾 """
    all_images = get_all_images(src_folder)
    selected_images = random.sample(all_images, min(num_images, len(all_images)))
    
    clear_directory(dest_folder)
    
    for image_path in selected_images:
        shutil.copy(image_path, dest_folder)
    
    return [os.path.basename(img) for img in selected_images]

def main():
    parser = argparse.ArgumentParser(description='隨機挑選圖片並複製到指定資料夾')
    parser.add_argument('num_images', type=int, help='要隨機挑選的圖片數量')
    args = parser.parse_args()
    
    src_folder = '../..//download_lingorm/photo_activity'
    dest_folder = './images'
    output_file = './images.csv'
    num_images = args.num_images
    
    # 確保目的資料夾存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # 複製隨機挑選的圖片
    copied_files = copy_random_images(src_folder, dest_folder, num_images)
    
    # 將檔案名稱寫入 CSV
    df = pd.DataFrame(copied_files, columns=['filename'])
    df['filename'] = df['filename'].apply(lambda x: os.path.join(dest_folder, x))
    df.to_csv(output_file, index=False, header=False)
    
    print(f"隨機挑選了 {df.shape[0]} 張圖片，並已存入 {dest_folder} 和 {output_file}")

if __name__ == "__main__":
    main()
