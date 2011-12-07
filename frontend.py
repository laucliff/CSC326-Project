from lib.bottle import *


#todo
#html template
#

@route('/', method='GET')
def searchPage():
  t = request.GET.get('query', '').strip()
  print t
  if t: 
    print 'true' 
  else: 
    print 'false'
  s = template('main')
  return s

run()