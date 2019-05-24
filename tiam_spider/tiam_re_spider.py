import re
import json

import requests
import pymysql


class TiamSpider:
    def __init__(self, page):
        self.page = page
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        self.file_name = "2019年最新動画人気ランキング"
        self.rule = '<article.*?href="(.*?)".*?src="(.*?)".*?<h2.*?>.*?>(.*?)</a>.*?</i>(.*?)</span>.*?</i>.*?>(.*?)</a>.*?</i>.*?>(.*?)</a>'
        self.db = pymysql.connect(
            host="shiqinying.xyz", port=3306, user="root", password="root", db="spiders"
        )
        self.cursor = self.db.cursor()

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
                "href": item[0].strip(),
                "image": item[1].strip(),
                "title": item[2].strip(),
                "view": int(item[3].strip()[:-3].replace(",", "")),
                "name": item[4].strip(),
                "category": item[5].strip(),
            }

    def _write_to_file(self, content):
        with open(self.file_name + ".txt", "a", encoding="utf-8") as f:
            json_content = json.dumps(content, ensure_ascii=False)
            f.write(json_content + "\n")

    def _write_to_mysql(self, content):

        data = content

        table = "tiam_rank"
        keys = ",".join(data.keys())
        values = ",".join(["%s"] * len(data))
        sql = "insert ignore into {table} ({keys}) values ({values})".format(
            table=table, keys=keys, values=values
        )
        try:
            ret = self.cursor.execute(sql, tuple(data.values()))
            if ret:
                print("Successful")
                self.db.commit()
        except Exception as e:
            print("Failed")
            print(e)
            self.db.rollback()

    def _main(self, page):
        # https://tiam.jp/post_ranking/page/803
        url = "https://tiam.jp/post_ranking/page/{}".format(str(page))
        html = self._get_one_page(url)
        items = self._parse_one_page(html)
        for item in items:
            self._write_to_mysql(item)

    def crawl(self):

        for i in range(1, self.page + 1):
            self._main(i)

        self.db.close()


if __name__ == "__main__":
    spider = TiamSpider(page=100)
    spider.crawl()
