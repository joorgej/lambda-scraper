import requests
from lxml import html as parser
import random

req = requests.Session()
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
user_agent = random.choice(user_agent_list)
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": user_agent,
}
req.headers = headers

def getSearchURL(search, page):
    baseURL = 'https://www.amazon.com/s?k={}&s=review-rank&page={}&language=es'
    search = search.replace(' ','+')
    return baseURL.format(search, page)

def getProductData(product_list):
    
    products = []
    for product in product_list:
        data = {}
        asin = product.get('data-asin')
        data['ASIN'] = asin
        
        img_list = product.xpath('//div[@data-asin="'+asin+'"]/div/span/div/div/div[2]/div[1]/div/div/span/a/div/img')
        if len(img_list)==0:
            continue
        data['IMG'] = img_list[0].get('src')
        
        price_list = product.xpath('//div[@data-asin="'+asin+'"]/div/span/div/div/div[2]/div[2]/div/div/div[3]/div[1]/div/div[1]/div/a/span/span[2]')
        if len(price_list)==0:
            continue
        data['PRICE'] = price_list[0].text_content()
        
        title_list = product.xpath('//div[@data-asin="'+asin+'"]/div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a/span/text()')
        if len(title_list)==0:
            continue
        data['TITLE'] = title_list[0]

        products += [data]
    return products

def getAllProducts(min_products, search):
    page = 0
    product_list = []
    while len(product_list)<min_products:
        page += 1
        url = getSearchURL(search, str(page))
        res = req.get(url)
        data = res.content
        html = parser.fromstring(data)
        products = html.xpath('//div[@data-asin]')
        product_list += getProductData(products)
        print(len(product_list))

    return product_list




if __name__ == '__main__':

    
    for product in products:
        print('---------------------------------------------')
        print('ASIM:    '+product['ASIN'])
        print('IMAGEN:  '+product['IMG'])
        print('TITLE:   '+product['TITLE'])
        print('PRICE:   '+product['PRICE'])

    
import json

def lambda_handler(event, context):
    search = event.get('search')
    count = event.get('count')

    products = getAllProducts(count, search)

    return {
        'statusCode': 200,
        'products': products
    } 
        
        
        
    

    #first_image = asin_data[3].xpath('//span[@data-component-type="s-product-image"]').xpath('//a')



    
