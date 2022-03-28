# %%
import os
from bs4 import BeautifulSoup
import json
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm


base_folder = 'article_raw_redownload'
if os.path.isdir(base_folder) == False:
    os.mkdir(base_folder)
# %%
# Open JSON file
f = open('article_info.json')
article_info = json.load(f)

order_to_key = {}

for key, val in article_info.items():
    order = int(val['article_order'])
    order_to_key[order] = key

# %%
def get_img_url(img):

    image_url = None
    if 'data-src' in img.attrs:
        image_url = img['data-src']
    elif 'src' in img.attrs:
        image_url = img['src']
    else:
        print("no img url")
    
    return image_url

def download_and_save_img(img_url, folder):
    '''
    url format:
    https://mmbiz.qpic.cn/mmbiz_jpg/Z08UWq352tkdNk6grHOa6ZY0P4ObZDiceVrGUpm8l3Yup90Stib99y90PNDFXcJl0IoWp0o23zXiczwvkuNYk54gg/640?wx_fmt=jpeg
    https://mmbiz.qpic.cn/mmbiz_gif/aQ4icLkjZVIic0Y7BZmB2icqAj8tu5mic5NhTLRGVHtAzTMCEPmcbhjollPvIolc4LHqoQvibTc6dCfRmWvicPNUq7BQ/640?
    
    corner case 1: 
    article order: 538, key: article-2171520, title: 真正的中国汽车长什么样｜大象公会
    https://mmbiz.qpic.cn/mmbiz/Z08UWq352tnnic2yGoGnal26RlHzPotBmOPF7B7rpcFJliaW3ZpKOSQZdYd3bXUMfwMicM8tH0rhibTiauccmeo9D7A/640
    
    corner case 2: 
    article order: 557, key: article-2134361, title: 中国什么地方的人最能打｜大象公会
    https://mmbiz.qpic.cn/mmbiz/Z08UWq352tnMYlpbR1u6ZgicCRPh1uVxY8Ur6YfnesuibLRkvmXZOOicICfBLYz85x2u6YmpND3woxpiczEQOUlkOQ/640
    '''

    try:
        r = requests.get(img_url)

        if '=' in img_url:
            img_format = img_url.split('=')[-1]
            img_name = img_url.split('/')[-2] + '.' + img_format # not work with gif
        else:
            if 'gif' in img_url:
                img_format = 'gif'
                img_name = img_url.split('/')[-2] + '.' + img_format
            elif 'jpg' in img_url or 'jpeg' in img_url:
                img_format = 'gif'
                img_name = img_url.split('/')[-2] + '.' + img_format
            elif 'png' in img_url:
                img_format = 'png'
                img_name = img_url.split('/')[-2] + '.' + img_format
            else:
                print('failed to determine format, write as byte format')
                img_name = img_url.split('/')[-2]
                with open(os.path.join(folder, img_name), "wb") as f:
                    f.write(BytesIO(r.content).getbuffer())

                return

        i = Image.open(BytesIO(r.content))
        i.save(os.path.join(folder, img_name))
    except:
        print('image download failed, skip: {}'.format(img_url)) 

# %% for experiment and debug
# url = article_info['article-2715746']['link'] # normal
# # url = article_info['article-2092377']['link'] # empty

# page = requests.get(url)
# soup = BeautifulSoup(page.text, 'html.parser')

# # %%
# div_cont_desc_span_1_of_2 = soup.find('div', class_='cont-desc span_1_of_2')
# div_rich_media_content = soup.find('div', class_='rich_media_content') # if div_rich_media_content len is 0. There is no article
# imgs = div_cont_desc_span_1_of_2.find_all('img') # get images
# img = imgs[0]
# img_url = get_img_url(img)

# download_and_save_img(img_url, 'article_raw/article-2715746.html')

# %%

url_list = ['http://web.anyv.net/index.php/article-2092377',
            'http://web.anyv.net/index.php/article-2715746',
            'http://web.anyv.net/index.php/article-497410']

# %%

download_status = {}

# [0 - 100)  done
# [100, 200) done
# [200, 300) done
# [300, 500) done
# [500, 700) done
# [700, 900) done
# [900, 937) done

# 330-359, need check

for i in tqdm(range(0, 937)):

    key = order_to_key[i]
    url = article_info[key]['link']

    print('article order: {}, key: {}, title: {}'.format(i, key, article_info[key]['title']))

    pagename = url.split("/")[-1]
    filename = '{}.html'.format(pagename)

    # make dir
    article_folder = os.path.join(base_folder, filename).split('.')[-2]
    if os.path.isdir(article_folder) == False:
        os.mkdir(article_folder)

    if os.path.isfile(os.path.join(article_folder, 'done.txt')):
        print('article {} already downloaded, skip'.format(pagename))
        continue

    if os.path.isfile(os.path.join(article_folder, 'noarticle.txt')):
        print('article {} already tried, and no article, skip'.format(pagename))
        continue

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    div_cont_desc_span_1_of_2 = soup.find('div', class_='cont-desc span_1_of_2')
    div_rich_media_content = soup.find('div', class_='rich_media_content') # if div_rich_media_content len is 0. There is no article
    
    if div_rich_media_content is None:
        # no article
        with open(os.path.join(article_folder, 'noarticle.txt'), 'wb') as f:
            f.write(b'')
        
        download_status['pagename'] = 'noarticle'
        print('no article')
        continue
    
    # save article
    with open(os.path.join(article_folder, filename), "w") as file:
        file.write(div_cont_desc_span_1_of_2.prettify())

    imgs = div_cont_desc_span_1_of_2.find_all('img') # get images

    if len(imgs) != 0:
        for img in imgs:
            img_url = get_img_url(img)
            if img_url is None:
                print('no img url, skip: {}'.format(img))
                continue
            download_and_save_img(img_url, os.path.join(article_folder))

    with open(os.path.join(article_folder, 'done.txt'), 'wb') as f:
        f.write(b'')

