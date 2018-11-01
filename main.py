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


class PatchTread(QThread):
    change_value = pyqtSignal(int)
    change_message = pyqtSignal(str)
    change_visible = pyqtSignal(bool)

    def __init__(self, directory, progress, kor_kind_patch_checkBox, patch_index, kor_sound_patch_checkBox, option_url, patch_url_list):
        QThread.__init__(self)
        self.setup_directory = directory + "Data\\"
        self.progress = progress

        self.kor_patch = kor_kind_patch_checkBox
        self.kor_sound_patch = kor_sound_patch_checkBox
        self.kor_sound_boolean = False

        self.option_url = option_url
        self.patch_url_list = patch_url_list

        self.patch_index = patch_index

    def __del__(self):
        self.wait()

    def run(self):
        print("Setup_directory: " + self.setup_directory)
        print("option_url: " + self.option_url)
        print("kor_patch_url: " + self.patch_url_list[0])
        print("kor_noname_patch_url: " + self.patch_url_list[1])
        print("kor_font_patch_url: " + self.patch_url_list[2])
        print("kor_sound_patch_url: " + self.patch_url_list[3])
        self.change_visible.emit(False)
        self.download()
        self.change_visible.emit(True)

    def download_url(self, url):
        self.change_message.emit('파일 다운로드 중 ...')
        urllib.request.urlretrieve(url, self.setup_directory + "kor_patch.zip",
                                   reporthook=self.dlProgress)
        self.patch_process(self.setup_directory)


    def download(self):
        if os.path.exists(self.setup_directory):
            if self.kor_patch.isChecked() and self.kor_sound_patch.isChecked():
                self.download_url(self.patch_url_list[self.patch_index])
                self.kor_sound_boolean = True
                self.download_url(self.patch_url_list[3])
                self.progress = 100
                self.change_value.emit(self.progress)
            elif self.kor_patch.isChecked():
                self.download_url(self.patch_url_list[self.patch_index])
                self.progress = 100
                self.change_value.emit(self.progress)
            elif self.kor_sound_patch.isChecked():
                self.download_url(self.patch_url_list[3])
                self.progress = 100
                self.change_value.emit(self.progress)
        else:
            self.change_message.emit("Data 폴더를 찾을 수 없습니다.")

    def dlProgress(self, count, blockSize, totalSize):
        # 다운로드 header 파일이 없을 경우 임의로 totalSize를 정해줌
        language_totalSize = 130000000
        sound_totalSize = 680000000

        if self.kor_patch.isChecked() and self.kor_sound_patch.isChecked():
            if self.kor_sound_boolean:
                percent = abs(int(count * blockSize * 100 / sound_totalSize) / 2.4) + 42
            else:
                percent = abs(int(count * blockSize * 100 / language_totalSize) / 2.4)
        elif self.kor_patch.isChecked():
            percent = abs(int(count * blockSize * 100 / language_totalSize) / 1.2)
        elif self.kor_sound_patch.isChecked():
            percent = abs(int(count * blockSize * 100 / sound_totalSize) / 1.2)
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
        self.version = "1.01"
        self.kor_patch_url = "https://drive.google.com/uc?export=download&id=1tw1_tzCViJkiXsrRepdwBuYK3g-KMJwF"
        self.kor_noname_patch_url = "https://drive.google.com/uc?export=download&id=1yfXf--tfYAzvth9OWhCuEj3yAVTepMNt"
        self.kor_font_patch_url = "https://drive.google.com/uc?export=download&id=1yNuTQSSSpnyU6h_udILEAwQuWFkXLNO6"
        self.kor_sound_patch_url = "https://www.dropbox.com/s/igfcrtkqcphivlb/Kor_sound2.zip?dl=1"
        self.patch_url_list = [self.kor_patch_url, self.kor_noname_patch_url, self.kor_font_patch_url, self.kor_sound_patch_url]

        self.option_url = "https://drive.google.com/uc?authuser=0&id=14WlWEWAI-wyEQ3TEBqw13H-GJaPKlOTx&export=download"
        self.update_url = "https://drive.google.com/uc?authuser=0&id=1zzbO3PMyUyq1nk_KuBTJrH86992LSUQi&export=download"
        self.site_url = "https://hyrama.com/?p=598"
        self.github_url = "https://github.com/lumyjuwon/Maple2_kor_patch"
        self.check_update()

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

    def confirm_checkBox(self):
        checkBox_Checked_list = [self.kor_patch_checkBox.isChecked(), self.kor_noname_patch_checkBox.isChecked(),
                        self.kor_font_patch_checkBox.isChecked()]
        checkBox_list = [self.kor_patch_checkBox, self.kor_noname_patch_checkBox, self.kor_font_patch_checkBox]
        index_checkBox = 0

        count = 0
        for checkBox in checkBox_Checked_list:
            if checkBox:
                index_checkBox = checkBox_Checked_list.index(checkBox)
                count += 1

        if count >= 2 or (self.kor_sound_patch_checkBox.isChecked() != True and count == 0):
            return False, -1, -1
        elif self.kor_sound_patch_checkBox.isChecked() or count == 1:
            return True, checkBox_list[index_checkBox], index_checkBox

    def patch(self):
        self.progress = 0
        self.progressBar.setValue(self.progress)
        confirm_status = self.confirm_checkBox()
        if confirm_status[0]:
            self.get_thread = PatchTread(self.load_directory(), self.progress, confirm_status[1], confirm_status[2], self.kor_sound_patch_checkBox, self.option_url, self.patch_url_list)
            self.save_dir(self.dir_edit.text())
            if os.path.exists(self.load_directory()):
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
                    self.get_thread.change_visible.connect(self.kor_noname_patch_checkBox.setEnabled)
                    self.get_thread.change_visible.connect(self.kor_font_patch_checkBox.setEnabled)
                    self.get_thread.change_visible.connect(self.kor_sound_patch_checkBox.setEnabled)
                    self.get_thread.start()
            else:
                QMessageBox.about(self, "Error", "이 경로에는 설치할 수 없습니다")
                self.patch_button.setEnabled(True)
                self.find_dir_button.setEnabled(True)
                self.dir_edit.setEnabled(True)
        else:
            QMessageBox.about(self, "Error", "한글패치(1개) 또는 한글 음성패치를 선택해 주시기 바랍니다")


    def check_update(self):
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

        if float(version) > float(self.version) and compulsion_update == "True":
            print("필수 업데이트 진행")
            update_MessageBox = QMessageBox.question(self, "알림", '필수 업데이트가 필요합니다', QMessageBox.Yes | QMessageBox.No)
            if update_MessageBox == QMessageBox.Yes:
                url = self.site_url
                webbrowser.open(url)
                sys.exit()
            if update_MessageBox == QMessageBox.No:
                QMessageBox.about(self, "알림", "프로그램을 종료합니다")
                sys.exit()

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
