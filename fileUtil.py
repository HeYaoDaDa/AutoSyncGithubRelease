import os


def listdir(path):
    fileNames = os.listdir(path)
    result = []
    for fileName in fileNames:
        result.append(os.path.join(path, fileName))
    return result
