import requests
import re
import json

# 爬取页数
PAGE = 10
# 用户代理
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
# 请求链接
URL = "https://maoyan.com/board/4"
# 文件保存名称
FILE_NAME = "top100排行榜"
# 爬取规则
PATTERN = '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>'


def get_one_page(url):
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    return None


def parse_one_page(html):
    pattern = re.compile(PATTERN, re.S,
    )
    items = re.findall(pattern, html)
    for item in items:
        yield {
            "rank": item[0].strip(),
            "image_url": item[1].strip(),
            "film_name": item[2].strip(),
            "actors": item[3].strip()[3:].split(",") if len(item[3]) > 3 else [],
            "release": item[4].strip()[5:] if len(item[4]) > 5 else "",
            # "score": item[5].strip() + item[6].strip(),
        }


def write_to_file(content):
    with open(FILE_NAME + ".txt", "a", encoding="utf-8") as f:
        json_content = json.dumps(content, ensure_ascii=False)
        f.write(json_content + "\n")


def main(offset):
    url = URL + "?offset={}".format(str(offset))
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == "__main__":
    for i in range(PAGE):
        main(offset=i * 10)
