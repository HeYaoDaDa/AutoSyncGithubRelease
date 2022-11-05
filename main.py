from util import *
from constant import download_dir
from multiprocessing import Pool

if __name__ == '__main__':
    releases_json = get_releases_json(
        "https://api.github.com/repos/CleverRaven/Cataclysm-DDA/releases?per_page=30")
    exist_files = get_path_files(download_dir)
    down_urls, remove_files = get_all_need_download_game_file_dirt(
        releases_json, exist_files)
    print(f"down size is {len(down_urls)}")
    pool = Pool(5)
    for i in down_urls:
        pool.apply_async(download_game_file, args=(i,))
    pool.close()
    pool.join()
    print(f"rm dir size is {len(remove_files)}")
    for dir in remove_files:
        print(f"start remove dir {dir}")
        rm_dir(remove_files)
    print("======>Finish<======")
