import urllib2
import re
import sys

reload(sys)
type = sys.getfilesystemencoding()
sys.setdefaultencoding(type)

from product import product
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(20)

def getPrice(search):
  searchURL = 'http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=' + str(search)
  #print searchURL
  try:
    amazon = urllib2.urlopen(searchURL)
  except:
    raise

  amazon_content = amazon.read().replace('\n', '')

  # file = open('amazon.html', 'w')
  # file.write(amazon_content)
  modelList = []
  items = re.findall(r'\<div class="result product"(.*?)\<br clear', amazon_content) 
  # print len(items)
  for i in range(len(items)):
    item = items[i]
    p = product()
    # print i+1
    #print item
    url = re.findall(r'\<div class="productTitle".*?href="(.*?)"\>', item)
    if len(url) > 0:
      url = url[0]
      p.url = url
      # p.url = p.url.encode('utf8')
      
    name = re.findall(r'\<div class="productTitle".*?href=".*?"\>(.*?)\</a\>', item)
    if len(name) > 0:
      name = name[0]
      p.name = name
    # print name
    price = re.findall(r'\<div class="newPrice"\>.*?\<span\>.*?\$([,0-9\.]+?)\</span\>', item)
    if len(price) > 0:
      price = price[0]
      p.price = float(filter(lambda x : x not in ',', price))
    else:
      price = re.findall(r'\<div class="subPrice"\>.*?\<span\>.*?\$([,0-9\.]+?)\</span\>', item)
      if len(price) > 0:
        price = price[0]
        p.price = float(filter(lambda x : x not in ',', price))
      else:
        p.price = None
    
    # print price
    #model = re.findall(r'\<strong itemprop="model"\>(.*?)\</strong\>', item)[0]
    p.source = '/images/amazon-logo.jpg'
    # Get the product photo
    imgurl = re.findall(r'\<div class="productImage".+?src="(.*?)"', item)
    if len(imgurl) > 0:
      imgurl = imgurl[0]
      p.imgurl = imgurl
    else:
      p.imgurl = p.source
    #p.model = model
    modelList.append(p)

    # html = '<li><a href="' + p.url + '">' + p.name + '</a><br>$' + str(p.price) + '<br>Amazon</li>'
    # file.write(html)
    # print p.name, '\n'
    # print p.url, '\n'
    # print p.price, '\n'
    # print '\n'
  # print amazon_content

  # file.write(amazon_content)
  # file.close()

  return modelList
  amazon.close()
  #return p.model

if __name__ == '__main__':
  getPrice('hard+drive')
