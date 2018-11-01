from bs4 import BeautifulSoup
import requests
import re
import json
import urllib
import os


class Crawling:
    def parser_day(self):
        try:
            urllib.request.urlretrieve(
                "https://drive.google.com/uc?export=download&id=1nhiBp_nKcJ5PfTIDr0CIQjoauJ4-1kRD", "update.json")
            file = open('update.json')
            data = str(json.load(file))
            file.close()

            try:
                os.remove("update.json")
            except:
                pass

            regex = re.compile("'t_Gb': '(\d+/\d+/\d+)")
            print(data)
            time_list = regex.findall(data)[0].split('/')
            time = time_list[2] + "년 " + time_list[1] + "월 " + time_list[0] + "일"
            return time
        except:
            return "Error"

    def download_url(selfs):
        url = "https://miyuyami.github.io/ms2_patches.html"
        request = requests.get(url)
        document = BeautifulSoup(request.content, 'html.parser')
        print(document.find_all('a', href=True))


if __name__ == "__main__":
    test = Crawling()
    test.parser_day()