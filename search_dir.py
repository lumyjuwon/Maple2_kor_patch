import os

class search_dir:
    def check_disk(self):
        using_disk = []
        uppercase = ['A:', 'B:', 'C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:',
                     'Q:',
                     'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
        for i in uppercase:
            if os.path.exists(i):
                using_disk.append(i)
        return using_disk

    def search_steamlibrary(self):
        using_disk = search_dir.check_disk(self)
        for disk in using_disk:
            if os.path.exists(disk + "\\SteamLibrary\\steamapps\\common\\MapleStory 2\\"):
                directory = disk + "\\SteamLibrary\\steamapps\\common\\MapleStory 2\\"
                return directory
        return "C:\\"

if __name__ == "__main__":
    print("run")