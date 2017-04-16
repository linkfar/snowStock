"""

Usage:
    snowball_stock.py <stock_code> <num> <sort>

Example:
    snowball_stock.py QQQ 100 alpha
"""
import requests
from docopt import docopt
class SnowBallScraper():
    def __init__(self,stock="SZ300017",num=10,sort="alpha"):
        #stock info
        self.stock_name = ""
        self.stock_code = stock
        self.stock_current_price = ""
        #stock txt field
        self.hot_release = [] # 100 * 10 txt
        self.new_release = [] #100 * 10 txt
        self.num_text = num # 需要的文本数
        self.sort = sort

    def crawl(self):
        self._get_stock_info()
        self._get_text_release()
        self._get_new_release()
        print("you gather {} posts!Go training your model!".format(self.num_text))

    def _get_stock_info(self):
        pass

    def _get_text_release(self):
        url = "https://xueqiu.com/statuses/search.json?"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Referer": "https://xueqiu.com/S/SH600519",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Host": "xueqiu.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cookie": "aliyungf_tc=AQAAAMozukkSsgoAfDxI3hit0rhocX5i; xq_a_token=ca292f8d934efc28f3fd052b7dcf46f14a20a0d3; xq_a_token.sig=OfkwBmKBwnYETfT5NOuElwVwhBY; xq_r_token=d1accc7b0cafd743be1b975a863a146e514d9c80; xq_r_token.sig=LV5APomGXuF1PJGnH9SmAPdxYHc; u=241492319621673; Hm_lvt_1db88642e346389874251b5a1eded6e3=1492319622; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1492320805; s=fd122c1mb6; __utma=1.270476060.1492319630.1492319630.1492319630.1; __utmc=1; __utmz=1.1492319630.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        }
        num_page = self.num_text // 10 + 1
        for page in range(num_page):
            if page+1 == num_page:
                last_num_text = self.num_text % 10
            else:
                last_num_text = 10
            payload = {
                "count": str(last_num_text),
                "comment": "0",
                "symbol": self.stock_code,
                "hl": "0",
                "source": "all",
                "page": str(page+1),
                "sort": self.sort,  # new = time
                "_": "1492323384833",
            }
            r = requests.get(url, headers=headers, params=payload)
            result = r.json()["list"]
            for i in range(len(result)):
                item = result[i]  # item
                title = item["title"]  # 标题
                desc = item["description"]  # 摘要信息
                text = item["text"]  # 文本信息
                retweet_count = item["retweet_count"]  # 转发数
                reply_count = item["reply_count"]  # 评论数
                timeBefore = item["timeBefore"]  # 发布时间
                target_url = item["target"].replace("/","_")  # 原文链接
                textRe = text.replace("<p>", "").replace("</p>", "\n")

                f = open("/Users/vance/Downloads/{}.txt".format((page,i,title)), "w")

                f.write(textRe)
               # print("getting {}".format(title))
    def _get_new_release(self):
        pass


def cli():
    arguments = docopt(__doc__)
    stock = arguments["<stock_code>"]
    num = arguments["<num>"]
    sort = arguments["<sort>"]
    snow = SnowBallScraper(stock,int(num),sort)
    snow.crawl()

if __name__ == '__main__':
    cli()
#snow = SnowBallScraper(stock="SH00001",num=100,sort="time")
#snow.crawl()


