import sqlite3

class db_sql3:

  def ___init___(params):

    #For performance reasons, db functions will blindly assume that the connection is open, instead of open/closing every time an operation is required.
    if 'location' in params:
      open(params['location'])
    else:
      open()

    #Check if {clean: true} is provided as a param.
    if 'clean' in params and params['clean']:
      #reset tables.
      c.execute('''DROP TABLE IF EXISTS words''')
      c.execute('''DROP TABLE IF EXISTS pages''')
      c.execute('''DROP TABLE IF EXISTS links''')
      c.execute('''DROP TABLE IF EXISTS indices''')
      #I am not sure if the commit here is necessary, but I want to ensure that all the drops are performed before recreating the tables.
      c.commit
      #create tables
      c.execute('''CREATE TABLE words (word TEXT UNIQUE;''')
      c.execute('''CREATE TABLE pages (url TEXT UNIQUE, rank INTEGER);''')
      c.execute('''CREATE TABLE links (parent INTEGER, child INTEGER, PRIMARY KEY(parent, child));''')
      c.execute('''CREATE TABLE indices (word_id INTEGER, url_id INTEGER, size INTEGER, count INTEGER DEFAULT 0, PRIMARY KEY(word_id, url_id, size));''')
      c.commit()

  def open(self, db_location = 'database'):
    self.conn = sqlite3.connect(db_location)
    self.c = conn.cursor()

  def close():
    c.close()
    conn.close()

  def addWord(word):
    #INSERT OR IGNORE INTO words VALUES (word);
    c.execute('''INSERT OR IGNORE INTO words VALUES (?);''', word)
    conn.commit()

  def addPage(url):
    #INSERT OR IGNORE INTO pages VALUES (url);
    c.execute('''INSERT OR IGNORE INTO pages VALUES (?);''', url)
    conn.commit()

  def addLink(parent, child):
    #INSERT OR IGNORE INTO links VALUES (parent, child);
    #python suggest we use the ? replacement instead of normal string formatting in order to prevent sql injection attacks. However, it does not seem to support key value linking like normal string formatting. As a result, some of the string substitution can be a bit messy.
    #query = 'INSERT OR IGNORE INTO links VALUES (%(parent)s, %(child)s);' % {'parent':parent, 'child':child}
    c.execute('''INSERT OR IGNORE INTO links VALUES (?,?);''', (parent, child))
    conn.commit()

  def addIndex(word, url, size):
    #sqlite3 lacks a proper insert or update on conflict query, so we have to do his messy setup instead.
    #if index exists, increment count value.
    #insert or update into indices select words.rowid, pages.rowid from words left join pages where words like 'word' and url like 'url';
    c.execute('''SELECT rowid FROM words WHERE word LIKE '?';''', word)
    word_id = c
    c.execute('''SELECT rowid FROM pages WHERE url LIKE '?';''', url)
    url_id = c



    c.execute('''INSERT OR IGNORE INTO indices (word_id, url_id, size) VALUES (?, ?, ?);''', (word_id, url_id, size))
    c.commit()
    c.execute('''UPDATE indices set count = count+1 WHERE word_id = ? AND url_id = ?''', (word_id, url_id))
    c.commit()

  def doSearch(word):
    c.execute('''SELECT word_id, url_id, size, count FROM indices WHERE word like '?';''', word)
    return c

  def getAllIndices():
    #SELECT * FROM indices
    c.execute('''SELECT * FROM indices;''')
    return c

  def updatePageRank(url, rank):
    #update table pages set rank = rank where url = url
    #UPDATE pages SET rank = rank WHERE url = url;
    #query = 'UPDATE pages SET rank = %(rank)s WHERE url = %(url)s;' % {'rank':rank, 'url':url}
    c.execute('''UPDATE pages SET rank = ? WHERE url like '?';''', (rank, url))
    c.commit()

  def customQuery(query):
    #For direct query execution
    c.execute('''?''', query)
    c.commit()
    return c

  def sanitize(query):
    return
    #sanitize the input to prevent syntax errors/injection attacks