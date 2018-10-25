from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from urllib.request import Request
from functools import partial
import webbrowser
import urllib.request
import sys
import search_dir
import crawling
import zipfile
import os
import time


class PatchTread(QThread):
    change_value = pyqtSignal(int)
    change_message = pyqtSignal(str)
    change_visible = pyqtSignal(bool)

    def __init__(self, directory, progress, kor_patch_checkBox, kor_sound_patch_checkBox, option_url, kor_patch_url, kor_sound_patch_url):
        QThread.__init__(self)
        self.setup_directory = directory + "Data\\"
        self.progress = progress
        self.progress2 = 0
        self.kor_patch = kor_patch_checkBox
        self.kor_sound_patch = kor_sound_patch_checkBox
        self.option_url = option_url
        self.kor_patch_url = kor_patch_url
        self.kor_sound_patch_url = kor_sound_patch_url

    def __del__(self):
        self.wait()

    def run(self):
        print("Setup_directory: " + self.setup_directory)
        print("option_url: " + self.option_url)
        print("kor_patch_url: " + self.kor_patch_url)
        print("kor_sound_patch_url: " + self.kor_sound_patch_url)
        self.change_visible.emit(False)
        self.download()
        self.change_visible.emit(True)

    def download(self):
        if os.path.exists(self.setup_directory):
            if self.kor_patch.isChecked() and self.kor_sound_patch.isChecked():
                self.change_message.emit('파일 다운로드 중 ...')
                urllib.request.urlretrieve(self.kor_patch_url, self.setup_directory + "kor_patch.zip",
                                           reporthook=self.dlProgress)
                self.patch_process(self.setup_directory)
                self.change_message.emit('파일 다운로드 중 ...')
                urllib.request.urlretrieve(self.kor_sound_patch_url, self.setup_directory + "kor_patch.zip",
                                           reporthook=self.dlProgress)
                self.patch_process(self.setup_directory)

                self.progress = 100
                self.change_value.emit(self.progress)
            elif self.kor_patch.isChecked():
                self.change_message.emit('파일 다운로드 중 ...')
                urllib.request.urlretrieve(self.kor_patch_url, self.setup_directory + "kor_patch.zip",
                                           reporthook=self.dlProgress)
                self.patch_process(self.setup_directory)

                self.progress = 100
                self.change_value.emit(self.progress)
            elif self.kor_sound_patch.isChecked():
                self.change_message.emit('파일 다운로드 중 ...')
                urllib.request.urlretrieve(self.kor_sound_patch_url, self.setup_directory + "kor_patch.zip",
                                           reporthook=self.dlProgress)
                self.patch_process(self.setup_directory)

                self.progress = 100
                self.change_value.emit(self.progress)
        else:
            self.change_message.emit("Data 폴더를 찾을 수 없습니다.")

    def dlProgress(self, count, blockSize, totalSize):
        # 다운로드 header 파일이 없을 경우 임의로 totalSize를 정해줌

        if self.kor_patch.isChecked() and self.kor_sound_patch.isChecked():
            # print(totalSize)
            if totalSize >= 300000000:
                percent = abs(int(count * blockSize * 100 / totalSize) / 2.4) + 42
            else:
                percent = abs(int(count * blockSize * 100 / totalSize) / 2.4)
        else:
            percent = abs(int(count * blockSize * 100 / totalSize) / 1.2)
        # print(count, blockSize, totalSize, count * blockSize)
        while self.progress <= percent:
            self.progress += 1
            print("progress: ", self.progress)
            self.change_value.emit(self.progress)


    def patch_process(self, directory_):
        print("patch_process")
        try:
            self.change_message.emit('파일 압축푸는 중 ...')
            zipfile.ZipFile(directory_+"kor_patch.zip").extractall(directory_)
            os.remove(directory_ + "kor_patch.zip")

            self.change_message.emit('패치 완료 !')
        except:
            self.change_message.emit('패치 에러')
            return -1


