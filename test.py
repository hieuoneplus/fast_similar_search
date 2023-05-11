import os

# Đường dẫn đến thư mục
folder_path = 'C:/Users/nshd1/OneDrive/Documents/code/fast_similar_search/static/image'

file_list = os.listdir(folder_path)

# Duyệt từng tệp bằng index
for i in range(len(file_list)):
    file_path = os.path.join(folder_path, file_list[i])
    if os.path.isfile(file_path):
        print(f"Tệp số {i}: {file_list[i]}")