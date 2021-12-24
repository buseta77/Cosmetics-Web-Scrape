from bs4 import BeautifulSoup
import requests
import shutil
import pandas as pd
from selenium import webdriver
import json
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os


def get_images_cosmetify(url, product_reference):
    counter = 1
    complete_list_url = []
    url_index = url.find('?')
    if url_index != -1:
        url = url[:url_index]
    url_base = 'https://www.cosmetify.com/'
    url_extension = str(url).replace('https://www.cosmetify.com/', '')
    if 'us/' in url_extension:
        img_name = url_extension.replace('us/', '').lower()
    else:
        img_name = url_extension.lower()
    image_name = str(img_name) + '-' + str(counter) + '.jpg'
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    product_block = soup.find('div', {'class': 'info'})
    product_name = product_block.find('h1').text
    thumbnails = soup.find('div', {'id': 'pdtImgThbs'})
    if thumbnails is None:
        main_image_part = soup.find('div', {'class': 'pdtImg pdtNoSlide'})
        main_image = main_image_part.find('img', {'height': '550', 'width': '550'})
        image_url_ext = main_image['src']
        image_url = url_base + image_url_ext
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            with open(image_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                list_url = 'https://storage.googleapis.com/my-way-beauty.appspot.com/' + str(image_name)
                complete_list_url.append(list_url)
    else:
        for image in thumbnails.find_all('img', {'height': '55', 'width': '55'}):
            image_url_ext = image['data-src']
            image_url = url_base + image_url_ext
            r = requests.get(image_url, stream=True)
            if r.status_code == 200:
                with open(image_name, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                    complete_list_url.append(list_url)
                    counter += 1
                    image_name = str(img_name) + '-' + str(counter) + '.jpg'
    complete_list_pre = ', '.join(complete_list_url)
    complete_list = [complete_list_pre]
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    cosmetify_new_images = pd.DataFrame(rows)

    return cosmetify_new_images


def get_images_amazon(url, product_reference, driver_path):
    counter = 1
    complete_list_url = []
    url_index = url.find('?')
    if url_index != -1:
        url = url[:url_index]
    url_extension = str(url).replace('https://www.amazon.com/', '')
    index = url_extension.find('dp/')
    img_name = url_extension[:index].lower()
    image_name = img_name + str(counter) + '.jpg'
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    title = soup.find('span', {'id': 'productTitle'})
    product_name = title.text.strip()
    keyword = "P.when('A').register"
    element = soup.find('div', {'id': 'leftCol'})
    real_script = ''
    for scr in element.find_all('script', {'type': 'text/javascript'}):
        if keyword in str(scr):
            real_script = scr
    texts = str(real_script).replace('\n', '')
    left = "colorImages': { 'initial': "
    right = "},       "
    json_script = texts[texts.index(left)+len(left):texts.index(right)]
    content_json = json.loads(json_script)
    for key in content_json:
        test = key['hiRes']
        if test is None:
            image_url = key['large']
        else:
            image_url = key['hiRes']
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            with open(image_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                complete_list_url.append(list_url)
                counter += 1
                image_name = img_name + str(counter) + '.jpg'
    complete_list_pre = ', '.join(complete_list_url)
    complete_list = [complete_list_pre]
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    amazon_new_images = pd.DataFrame(rows)

    return amazon_new_images


def get_images_sephora(url, product_reference, driver_path):
    counter = 1
    complete_list_url = []
    url_index = url.find('?')
    if url_index != -1:
        url = url[:url_index]
    img_name = str(url).replace('https://www.sephora.com/product/', '').lower()
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    product_name = soup.find('span', {'data-at': 'product_name'}).text
    image_name = img_name + '-' + str(counter) + '.jpg'
    image_list = soup.find('div', {'class': 'css-122y91a'})
    for thumb in image_list.find_all('div', {'class': 'css-aaj5ah'}):
        img_elt = thumb.find('img')
        if img_elt['alt'] != 'Video':
            img_url = img_elt['src'].replace('?imwidth=48', '')
            r = requests.get(img_url, stream=True, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
            if r.status_code == 200:
                with open(image_name, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                    complete_list_url.append(list_url)
                    counter += 1
                    image_name = img_name + str(counter) + '.jpg'
    complete_list_pre = ', '.join(complete_list_url)
    complete_list = [complete_list_pre]
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    sephora_new_images = pd.DataFrame(rows)

    return sephora_new_images


def get_images_colourpop(url, product_reference, driver_path):
    counter = 1
    complete_list_url = []
    url_index = url.find('?')
    if url_index != -1:
        url = url[:url_index]
    img_name = str(url).replace('https://colourpop.com/products/', '').lower()
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    product_name = soup.find('div', {'class': 'product-details__info hidetablet'}).text.replace('\n', ' ').strip()
    image_name = img_name + '-' + str(counter) + '.jpg'
    elt = soup.find('div', {'class': 'product-images__carousel product-images__carousel--desktop hidetablet'})
    for img_elt in elt.find_all('div', {'class': 'product-image'}):
        image_url = img_elt['data-src']
        img_url = 'http:' + image_url
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(image_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                complete_list_url.append(list_url)
                counter += 1
                image_name = img_name + '-' + str(counter) + '.jpg'
    complete_list_pre = ', '.join(complete_list_url)
    complete_list = [complete_list_pre]
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    colourpop_new_images = pd.DataFrame(rows)

    return colourpop_new_images


def get_images_elf(url, product_reference, driver_path):
    counter = 1
    complete_list_url = []
    url_index = url.find('?')
    if url_index != -1:
        url = url[:url_index]
    img_name = str(url).replace('.html', '').replace('https://www.elfcosmetics.com/', '').replace('/', '-').lower()
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    product_name = soup.find('h1', {'class': 'product-name'}).text
    image_name = img_name + '-' + str(counter) + '.jpg'
    elt = soup.find('div', {'id': 'thumbnails'})
    for img_elt in elt.find_all('li'):
        list_ext = img_elt.find('img')['data-lgimg']
        script = json.loads(list_ext)
        img_url = script['hires']
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(image_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                complete_list_url.append(list_url)
                counter += 1
                image_name = img_name + '-' + str(counter) + '.jpg'
    complete_list_pre = ', '.join(complete_list_url)
    complete_list = [complete_list_pre]
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    elf_new_images = pd.DataFrame(rows)

    return elf_new_images


def get_images_maybelline(url, product_reference, driver_path):
    counter = 1
    complete_list_url = []
    url_index = url.find('?')
    if url_index != -1:
        url = url[:url_index]
    img_name = url.replace('https://www.maybelline.com/', '').replace('/', '-').lower()
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    product_block = soup.find('div', {'class': 'prod-title__section product-info__title'})
    product_name = product_block.find('h1').text.replace('\n', '')
    image_name = img_name + '-' + str(counter) + '.jpg'
    element = soup.find('div', {'class': 'PDP-img__top'})
    image_list = ''
    for block in element.find_all('ul'):
        check = block['class']
        if 'active' in str(check):
            image_list = block
    for img in image_list.find_all('img'):
        url_extension = img['src']
        img_url = 'http://maybelline.com' + url_extension
        index = img_url.find('?')
        image_url = img_url[:index]
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            with open(image_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                complete_list_url.append(list_url)
                counter += 1
                image_name = img_name + '-' + str(counter) + '.jpg'
    complete_list_pre = ', '.join(complete_list_url)
    complete_list = [complete_list_pre]
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    maybelline_new_images = pd.DataFrame(rows)

    return maybelline_new_images


def get_images_bing(csv_file, driver_path):
    driver = webdriver.Chrome(executable_path=driver_path)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    search_queries = pd.read_csv(csv_file)
    search_list = search_queries['Name']
    references = search_queries['Ref']
    product_reference, product_name, picture, text, complete_list = [], [], [], [], []
    s = 0
    while s < len(search_list):
        i = 1
        complete_list_url = []
        url_core = 'https://www.bing.com/images/search?q='
        url_ext = search_list[s]
        product_name.append(url_ext)
        product_reference.append(references[s])
        url_ext2 = url_ext.replace(' ', '+')
        url_ext3 = url_ext.replace(' ', '-').lower()
        url = url_core + url_ext2
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        image_name = url_ext3 + '-' + str(i) + '.jpg'
        for j in [0, 1]:
            table = soup.find('ul', {'data-row': j})
            if table is None:
                table = soup.find('ul', {'data-col': j + 1})
                if table is None:
                    continue
            for element in table.find_all('a', {'class': 'iusc'}):
                all_name = element['m']
                to_json = json.loads(all_name)
                image_url = to_json['murl']
                try:
                    r = requests.get(image_url, stream=True, headers=headers, timeout=1)
                    if r.status_code == 200:
                        with open(image_name, 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                            list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                            complete_list_url.append(list_url)
                            i += 1
                            image_name = url_ext3 + '-' + str(i) + '.jpg'
                except:
                    time.sleep(10)
                    continue
        complete_list_pre = ', '.join(complete_list_url)
        complete_list.append(complete_list_pre)
        s += 1
    driver.quit()
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    bing_new_images = pd.DataFrame(rows)

    return bing_new_images


def get_images_ulta(url, product_reference):
    counter = 1
    complete_list_url = []
    url_index = url.find('?')
    if url_index != -1:
        url = url[:url_index]
    url_extension = str(url).replace('https://www.ulta.com/p/', '').lower()
    image_name = str(url_extension) + '-' + str(counter) + '.jpg'
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    product_name = soup.find('h1', {'class': 'Title Title--subtitle-1 Title--small'}).text
    name = soup.find('div', {'class': 'ProductImage__thumbNails'})
    if name is None:
        print('Error!')
    else:
        for image in name.find_all('img'):
            url_ext = image['src'].replace('?$tn$', '')
            r = requests.get(url_ext, stream=True)
            if r.status_code == 200:
                with open(image_name, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                    list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                    complete_list_url.append(list_url)
                    counter += 1
                    image_name = str(url_extension) + '-' + str(counter) + '.jpg'
    complete_list_pre = ', '.join(complete_list_url)
    complete_list = [complete_list_pre]
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    ulta_new_images = pd.DataFrame(rows)

    return ulta_new_images


def get_images_temptalia(url, product_reference):
    counter = 1
    complete_list_url = []
    url_index = url.find('?')
    if url_index != -1:
        url = url[:url_index]
    url_extension = str(url).replace('https://www.temptalia.com/', '').replace('/', '-').lower()
    image_name = str(url_extension) + '-' + str(counter) + '.jpg'
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    name = soup.find('div', {'class': 'slickslide my-2'})
    product_name = name.find('figcaption', {'class': 'pt-2 f-2 sans-serif text-uppercase text-center'})
    extra = name.find('img', {'src-set': ''})
    extra_url = extra['data-lazy-src']
    r = requests.get(extra_url, stream=True)
    if r.status_code == 200:
        with open(image_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
            complete_list_url.append(list_url)
            counter += 1
            image_name = str(url_extension) + '-' + str(counter) + '.jpg'
    for image in name.find_all('div', {'class': 'lazy-image'}):
        img = image.find('img')
        url_ext = img['data-lazy']
        r = requests.get(url_ext, stream=True)
        if r.status_code == 200:
            with open(image_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                list_url = 'https://storage.googleapis.com/my-way-beauty/' + str(image_name)
                complete_list_url.append(list_url)
                counter += 1
                image_name = str(url_extension) + '-' + str(counter) + '.jpg'
    complete_list_pre = ', '.join(complete_list_url)
    complete_list = [complete_list_pre]
    rows = {'Product Ref': product_reference, 'Product Name': product_name, 'Product List URLs': complete_list}
    temptalia_new_images = pd.DataFrame(rows)

    return temptalia_new_images


def upload_firebase(login_json, bucket_name, image_folder):
    cred = credentials.Certificate(login_json)
    firebase_admin.initialize_app(cred, {'storageBucket': 'my-way-beauty.appspot.com'})
    bucket = storage.bucket(bucket_name)
    directory = image_folder
    for image in os.listdir(directory):
        blob = bucket.blob(f'{image}')
        imagePath = directory + image
        blob.upload_from_filename(imagePath)
