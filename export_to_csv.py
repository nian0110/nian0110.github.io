import os
import pandas as pd

def get_all_files(directory):
    """ 獲取指定資料夾中所有檔案的完整路徑 """
    return [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

if __name__ == "__main__":
    dest_folder = './images'
    output_file = './images.csv'
    
    # 獲取目的資料夾中的所有檔案
    all_files = get_all_files(dest_folder)
    
    # 將檔案名稱寫入 CSV
    df = pd.DataFrame(all_files, columns=['filename'])
    df.to_csv(output_file, index=False, header=False)
    
    print(f"已將 {len(all_files)} 個檔案匯出到 {output_file}")
