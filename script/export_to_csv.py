import os
import pandas as pd
import argparse
from dotenv import load_dotenv

# 加載 .env 文件
load_dotenv()

def str_to_bool(v):
    if v.lower() in ('true', 't', '1'):
        return True
    elif v.lower() in ('false', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def find_jpg_files(root_folder):
    file_list = []

    # 遍历目录
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.webp'):
                full_path = os.path.join(dirpath, filename)
                file_list.append({'filename': filename, 'full_path': full_path})

    # 转换为 DataFrame
    df = pd.DataFrame(file_list, columns=['filename', 'full_path'])
    df['full_path'] = df['full_path'].apply(lambda x: x.replace('\\', '/'))
    duplicated_count = df[df.duplicated(subset=['filename'])].shape[0]
    print(f'dup count：{df.shape[0]} - {duplicated_count} = {df.shape[0]-duplicated_count}')
    df = df.drop_duplicates('filename').reset_index(drop=True)
    print(f'df count：{df.shape[0]}')

    return df

def merge_notion_df(df):
    notion_df = pd.read_excel('photo_data_notion.xlsx')
    notion_df = notion_df.rename(columns={'children_path':'activity', 'month_path':'month'})
    notion_df['lingorm'] = notion_df['relative_path'].apply(lambda x: x.split('/')[-1])
    notion_df = notion_df[['filename', 'username', 'root_path', 'activity', 'month', 'lingorm']]

    df['filename'] = df['filename'].apply(lambda x: os.path.splitext(x)[0])
    df = df.rename(columns={'filename':'base_filename'})
    notion_df['base_filename'] = notion_df['filename'].apply(lambda x: os.path.splitext(x)[0])

    # 合并数据框
    merged_df = pd.merge(df, notion_df, on='base_filename', how='inner')

    # 删除临时列
    merged_df = merged_df.drop(columns=['base_filename'])
    merged_df['filename'] = merged_df['full_path'].apply(lambda x:x.split('/')[-1])
    merged_df = merged_df[['filename', 'full_path', 'username', 'root_path', 'activity', 'month', 'lingorm']]

    return merged_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='指定是否合併其他欄位')
    parser.add_argument('merge', type=str_to_bool, help='True/False')
    parser.add_argument('csv_img_folder', type=str, help='csv_img_folder')
    parser.add_argument('csv_filename', type=str, help='csv_filename')
    
    args = parser.parse_args()
    merge = args.merge
    csv_img_folder = args.csv_img_folder
    csv_filename = args.csv_filename
    print(f'merge: {merge}')
    print(f'csv_img_folder: {csv_img_folder}')
    print(f'csv_filename: {csv_filename}\n')
    
    # 獲取目的資料夾中的所有檔案
    tmp_df = find_jpg_files(csv_img_folder)
    if merge:
        df = merge_notion_df(tmp_df)
    else:
        df = tmp_df

    df.to_csv(csv_filename, index=False)
    
    print(f"已將 {tmp_df.shape[0]} 個檔案匯出到 {csv_filename}")