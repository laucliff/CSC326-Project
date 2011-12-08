from lib.bottle import *
import db_sqlite3 as db_lib


@route('/', method='GET')
def searchPage():
  query = request.GET.get('query', '').strip()
  print query
  if query: 
    db = db_lib.sql3()
    results = db.doSearch(query)
  else:
    results = None
  
  s = template('main', results=results)

  return s

run()