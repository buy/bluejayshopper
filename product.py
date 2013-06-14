class product(object):
  def __init__(self, name=None, price=None, url=None, imgurl=None, model=None, source=None):
    self.name = name
    self.price = price
    self.lowprice = None
    self.url = url
    self.imgurl = imgurl
    self.model = model
    self.source = source
    self.count = 0
    