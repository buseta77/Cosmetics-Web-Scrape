import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from requests.models import PreparedRequest
import math


def get_reviews_sephora(product_url, product_reference, driver_path):
    counter = 0
    product_no, rev_number, rating, reviews, title, helpful, attributes = [], [], [], [], [], [], []
    purchase, variant, recommended = [], [], []
    rev_index = 1
    url_index = product_url.find('?')
    if url_index != -1:
        product_url = product_url[:url_index]
    url_serial = product_url.rpartition('-')[-1]
    prod_serial = 'ProductId:' + url_serial

    url = 'https://api.bazaarvoice.com/data/reviews.json'
    params = {
        'Filter': prod_serial,
        'Sort': 'SubmissionTime:desc',
        'Limit': 6,
        'Offset': 0,
        'Include': 'Products,Comments',
        'Stats': 'Reviews',
        'passkey': 'caQ0pQXZTqFVYA1yYnnJ9emgUiW59DXA85Kxry8Ma02HE',
        'apiversion': 5.4,
        'Locale': 'en_US'}

    req = PreparedRequest()
    req.prepare_url(url, params)
    r = requests.get(req.url)
    cont = r.json()

    total_rev = cont['TotalResults']
    prod_keys = cont['Includes']['Products'].keys()
    prod_id = list(prod_keys)[0]
    brand = cont['Includes']['Products'][prod_id]['Brand']['Name']
    rating2 = cont['Includes']['Products'][prod_id]['ReviewStatistics']['AverageOverallRating']
    recommended2 = cont['Includes']['Products'][prod_id]['ReviewStatistics']['RecommendedCount']
    about2 = cont['Includes']['Products'][prod_id]['Description']

    while counter < total_rev:
        url1 = 'https://api.bazaarvoice.com/data/reviews.json'
        params1 = {
            'Filter': prod_serial,
            'Sort': 'SubmissionTime:desc',
            'Limit': 100,
            'Offset': counter,
            'Include': 'Products,Comments',
            'Stats': 'Reviews',
            'passkey': 'caQ0pQXZTqFVYA1yYnnJ9emgUiW59DXA85Kxry8Ma02HE',
            'apiversion': 5.4,
            'Locale': 'en_US'}
        req1 = PreparedRequest()
        req1.prepare_url(url1, params1)
        r = requests.get(req1.url)
        cont1 = r.json()
        if total_rev - counter > 99:
            for j in range(0, 100):
                rev = cont1['Results'][j]['ReviewText']
                if rev is not None:
                    rev.replace('\n', ' ')
                reviews.append(rev)
                product_no.append(product_reference)
                rev_number.append(rev_index)
                rev_index += 1
                if 'eyeColor' in cont1['Results'][j]['ContextDataValues']:
                    eye = cont1['Results'][j]['ContextDataValues']['eyeColor']['ValueLabel']
                else:
                    eye = 'No'
                if 'hairColor' in cont1['Results'][j]['ContextDataValues']:
                    hair = cont1['Results'][j]['ContextDataValues']['hairColor']['ValueLabel']
                else:
                    hair = 'No'
                if 'skinTone' in cont1['Results'][j]['ContextDataValues']:
                    skin = cont1['Results'][j]['ContextDataValues']['skinTone']['ValueLabel']
                else:
                    skin = 'No'
                if 'skinType' in cont1['Results'][j]['ContextDataValues']:
                    skin2 = cont1['Results'][j]['ContextDataValues']['skinType']['ValueLabel']
                else:
                    skin2 = 'No'
                char = [eye + ' eye color', hair + ' hair color', skin + ' skin color', skin2 + ' skin type']
                chars = ', '.join(char)
                attributes.append(chars)
                rate = cont1['Results'][j]['Rating']
                rating.append(rate)
                recommend = cont1['Results'][j]['IsRecommended']
                rec = str(recommend)
                if rec == "False":
                    recommended.append('No')
                else:
                    recommended.append('Yes')
                tit = cont1['Results'][j]['Title']
                title.append(tit)
                pos_fb = cont1['Results'][j]['TotalPositiveFeedbackCount']
                neg_fb = cont1['Results'][j]['TotalNegativeFeedbackCount']
                fb_count = pos_fb - neg_fb
                helpful.append(fb_count)
                if 'VerifiedPurchaser' in cont1['Results'][j]['ContextDataValues']:
                    purch = cont1['Results'][j]['ContextDataValues']['VerifiedPurchaser']['ValueLabel']
                    purchase.append(purch)
                else:
                    purchase.append('No')
                var_id = cont1['Results'][j]['ProductId']
                var_name = cont1['Includes']['Products'][var_id]['Name']
                variant.append(var_name)
        else:
            for j in range(0, total_rev - counter):
                rev = cont1['Results'][j]['ReviewText']
                if rev is not None:
                    rev.replace('\n', ' ')
                reviews.append(rev)
                product_no.append(product_reference)
                rev_number.append(rev_index)
                rev_index += 1
                if 'eyeColor' in cont1['Results'][j]['ContextDataValues']:
                    eye = cont1['Results'][j]['ContextDataValues']['eyeColor']['ValueLabel']
                else:
                    eye = 'No'
                if 'hairColor' in cont1['Results'][j]['ContextDataValues']:
                    hair = cont1['Results'][j]['ContextDataValues']['hairColor']['ValueLabel']
                else:
                    hair = 'No'
                if 'skinTone' in cont1['Results'][j]['ContextDataValues']:
                    skin = cont1['Results'][j]['ContextDataValues']['skinTone']['ValueLabel']
                else:
                    skin = 'No'
                if 'skinType' in cont1['Results'][j]['ContextDataValues']:
                    skin2 = cont1['Results'][j]['ContextDataValues']['skinType']['ValueLabel']
                else:
                    skin2 = 'No'
                char = [eye + ' eye color', hair + ' hair color', skin + ' skin color', skin2 + ' skin type']
                chars = ', '.join(char)
                attributes.append(chars)
                rate = cont1['Results'][j]['Rating']
                rating.append(rate)
                recommend = cont1['Results'][j]['IsRecommended']
                rec = str(recommend)
                if rec == "False":
                    recommended.append('No')
                else:
                    recommended.append('Yes')
                tit = cont1['Results'][j]['Title']
                title.append(tit)
                pos_fb = cont1['Results'][j]['TotalPositiveFeedbackCount']
                neg_fb = cont1['Results'][j]['TotalNegativeFeedbackCount']
                fb_count = pos_fb - neg_fb
                helpful.append(fb_count)
                if 'VerifiedPurchaser' in cont1['Results'][j]['ContextDataValues']:
                    purch = cont1['Results'][j]['ContextDataValues']['VerifiedPurchaser']['ValueLabel']
                    purchase.append(purch)
                else:
                    purchase.append('No')
                var_id = cont1['Results'][j]['ProductId']
                var_name = cont1['Includes']['Products'][var_id]['Name']
                variant.append(var_name)
        counter += 100

    review_row = {'Product Ref': product_no, 'Review Number': rev_number, 'Rating': rating, 'Recommended': recommended,
                  'Title': title, 'Comment': reviews, 'Helpful': helpful, 'Attributes': attributes,
                  'Purchased': purchase, 'Variant': variant}
    sephora_review_df = pd.DataFrame(review_row)

    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(product_url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    prod_name = soup.find('span', {'data-at': 'product_name'}).text
    loves = soup.find('span', class_='css-jk94q9').text
    colour = []
    for bb in soup.find_all("div", {"data-at": "color_swatch_name"}):
        bbb = bb.text.replace('  ', '')
        colour.append(bbb)
    variant2 = ', '.join(colour)
    if len(colour) > 0:
        variant3 = str(len(colour)) + ': ' + variant2
    else:
        variant3 = '1: ' + prod_name
    about3 = soup.find('div', {'class': 'css-1kcruh2 eanm77i0'}).text.strip()
    about4 = about3.replace('\n', ' ')
    index2 = about4.find('What it is: ')
    about5 = about4[index2:].replace('Show more', '')
    ingred = soup.find('div', {'aria-labelledby': 'ingredients_heading'})
    if ingred is not None:
        ingred_2 = ingred.text
    else:
        ingred_2 = ''
    how_to = soup.find('div', {'data-at': 'how_to_use_section'})
    if how_to is not None:
        how_to_2 = how_to.text
    else:
        how_to_2 = ''

    prod_ref_2, link_2, brand_name_2, prod_name_2, star_2, review_count_2,  = [], [], [], [], [], []
    total_recommend_2, love_count_2, swatches_2, prod_ingred_2 = [], [], [], []
    prod_ref_2.append(product_reference)
    link_2.append(product_url)
    brand_name_2.append(brand)
    prod_name_2.append(prod_name)
    star_2.append(rating2)
    review_count_2.append(total_rev)
    total_recommend_2.append(recommended2)
    love_count_2.append(loves)
    swatches_2.append(variant3)
    prod_info_2 = []
    if about2 is None:
        prod_info_2.append(about5)
    else:
        prod_info_2.append(about2)
    if ingred_2 is not None:
        prod_ingred_2.append(ingred_2)
    else:
        prod_ingred_2.append('')
    prod_howto_2 = []
    if how_to_2 is not None:
        prod_howto_2.append(how_to_2)
    else:
        prod_howto_2.append('')

    info_row = {'Product Ref': prod_ref_2, 'Url': link_2, 'Brand': brand_name_2, 'Product': prod_name_2,
                'Rating': star_2, 'Review Count': review_count_2, 'How Many Recommended': total_recommend_2,
                'Loves': love_count_2, 'Variants': swatches_2, 'About': prod_info_2,
                'Ingredients': prod_ingred_2, 'How to Use': prod_howto_2}
    sephora_info_df = pd.DataFrame(info_row)

    return sephora_review_df, sephora_info_df


def get_reviews_ulta(product_url, product_reference, driver_path):
    counter = 0
    product_no, rev_number, rating, reviews, title, helpful, attributes = [], [], [], [], [], [], []
    purchase, variant, recommended = [], [], []
    rev_index = 1
    url_index = product_url.find('?')
    if url_index != -1:
        product_url = product_url[:url_index]
    url_serial = product_url.rpartition('-')[-1]

    url = 'https://display.powerreviews.com/m/6406/l/en_US/product/' + url_serial + '/reviews'
    params = {
        'paging.from': counter,
        'paging.size': 25,
        'filters': '',
        'search': '',
        'sort': 'Newest',
        'image_only': 'false',
        '_noconfig': 'true',
        'apikey': 'daa0f241-c242-4483-afb7-4449942d1a2b'}

    req = PreparedRequest()
    req.prepare_url(url, params)
    r = requests.get(req.url)
    cont = r.json()
    total_rev = cont['paging']['total_results']
    rating2 = cont['results'][0]['rollup']['average_rating']
    recom_ratio = cont['results'][0]['rollup']['recommended_ratio']
    recommended2 = total_rev * recom_ratio
    prod_name = cont['results'][0]['rollup']['name']

    while counter < total_rev:
        url1 = url
        params1 = {
            'paging.from': counter,
            'paging.size': 25,
            'filters': '',
            'search': '',
            'sort': 'Newest',
            'image_only': 'false',
            '_noconfig': 'true',
            'apikey': 'daa0f241-c242-4483-afb7-4449942d1a2b'}

        req1 = PreparedRequest()
        req1.prepare_url(url1, params1)
        r = requests.get(req1.url)
        cont1 = r.json()
        if total_rev - counter > 24:
            for j in range(0, 25):
                rev = cont1['results'][0]['reviews'][j]['details']['comments']
                if rev is not None:
                    rev.replace('\n', ' ')
                reviews.append(rev)
                product_no.append(product_reference)
                rev_number.append(rev_index)
                rev_index += 1
                rate = cont1['results'][0]['reviews'][j]['metrics']['rating']
                rating.append(rate)
                if 'bottom_line' in cont1['results'][0]['reviews'][j]['details']:
                    recommend = cont1['results'][0]['reviews'][j]['details']['bottom_line']
                else:
                    recommend = 'No'
                recommended.append(recommend)
                tit = cont1['results'][0]['reviews'][j]['details']['headline']
                title.append(tit)
                pos_fb = cont1['results'][0]['reviews'][j]['metrics']['helpful_votes']
                neg_fb = cont1['results'][0]['reviews'][j]['metrics']['not_helpful_votes']
                fb_count = pos_fb - neg_fb
                helpful.append(fb_count)
                purch = cont1['results'][0]['reviews'][j]['badges']['is_verified_buyer']
                pur = str(purch)
                if pur == 'true':
                    purchase.append('Yes')
                else:
                    purchase.append('No')
                variant.append(prod_name)
                attributes.append('')
        else:
            for j in range(0, total_rev - counter):
                rev = cont1['results'][0]['reviews'][j]['details']['comments']
                if rev is not None:
                    rev.replace('\n', ' ')
                reviews.append(rev)
                product_no.append(product_reference)
                rev_number.append(rev_index)
                rev_index += 1
                rate = cont1['results'][0]['reviews'][j]['metrics']['rating']
                rating.append(rate)
                if 'bottom_line' in cont1['results'][0]['reviews'][j]['details']:
                    recommend = cont1['results'][0]['reviews'][j]['details']['bottom_line']
                else:
                    recommend = 'No'
                recommended.append(recommend)
                tit = cont1['results'][0]['reviews'][j]['details']['headline']
                title.append(tit)
                pos_fb = cont1['results'][0]['reviews'][j]['metrics']['helpful_votes']
                neg_fb = cont1['results'][0]['reviews'][j]['metrics']['not_helpful_votes']
                fb_count = pos_fb - neg_fb
                helpful.append(fb_count)
                purch = cont1['results'][0]['reviews'][j]['badges']['is_verified_buyer']
                pur = str(purch)
                if pur == 'true':
                    purchase.append('Yes')
                else:
                    purchase.append('No')
                variant.append(prod_name)
                attributes.append('')
        counter += 25

    review_row = {'Product Ref': product_no, 'Review Number': rev_number, 'Rating': rating, 'Recommended': recommended,
                  'Title': title, 'Comment': reviews, 'Helpful': helpful, 'Attributes': attributes,
                  'Purchased': purchase, 'Variant': variant}
    ulta_review_df = pd.DataFrame(review_row)

    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(product_url)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    driver.quit()
    colour = []
    for swatch in soup.find_all('div', class_='Image ProductSwatchImage__image ProductSwatchImage__image--circle'):
        vary = swatch.find('img')
        color = vary['alt']
        colour.append(color)
    varian_2 = ', '.join(colour)
    variant_2 = varian_2.replace('  ', '')
    if len(colour) > 0:
        swatch = str(len(colour)) + ': ' + variant_2
    else:
        swatch = '1: ' + prod_name
    about2 = soup.find('div', {'class': 'ProductDetail__productDetails', 'id': 'productDetails'})
    if about2 is not None:
        about23 = about2.text.replace('Details', '').replace('  ', '').strip()
    else:
        about23 = 'Missing'
    ingred_2 = soup.find('div', class_='ProductDetail__ingredients')
    if ingred_2 is not None:
        ingred_23 = ingred_2.text.replace('Ingredients', '')
    else:
        ingred_23 = 'Missing'
    how_to2 = soup.find('div', class_='ProductDetail__howToUse')
    if how_to2 is not None:
        how_to23 = how_to2.text.replace('How to Use', '')
    else:
        how_to23 = 'Missing'
    brand = soup.find('p', class_='Text Text--body-1 Text--left Text--bold Text--small Text--$magenta-50').text.strip()

    prod_ref_2, link_2, brand_name_2, prod_name_2, star_2, review_count_2,  = [], [], [], [], [], []
    total_recommend_2, love_count_2, swatches_2, prod_ingred_2 = [], [], [], []
    prod_ref_2.append(product_reference)
    link_2.append(product_url)
    brand_name_2.append(brand)
    prod_name_2.append(prod_name)
    star_2.append(rating2)
    review_count_2.append(total_rev)
    total_recommend_2.append(int(recommended2))
    love_count_2.append('Missing')
    swatches_2.append(swatch)
    prod_info_2, prod_howto_2 = [], []
    prod_info_2.append(about23)
    prod_ingred_2.append(ingred_23)
    prod_howto_2.append(how_to23)

    info_row = {'Product Ref': prod_ref_2, 'Url': link_2, 'Brand': brand_name_2,
                'Product': prod_name_2, 'Rating': star_2, 'Review Count': review_count_2,
                'How Many Recommended': total_recommend_2, 'Loves': love_count_2,
                'Variants': swatches_2, 'About': prod_info_2, 'Ingredients': prod_ingred_2, 'How to Use': prod_howto_2}
    ulta_info_df = pd.DataFrame(info_row)

    return ulta_review_df, ulta_info_df


def get_reviews_amazon(product_url, product_reference, driver_path):
    a, j, b = 1, 1, 0
    review_count, all_reviews, product_ref, rating, recommended = [], [], [], [], []
    title, helpful, attributes, purchase, variant = [], [], [], [], []
    url_index = product_url.find('?')
    if url_index != -1:
        product_url = product_url[:url_index]
    url_review = product_url.replace('/dp/', '/product-reviews/')
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(url_review)
    content_2 = driver.page_source
    soup_2 = BeautifulSoup(content_2, 'html.parser')
    dd = soup_2.find(text=lambda t: "global review" in t).text
    index = dd.find('| ')
    cc = dd[index:].replace('| ', '').replace(' global reviews', '').replace(' global review', '')
    page_counter = math.ceil(int(cc) / 10)

    while a - 1 < page_counter:
        params = {
            'pageNumber': a}
        req = PreparedRequest()
        req.prepare_url(url_review, params)
        driver.get(req.url)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        for element in soup.find_all('div', {'data-hook': 'review'}):
            review = element.find('span', {'data-hook': 'review-body'})
            rev = review.text.replace('\n', ' ')
            rev2 = rev.replace('    ', '')
            all_reviews.append(rev2)
            review_count.append(j)
            j += 1
            product_ref.append(product_reference)
            recommended.append('Missing')
            title.append('Missing')
            attributes.append('Missing')
            helpful.append(0)
        vary = soup.find('a', {'data-hook': 'product-link', 'class': 'a-link-normal'})
        for element5 in soup.find_all('div', class_='a-section celwidget'):
            vary2 = element5.find('a', class_='a-size-mini a-link-normal a-color-secondary')
            if vary2 is None:
                variant.append(vary.text)
            else:
                variant.append(vary2.text)
        for element2 in soup.find_all('i', {'data-hook': 'review-star-rating'}):
            star = element2.find('span')
            rate = star.text
            rate2 = rate.replace('.0 out of 5 stars', '')
            rating.append(rate2)
        for element20 in soup.find_all('i', {'data-hook': 'cmps-review-star-rating'}):
            star = element20.find('span')
            rate = star.text
            rate2 = rate.replace('.0 out of 5 stars', '')
            rating.append(rate2)
        for element3 in soup.find_all('div',
                                      class_='a-row a-expander-container a-expander-inline-container cr-vote-action-bar'):
            elt = element3.find('span', {'data-hook': 'helpful-vote-statement',
                                         'class': 'a-size-base a-color-tertiary cr-vote-text'})
            if elt is None:
                helpful[b] = 0
                b += 1
            else:
                help_box = elt.text
                help2 = help_box.replace(' people found this helpful', '')
                help3 = help2.replace('One person found this helpful', '1')
                helpful[b] = help3
                b += 1
        for element4 in soup.find_all('div', class_='a-section celwidget'):
            purcc = element4.find('span', class_='a-size-mini a-color-state a-text-bold')
            if purcc is None:
                purchase.append('No')
            else:
                purchase.append('Yes')
        a += 1

    review_row = {'Product Ref': product_ref, 'Review Number': review_count, 'Rating': rating,
                  'Recommended': recommended, 'Title': title, 'Comment': all_reviews, 'Helpful': helpful,
                  'Attributes': attributes, 'Purchased': purchase, 'Variant': variant}
    amazon_review_df = pd.DataFrame(review_row)

    driver.get(product_url)
    content_3 = driver.page_source
    soup_3 = BeautifulSoup(content_3, 'html.parser')
    driver.quit()

    prod_ref_2, link_2, brand_name_2 = [], [], []
    prod_ref_2.append(product_reference)
    link_2.append(url_review)
    brn = soup_2.find('div', {'data-hook': 'cr-product-byline'})
    if brn is not None:
        brand = brn.text.replace('    by', '').strip()
    else:
        brand = 'Missing'
    brand_name_2.append(brand)
    prod_name_2, star_2, review_count_2, total_recommend_2, love_count_2 = [], [], [], [], []
    product2 = soup_2.find('a', {'data-hook': 'product-link'}).text.strip()
    prod_name_2.append(product2)
    ratt = soup_2.find('span', {'data-hook': 'rating-out-of-text'})
    rating2 = ratt.text.replace(' out of 5', '')
    star_2.append(rating2)
    review_count_2.append(j - 1)
    total_recommend_2.append('Missing')
    love_count_2.append('Missing')
    swatches, swatches_2 = [], []
    for swatch in soup_3.find_all('img', {'class': 'swatch-image inline-twister-manual-load'}):
        swatches.append(swatch['alt'])
    all_color = ', '.join(swatches)
    if len(swatches) > 0:
        all_colors = str(len(swatches)) + ': ' + all_color
    else:
        all_colors = '1: ' + product2
    swatches_2.append(all_colors)
    prod_info_2 = []
    abou2 = soup_3.find('div', {'id': 'featurebullets_feature_div'})
    if abou2 is not None:
        about2 = abou2.text.strip().replace('\n', ' ').replace('About this item', '')
        prod_info_2.append(about2)
    else:
        prod_info_2.append('Missing')
    prod_ingred_2, prod_howto_2 = [], []
    prod_ingred_2.append('Missing')
    prod_howto_2.append('Missing')

    info_row = {'Product Ref': prod_ref_2, 'Url': link_2, 'Brand': brand_name_2, 'Product': prod_name_2, 'Rating': star_2,
                'Review Count': review_count_2, 'How Many Recommended': total_recommend_2, 'Loves': love_count_2,
                'Variants': swatches_2, 'About': prod_info_2, 'Ingredients': prod_ingred_2, 'How to Use': prod_howto_2}
    amazon_info_df = pd.DataFrame(info_row)

    return amazon_review_df, amazon_info_df
