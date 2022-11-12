import os
import requests
from constant import download_dir, github_token


def rm_dir(dir: str):
    files = os.listdir(dir)
    result = []
    for file in files:
        if os.path.isdir(file):
            rm_dir(file)
        else:
            os.remove(file)
    os.removedirs(dir)


def get_path_files(path: str) -> list[str]:
    if os.path.exists(path):
        files = os.listdir(path)
        result = []
        for file in files:
            if os.path.isdir(file):
                result.append(get_path_files(file))
            else:
                result.append(file)
        return files
    else:
        return []


def get_all_need_download_game_file_dirt(release_jsons, exist_game_files: list[str]) -> list:
    asset_tuple_list = []
    release_jsons = sorted(
        release_jsons, key=lambda release: release["published_at"]
    )
    for release_json in release_jsons:
        assets = release_json["assets"]
        version = release_json["tag_name"]
        prerelease = bool(release_json["prerelease"])
        for asset in assets:
            url = asset["browser_download_url"]
            name = asset["name"]
            size = int(asset["size"])/1024/1024
            if is_need_upload(name, size) and name not in exist_game_files:
                asset_tuple_list.append(url)
    remove_files = set()
    for exist_file in exist_game_files:
        if exist_file not in release_jsons:
            remove_files.add(os.path.pardir(exist_file))
    return asset_tuple_list, remove_files


def is_need_upload(filename: str, size: int):
    if filename.endswith('.zip') or filename.endswith('.apk'):
        return True
    else:
        return False


def download_game_file(url: str, size: int = 0):
    if size >= 5:
        print(f"download has reply 5, url is {url}")
        return None
    splits = url.split("/")
    filename = splits[-1]
    version = splits[-2]
    targetDir = os.path.join(download_dir, version)
    targetFile = os.path.join(targetDir, filename)
    if os.path.exists(targetFile):
        return
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    print("start download " + filename)
    r = requests.get(url)
    with open(targetFile, 'wb') as f:
        f.write(r.content)
    if not os.path.exists(targetFile):
        print(f"download is not exists")
        targetFile = download_game_file(url, size+1)
    else:
        filesize = os.path.getsize(targetFile)/1024/1024
        if filesize < 30:
            print(f"download size is wrong, size is {filesize}")
            targetFile = download_game_file(url, size+1)
    return targetFile


def get_releases_json(release_url: str) -> list[object]:
    return requests.get(release_url, headers=github_token).json()