form_class = uic.loadUiType("maplestory2.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('icon.png'))
        self.version = "1.0"
        self.kor_patch_url = "https://www.dropbox.com/s/scepv8sk3dd27er/Xml.zip?dl=1"
        self.kor_sound_patch_url = "https://www.dropbox.com/s/igfcrtkqcphivlb/Kor_sound2.zip?dl=1"
        self.option_url = "https://drive.google.com/uc?authuser=0&id=14WlWEWAI-wyEQ3TEBqw13H-GJaPKlOTx&export=download"
        self.update_url = "https://drive.google.com/uc?authuser=0&id=1zzbO3PMyUyq1nk_KuBTJrH86992LSUQi&export=download"
        self.site_url = "https://hyrama.com/?p=598"
        self.github_url = "https://github.com/lumyjuwon/MapleStory2_kor_patch"
        self.check_Update()

        self.setupUi(self)
        self.setWindowTitle("MapleStory2 Korean Patch")

        self.progress = 0
        # self.th = threading.Thread(target=self.download)

        self.update_status_label.setFocus(True)

        self.patch_button.clicked.connect(self.patch)
        self.actionSite.triggered.connect(partial(self.open_url, self.site_url))
        self.actionGithub.triggered.connect(partial(self.open_url, self.github_url))

        self.update_status_label.setText(crawling.Crawling().parser_day())
        self.update_status_label.setStyleSheet('color: green')

        self.dir_edit.setText(self.load_directory())

        self.find_dir_button.clicked.connect(self.directory_dialog)
        self.close()

    def directory_dialog(self):
        select_dialog = QFileDialog.getExistingDirectory(self, 'Directory', 'c:\\')
        print(select_dialog)
        try:
            self.save_dir(select_dialog)
        except:
            pass

    def load_directory(self):
        try:
            file = open('directory.txt', 'r')
            directory = file.readlines()[0]
            return directory
        except:
            default_directory = search_dir.search_dir().search_steamlibrary()
            return default_directory

    def save_dir(self, dialog):
        dir_edit_text = dialog
        if dir_edit_text[-1] != "\\":
            dir_edit_text += "\\"
        if dir_edit_text:
            file = open('directory.txt', 'w')
            file.writelines(dir_edit_text)
            file.close()
            self.dir_edit.setText(dir_edit_text)

    def patch(self):
        self.progress = 0
        self.progressBar.setValue(self.progress)
        self.get_thread = PatchTread(self.load_directory(), self.progress, self.kor_patch_checkBox,
                                     self.kor_sound_patch_checkBox, self.option_url, self.kor_patch_url, self.kor_sound_patch_url)
        self.save_dir(self.dir_edit.text())

        if os.path.exists(self.load_directory()):

            if self.kor_patch_checkBox.isChecked() or self.kor_sound_patch_checkBox.isChecked():
                # self.connect(self.get_thread, SIGNAL("finished()"), self.done)
                if (self.load_directory().find("MapleStory 2") == -1):
                    QMessageBox.about(self, "Error", "MapleStory 2 경로가 아닙니다")
                else:
                    self.get_thread.change_value.connect(self.progressBar.setValue)
                    self.get_thread.change_message.connect(self.statusbar.showMessage)
                    self.get_thread.change_visible.connect(self.patch_button.setEnabled)
                    self.get_thread.change_visible.connect(self.find_dir_button.setEnabled)
                    self.get_thread.change_visible.connect(self.dir_edit.setEnabled)
                    self.get_thread.change_visible.connect(self.kor_patch_checkBox.setEnabled)
                    self.get_thread.change_visible.connect(self.kor_sound_patch_checkBox.setEnabled)
                    self.get_thread.start()
            else:
                QMessageBox.about(self, "Error", "한글패치 또는 한글 음성패치를 선택하세요")

        else:
            QMessageBox.about(self, "Error", "이 경로에는 설치할 수 없습니다")
            self.patch_button.setEnabled(True)
            self.find_dir_button.setEnabled(True)
            self.dir_edit.setEnabled(True)

    def check_Update(self):
        urllib.request.urlretrieve(self.update_url, "MapleStory2_patch_version.txt")
        file = open("MapleStory2_patch_version.txt", 'r')
        list = []
        for i in file.readlines():
            list.append(i)
        version = list[0][0:3]
        compulsion_update = list[1]
        print("This Program Verrsion: " + self.version + "\nNew Version: " + version + "\n필수 업데이트: " + compulsion_update)
        file.close()
        try:
            os.remove("MapleStory2_patch_version.txt")
        except:
            pass

        if self.version == version:
            print("최신 버전이 있습니다")
        else:
            if compulsion_update == "True":
                print("필수 업데이트 진행")
                update_MessageBox = QMessageBox.question(self, "알림", '새로운 버전이 발견됐습니다 업데이트를 진행하겠습니까 ?', QMessageBox.Yes | QMessageBox.No)
                if update_MessageBox == QMessageBox.Yes:
                    url = self.site_url
                    webbrowser.open(url)
                    sys.exit()
                else:
                    QMessageBox.about(self, "Alarm", "필수 업데이트가 필요합니다")
                    sys.exit()
    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
