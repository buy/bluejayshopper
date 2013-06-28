import cgi
import webapp2
#import md5
import re
import sys

# self defined module
import bestbuy
import amazon
import newegg

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
urlfetch.set_default_fetch_deadline(35)


MAIN_PAGE_HTML = """\
<html>
  <head>
		<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="http://ajax.aspnetcdn.com/ajax/jquery.validate/1.11.1/jquery.validate.min.js"></script>
    <script type="text/javascript" src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <script type="text/javascript" src="/scripts/main.js"></script>
		<title>Jay Shopper</title>
	</head>
  <body>
    <div class="body-content">
      <div class="functionBox">
        <form action="/result" method="get">
          <div id="logo-img">
            <img id="logo" src="/images/logo.jpg" />
          </div>
          <div id="input-search"><input class="search" id="search2" type="text" name="product" value="ipad mini 16GB" style="color: #aaa"></div>
          <div id="submit-button"><input class="button orange" type="submit" value="Get My Deals"></div>
        </form>
      </div>
      <div class="divbox dealrank">
        Introducing the DealRank algorithm<br>Where the best deals are always on TOP!
      </div>
      <div class="dealrankInfo">
        <div class="dealrankIntro textCenter">
          <h1>The NEW DealRank</h1>
            <p>
              With deals in mind, we provide the best way to get what you want!<br />Our DealRank algorithm will get you the best price for the product you search!
            </p>
          <h2>Very Simple Rules</h2>
          <img class="redBlueSample" src="/images/dealrank.jpg" /><br /><br />
          <span class="price bold red">Red is bad price</span><br />
          <span class="price bold blue">Blue is normal price</span><br />
          <span class="price bold green">Green is REDUCED price!</span><br />
        </div>
        <div class="divbox backMain">
          Go Back
        </div>
      </div>
    </div>
  </body>
  <script language="javascript">
    var s=document.getElementById("search2");
    s.onfocus=function(){if(this.value==this.defaultValue)this.value=''};
    s.onblur=function (){if(/^\s*$/.test(this.value)){this.value=this.defaultValue;this.style.color='#aaa'}}
    s.onkeydown=function(){	this.style.color='#333'}
  </script>
</html>
"""

RESULT_PAGE_HTML_HEAD = """\
<html>
  <head>
		<link type="text/css" rel="stylesheet" href="/stylesheets/results.css" />
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script type="text/javascript" src="http://ajax.aspnetcdn.com/ajax/jquery.validate/1.11.1/jquery.validate.min.js"></script>
    <script type="text/javascript" src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <script type="text/javascript" src="/scripts/resultpage.js"></script>
		<title>Shopper Result</title>
	</head>
  <body>
    <div class="search-box">
      <form action="/result" method="get">
        <div class="function-box">
          <div id="input-search"><input class="search" id="search2" type="text" name="product" value="ipad mini 16GB" style="color: #aaa"></div>
          <div id="submit-button"><input class="button orange" type="submit" value="Get My Deals"></div>
        </div>
      </form>
    </div>
    <div class="slide">Click here to search another product</div>
    <div id="content">
      <table class="result-table" cellspacing="0">
      <tr><th>Product Name</th><th>Product Photo</th><th>Current Price</th><th>History Lowest Price</th><th>Click to Buy</th></tr>
"""      
RESULT_PAGE_HTML_FOOT = """\
      </table>
      <br><br><br>
    </div>
  </body>
  <script language="javascript">
    var s=document.getElementById("search2");
    s.onfocus=function(){if(this.value==this.defaultValue)this.value=''};
    s.onblur=function (){if(/^\s*$/.test(this.value)){this.value=this.defaultValue;this.style.color='#aaa'}}
    s.onkeydown=function(){	this.style.color='#333'}
  </script>
</html>
"""

ERROR_500 = """\
  </table>
  </div>
  <div class="divbox"><br /><br />
    Ooops, looks like something is wrong!<br /><br />
    Don't blame me, try to reload the page or do another search :)<br /><br /><br />
  </div>
"""

### The index page
class MainPage(webapp2.RequestHandler):
  # GET request handler
  def get(self):
    self.response.write(MAIN_PAGE_HTML)

