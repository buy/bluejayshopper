import urllib2
import re
import sys

reload(sys)
type = sys.getfilesystemencoding()
sys.setdefaultencoding(type)

from product import product
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)

def getPrice(search):  
  # testing output
  # file = open('bestbuy.html', 'w')
  
  # result product list for return
  pList = []

  # Bestbuy's search URL
  searchURL = 'http://www.bestbuy.com/site/searchpage.jsp?_dyncharset=ISO-8859-1&_dynSessConf=ATG12474449190&id=pcat17071&type=page&sc=Global&cp=1&nrp=15&sp=&qp=&list=n&iht=y&usc=All+Categories&ks=960&saas=saas&st=%s' % search
  
  bestbuy = urllib2.urlopen(searchURL)
  # Get the content and eliminate the \n so we can use regex
  bestbuy_content = bestbuy.read().replace('\n', '')
  
  # find all the product divs and store in a list
  items = re.findall(r'\<div class="hproduct"(.*?)itemprop="description"', bestbuy_content) 
  # For each product, we build out product object
  for i in range(len(items)):
    item = items[i]
    p = product()
    # print i
    # print item
    url = re.findall(r'\<a.*?rel="product" href="(.*?)"', item)
    if len(url) > 0:
      url = url[0]
      p.url = 'http://www.bestbuy.com' + url
      # p.url = p.url.encode('utf8')
    
    name = re.findall(r'\<h3.*\>\<a.*?rel="product".*?\>(.*?)\</a\>', item)
    if len(name) > 0:
      name = name[0]
      p.name = name
    
    price = re.findall(r'\<h4 class="price sale"\>.*?\$([,0-9\.]+).*?\</h4\>', item)
    if len(price) > 0:
      price = price[0]
      p.price = float(filter(lambda x : x not in ',', price))
    else:
      p.price = None
    
    model = re.findall(r'\<strong itemprop="model"\>(.*?)\</strong\>', item)
    if len(model) > 0:
      p.model = model[0]
    # build our product object
    # print name
    # print price
    
    p.source = '/images/bestbuy-logo.jpg'
    
    # Get the product photo
    imgurl = re.findall(r'\<img itemprop="image".*?src="(.*?)"', item)
    if len(imgurl) > 0:
      imgurl = imgurl[0]
      p.imgurl = imgurl
    else:
      p.imgurl = p.source
    
    # add to list
    pList.append(p)
    
    # html = '<li><a href="' + p.url + '">' + p.name + '</a><br>' + p.price + '<br>' + p.model + '</li>'
    # file.write(html)
    # print p.name, '\n'
    # print p.url, '\n'
    # print p.price, '\n'
    # print '\n'
  # print bestbuy_content

  # file.write(bestbuy_content)
  # file.close()
  bestbuy.close()
  return pList
  
if __name__ == '__main__':
  getPrice('kindle')