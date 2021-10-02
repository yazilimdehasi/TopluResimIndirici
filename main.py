import requests
from bs4 import BeautifulSoup
from urllib import request as ulreq
from PIL import ImageFile
import ssl
from tqdm import tqdm

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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img')
    image_urls = [tag['src'] for tag in image_tags]
    return image_urls


if __name__ == "__main__":
    import os
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
