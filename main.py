import requests
from bs4 import BeautifulSoup
from urllib import request as ulreq
from PIL import ImageFile
import ssl
from tqdm import tqdm
import os

def getImageSize(url):
    try:
        """
        get file size *and* image size (None if not known)
        """ 
        context = ssl._create_unverified_context()
        file = ulreq.urlopen(url, context=context)
        size = file.headers.get("content-length")
        if size: 
            size = int(size)
        p = ImageFile.Parser()
        while True:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return size, p.image.size
                break
        file.close()
        return(size, None)
    except:
        return None, None

def downloadImage(url, name):
    """
    Download an image from a url.
    """
    img_data = requests.get(url).content
    with open('imgs/' + name + '.jpg', 'wb') as handler:
        handler.write(img_data)

def getImageUrls(url):
    """
    Get image urls from a webpage.
    """

    # User agent to validate that the request is made from the browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} 
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img')

    image_urls = []
    for image_tag in image_tags:

        # to ensure that it doesn't throw an error on links without src field
        try:
            image_urls.append(image_tag['src'])
        except KeyError as keyError:
            continue

    return image_urls


if __name__ == "__main__":
    if not os.path.exists('imgs'):
        os.makedirs('imgs')

    url = input("Enter the URL to download images from : ")

    images = getImageUrls(url)
    
    count = 1
    for i in tqdm(range(len(images))):
        image = images[i]
        try:
            fileSize, imageSize = getImageSize(image)
            if fileSize == None or imageSize == None or imageSize[0] < 200 or imageSize[1] < 200:
                continue
            else:
                downloadImage(image, str(count))
                count += 1
        except Exception as e:
            pass

    print("All images have been downloaded to imgs folder.")
