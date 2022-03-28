# Elephants' Graveyard

某个消失的叫大象的公众号的部分文章备份。

source_1 抓取自 http://web.anyv.net/index.php/account-46983

目录和文件说明

```
\source_1
    article_crawler.py                // 抓取文章内容和图片
    article_info.json                 // 文章标题，时间，链接，封面图链接等
    article_info_crawler.py           // 抓取文章基本信息，生成article_info.json
    \toc_raw                          // 存储文章目录页面
        account-46983.html            // 文章目录页面1
        account-46983-page-2.html     // 文章目录页面2
    \article_raw                      // 存储文章内容
        \article-1027572              // 文章目录
            article-1027572.html      // 文章页面
            ...
```

格式说明

以article_info.json的第一条为例：
```
    "article-4536150": {
        "title": "985 二代「内卷」真的不可避免吗？",
        "link": "http://web.anyv.net/index.php/article-4536150",
        "date": "2021-1-14 09:45",
        "cover_img_link": "http://mmbiz.qpic.cn/mmbiz_jpg/Z08UWq352tkF2ibicuKRCshRu0icgKib39IwG3wibZ0lGy1ygS8ibbvH6q1ico1sUnzdT0iabSDaSialJRTRJaXjfsyJlSw/0?wx_fmt=jpeg",
        "intro": "能不能让效率的归效率，让公平的归公平？",
        "source_page_name": "account-46983.html",
        "article_order": 0
    },
```
article_info.json中的信息抓取自文章目录页面，url格式为account-46983-page-X.html，其中X为页面的编号。
第一页，即公众号首页没有编号:
```
http://web.anyv.net/index.php/account-46983
```
从第二页开始，url为：
```
http://web.anyv.net/index.php/account-46983-page-2.html
http://web.anyv.net/index.php/account-46983-page-3.html
```
article-4536150：文章的key，也是文章的html文件名。每篇文章唯一。文章页面的url格式为 http://web.anyv.net/index.php/article-xxxxx 例如 http://web.anyv.net/index.php/article-4536150 
source_page_name：包含文章的目录页面的文件名
intro：导语。
cover_img_link：封面图片的链接，封面图片暂未抓取至本地。
article_order：文章抓取的顺序，从0开始升序排列。
date：文发布日期。
link：文章页面的链接。

每一篇文章在```\source_1\article_raw```中有单独的目录，目录名为```article_info.json```中的key。文章的html页面名字和key一致。```done.txt```为空文件，供辅助爬虫。其他文件为文章中的图片，格式可能为jpg，png或gif。有些文章页面存在，但实际上页面为空白，这种情况同样创建了对应的目录，其中有```noarticle.txt```作为标记，例如```article-155929```。

没有抓取完整的文章页面，仅抓取了包含文章正文的 ```<div>``` 部分，文章的html未经进一步处理，浏览器不能正常显示。但是文章都完整收录。另外，文章的html文件中的图片链接依然指向原始的来源，如果想进一步处理则要修改图片链接。所有图片都存储在每一篇文章自己的目录里，文件名略有修改以```article-4536150```为例：
其中一个图片为：
```
<img class="rich_pages js_insertlocalimg" data-backh="386" data-backw="578" data-ratio="0.6669921875" data-s="300,640" data-src="https://mmbiz.qpic.cn/mmbiz_jpg/Z08UWq352tkF2ibicuKRCshRu0icgKib39IwkoqHaCSUS8vDA0ANkGFymibxLEHibsOI2ib00icyJ6Q1yXFGBHDxyBcpmA/640?wx_fmt=jpeg" data-type="jpeg" data-w="1024" style="width: 100%;height: auto;"/>
```
```data-src```为图片链接，把结尾的```/640?wx_fmt=jpeg```去掉即得到本地的图片文件名:
```
Z08UWq352tkF2ibicuKRCshRu0icgKib39IwkoqHaCSUS8vDA0ANkGFymibxLEHibsOI2ib00icyJ6Q1yXFGBHDxyBcpmA
```
gif和png处理方法类似。


由于时间精力和能力所限，恕不能进一步整理和格式化文章。如有兴趣请fork。
