import requests
import re
import json


class MaoyanSpider:
    def __init__(self, page):
        self.page = page
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        self.url = "https://maoyan.com/board/4"
        self.file_name = "top100排行榜"
        self.rule = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>'

    def _get_one_page(self, url):
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.text
        return None

    def _parse_one_page(self, html):
        pattern = re.compile(self.rule, re.S)
        items = re.findall(pattern, html)
        for item in items:
            yield {
                "rank": item[0].strip(),
                "image_url": item[1].strip(),
                "film_name": item[2].strip(),
                "actors": item[3].strip()[3:].split(",") if len(item[3]) > 3 else [],
                "release": item[4].strip()[5:] if len(item[4]) > 5 else "",
                "score": item[5].strip() + item[6].strip(),
            }

    def _write_to_file(self, content):
        with open(self.file_name + ".txt", "a", encoding="utf-8") as f:
            json_content = json.dumps(content, ensure_ascii=False)
            f.write(json_content + "\n")

    def _main(self, offset):
        url = self.url + "?offset={}".format(str(offset))
        html = self._get_one_page(url)
        for item in self._parse_one_page(html):
            self._write_to_file(item)

    def crawl(self):
        for i in range(self.page):
            self._main(i * 10)


if __name__ == "__main__":
    spider = MaoyanSpider(page=5)
    spider.crawl()
