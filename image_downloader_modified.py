# source of original code:
# https://github.com/WuLC/GoogleImagesDownloader
# as described in the first method of the blog
# http://wulc.me/2017/09/23/Google%20%E5%9B%BE%E7%89%87%E7%88%AC%E8%99%AB/

# code has been modified and understood
# controlled image download quantity
# removed supplementary keywords (simplified input)
# randomized image links sample
# removed logger
# simplified exception handling
# string formatting for readability
# adjusted comments
# etc

# to better understand re.findall('src="(.*?)"', page_content) 
# https://docs.python.org/3/library/re.html

# the reason we use user_agent is because we cannot make the request to google without it, otherwise it will be forbidden/denied
# therefore we pass in the user agent in the header when manking the request

# it should be noted that regular expressions are suboptimal for parsing html files


import os
import re
import urllib.request
import urllib.error
from urllib.parse import quote
from user_agent import generate_user_agent
import random


def download_page(url):
    'download raw content of the page (html)'

    try:
        headers = {}
        headers['User-Agent'] = generate_user_agent()
        headers['Referer'] = 'https://www.google.com'
        req = urllib.request.Request(url, headers = headers) #must pass in user agent, or else the request will be denied
        resp = urllib.request.urlopen(req)
        return str(resp.read())
    except Exception as e:
        print(f'Error while downloading page {url}')
        return None


def parse_page(url,image_quantity):
    'parge the page and get a random sample (of specified size) of image links'

    page_content = download_page(url)

    if page_content:
        link_list = re.findall('src="(.*?)"', page_content)
        if len(link_list) == 0:
            return set()
        else:
            return random.sample(set(link_list),image_quantity)
    else:
        return set()


def download_images(main_keyword, image_quantity):
    'download a specified amount of images with the main keyword into the download directory'

    # create a directory for a main keyword
    img_dir =  './images/' + main_keyword + '/'
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    url = 'https://www.google.com/search?q=' + quote(main_keyword) + '&source=lnms&tbm=isch'
    image_links = set()
    image_links = image_links.union(parse_page(url,image_quantity))
        
    #print ("Start downloading...")

    count = 0
    for link in image_links:
        try:
            req = urllib.request.Request(link, headers = {"User-Agent": generate_user_agent()})
            response = urllib.request.urlopen(req)
            data = response.read()
            file_path = img_dir + f'{count+1}.jpg'
            with open(file_path,'wb') as wf:
                wf.write(data)
            #print(f'{main_keyword}/{count}.jpg Download Complete')
            count += 1
        except:
            print('Error while downloading image')

    #print(f"Finished downloading {count} image(s)")


def testprogram():
    try:
        image_quantity = int(input("How many images do you want to download? (limit: 50)\n"))
        if image_quantity > 50:
            print("The limit is 50 images at a time\n")
            return main()
    except:
        print("Please enter a valid base-10 integer\n")
        return main()

    main_keyword = input("Enter the search keyword for the images (e.g. grass green)\n")

    download_images(main_keyword, image_quantity)