### The handler of the result display page 
class PriceFinder(webapp2.RequestHandler):
  # GET request handler
  def get(self):
    pList = []  # array to store all the fetched results
    search = self.request.get('product')
    search = '+'.join(search.split()) # Search keyword
    try:
      pList += bestbuy.getPrice(search) # Get the results from BestBuy
      pList += amazon.getPrice(search)  # Get the results from Amazon
      pList += newegg.getPrice(search)  # Get the results from Newegg
    except:
      self.response.write(RESULT_PAGE_HTML_HEAD)
      self.response.write(ERROR_500)
      self.response.write(RESULT_PAGE_HTML_FOOT)
      return
    
    pList.sort(key=lambda x: x.price) # Sort the list of products by their prices
    sortByCount(pList)  # Sort again and this time by click counts
    self.response.write(RESULT_PAGE_HTML_HEAD)
    
    laterOutput = [] # Store the normal price or bad price in the list for later output
    # Build the result display page
    for p in pList:
      p.lowprice = setLowPrice(p)
      priceClass = 'blue'
      moveTop = False # if we got a slick deal, display it on the top
      if p.lowprice < p.price:
        priceClass = 'red'
      if p.lowprice > p.price:
        priceClass = 'green'
        moveTop = True
      html = '<tr><td><a href="' + p.url + '">' + p.name + '</a></td><td class="imgbox"><a href="' + p.url + '"><img src="' + p.imgurl + '"></a></td><td><a class="bold price ' + priceClass + '" href="' + p.url + '">$' + str(p.price) + '</a></td><td><a class="price blue" href="' + p.url + '">$' + str(p.lowprice) + '</a></td><td><a href="' + p.url + '"><img class="merchantimg" src="' + p.source + '"></a></td>'
      if moveTop is True:
        self.response.write(html)
      else:
        laterOutput.append(html)
    # writeout the normal price
    for html in laterOutput:
      self.response.write(html)
    self.response.write(RESULT_PAGE_HTML_FOOT)

class History(ndb.Model):
  """Models an individual History click entry with url and count"""
  price = ndb.FloatProperty();
  count = ndb.IntegerProperty();
  date = ndb.DateTimeProperty(auto_now_add=True)

### This class is used to handle the click information gathered by jQuery  
class GetURL(webapp2.RequestHandler):
  # GET request handler
  def get(self):
    url = self.request.get('link')
    tmp = re.findall(r'(.*?)jsessionid.*?',url)
    if len(tmp)>0:
      url = tmp[0]
    #url = md5.md5(url).hexdigest()
    history_entity = History.get_by_id(url) # load the entity from datastore
    # if not, we creat a new instance and store it
    if history_entity is None:
      history_entity = History(id = url)
      history_entity.count = 1
      history_entity.put()
    # check if the entity is in the datastore
    else:
      history_entity.count += 1
      history_entity.put()

# get the GetURL key      
def geturl_key(geturl_name):
  return ndb.Key('GetURL', geturl_name)

def setLowPrice(p):
  price = 'N/A' # The price to return
  url = p.url
  # p.price = float(p.price)
  tmp = re.findall(r'(.*?)jsessionid.*?', url)
  if len(tmp)>0:
    url = tmp[0]
  history_entity = History.get_by_id(url)
  if history_entity is None:
    history_entity = History(id = url)
    history_entity.price = p.price
    history_entity.count = 0
    history_entity.put()
  else:
    price = history_entity.price
    if type(p.price) is type(1.1) and history_entity.price > p.price:
      history_entity.price = p.price
      history_entity.put()
  return price
  
# Sort the product list by its click count
def sortByCount(pList):
  for p in pList:
    #url = md5.md5(p.url).hexdigest()
    tmp = re.findall(r'(.*?)jsessionid.*?',p.url)
    #url = None
    e = None
    if len(tmp)>0:
      url = tmp[0]
      e = History.get_by_id(url)
    else:
      e = History.get_by_id(p.url)

    if e is not None:
      p.count = e.count
  
  pList.sort(key=lambda x: x.count, reverse=True)
 
# the entry function 
try:
  application = webapp2.WSGIApplication([
      ('/', MainPage),
      ('/result', PriceFinder),
      ('/click', GetURL),
  ], debug=False)
except:
  print "Unexpected error:", sys.exc_info()[0]