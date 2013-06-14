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
  searchURL = 'http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&N=-1&isNodeId=1&Description='+ str(search) +'&x=-852&y=-112'
  newegg = urllib2.urlopen(searchURL)
  newegg_content = newegg.read().replace('\n','')
  newegg_content = newegg_content.replace('\t','')
  
  # file = open('newegg.html', 'w')
  # file.write(newegg_content)

  modelList = []
  items = re.findall(r'\<div class="itemCell"(.*?)\<br class="clear"', newegg_content)
  for item in items:
    p = product()
    #print item + '\n'
    url = re.findall(r'\<a href="(.*?)"',item)
    if len(url) > 0:
      p.url = url[0]
      # p.url = p.url.encode('utf8')

    name = re.findall(r'\<span class="itemDescription" id="titleDescription.*?\>(.*?)</span>',item)
    if len(name) > 0:
      p.name = name[0]
      
    price = re.findall(r'\<input type="hidden" name="priceBefore" value="\$([,0-9\.]+?)"',item)
    if len(price) > 0:
      p.price = float(filter(lambda x : x not in ',', price[0]))
    else:
      p.price = None

    p.source = '/images/newegg-logo.jpg'
    
    # Get the product photo
    imgurl = re.findall(r'\<div class="itemGraphics"\>.*?src="(.*?)"', item)
    if len(imgurl) > 0:
      imgurl = imgurl[0]
      p.imgurl = imgurl
    else:
      p.imgurl = p.source
      
    modelList.append(p)
    # html = '<li><a href="' + p.url + '">' + p.name + '</a><br>' + p.price + '<br>Newegg</li>'
    # file.write(html)
  # file.close()
  newegg.close()
  return modelList

if __name__ == '__main__':
  getPrice('ipad+mini+16gb')