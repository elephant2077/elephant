# %%
import scrapy
from scrapy.crawler import CrawlerProcess
import os
from bs4 import BeautifulSoup
import json 
# %%

if os.path.isdir('toc_raw') == False:
    os.mkdir('toc_raw')

# %% download webpages
# create urls
url_list = ['http://web.anyv.net/index.php/account-46983']
base = 'http://web.anyv.net/index.php/account-46983-page-'
for i in range(2,74):
    url_list.append(base+str(i))

# %%
class ArticleListSpider(scrapy.Spider):
    name = "ArticleListSpider"

    def start_requests(self):
        urls = url_list
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = '{}.html'.format(page)
        filepath = os.path.join('toc_raw/',filename)
        with open(filepath, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

# %%
process = CrawlerProcess(settings={
    'FEED_EXPORT_ENCODING': 'utf-8',
}
)
process.crawl(ArticleListSpider)
process.start()
process.stop()

# %% parse downloader file to get article info
files = os.listdir('toc_raw')

# %% sort file name in ascending order
sorted_names = [''] * len(files)

for idx, name in enumerate(files):
    number = int(name.split('-')[-1].split('.')[0])
    if number == 46983: # first page's name format is different
        number = 1
    pos = number - 1
    sorted_names[pos] = name

# %% single file parse test
file = open(os.path.join('toc_raw', sorted_names[0]), "r",encoding='GB2312')
body = file.read()
soup = BeautifulSoup(body, 'html.parser')

image_groups = soup.find_all('div', class_='image group')

group = image_groups[0]

div_grid_news_desc = group.find('div', class_='grid news_desc')
title = div_grid_news_desc.find('h3')
title_text = title.find('a')['title']
intro = div_grid_news_desc.find('p').find('a').contents[0]
date = div_grid_news_desc.find('span', class_='datecss').contents[0]
date = date.replace('\n ', '')
link = title.find('a')['href']
key = link.split('/')[-1]
img_link = group.find('img')['src']

# %% extract info from all pages
article_info_dict = {}
cnt = 0
for file_name in sorted_names:
    file_path = os.path.join('toc_raw', file_name)
    file = open(file_path, "r",encoding='GB18030')
    body = file.read()
    soup = BeautifulSoup(body, 'html.parser')

    image_groups = soup.find_all('div', class_='image group')

    for group in image_groups:
        div_grid_news_desc = group.find('div', class_='grid news_desc')
        title = div_grid_news_desc.find('h3')
        title_text = title.find('a')['title']

        intro = div_grid_news_desc.find('p').find('a')

        if len(intro.contents) != 0: # no intro
            intro_text = intro.contents[0]
        else:
            intro_text = '' # no text
        
        date = div_grid_news_desc.find('span', class_='datecss').contents[0]
        date = date.replace('\n ', '')
        link = title.find('a')['href']
        key = link.split('/')[-1]
        cover_img_link = group.find('img')['src']

        entry = {'title' : title_text,
                'link' : link,
                'date' : date,
                'cover_img_link' : cover_img_link,
                'intro' : intro_text,
                'source_page_name' : file_name,
                'article_order' : cnt}
        
        article_info_dict[key] = entry

        cnt += 1


# %% dump json
# with open("article_info.json", "w") as outfile:
#     json.dump(article_info_dict, outfile, indent=4)

with open('article_info.json', 'w', encoding='utf8') as json_file:
    json.dump(article_info_dict, json_file, ensure_ascii=False, indent=4)
# %%