from bs4 import BeautifulSoup
import requests
import re


class Crawling:
    def parser_day(self):
        url = "https://cors.io/?https://www.dropbox.com/s/25xodqbkn5r8dyz/updated.json?dl=1"
        request = requests.get(url)
        document = BeautifulSoup(request.content, 'html.parser')
        document_ = str(document)
        # print(document_)
        regex = re.compile('"t_Gb":"(\d+/\d+/\d+)')
        time_list = regex.findall(document_)[0].split('/')
        time = time_list[2] + "년 " + time_list[1] + "월 " + time_list[0] + "일"
        return time


    def download_url(selfs):
        url = "https://miyuyami.github.io/ms2_patches.html"
        request = requests.get(url)
        document = BeautifulSoup(request.content, 'html.parser')
        print(document.find_all('a', href=True))


if __name__ == "__main__":
    test = Crawling()
    test.download_url()