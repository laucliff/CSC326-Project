import sqlite3

class sql3:

  def __init__(self, params):

    #For performance reasons, db functions will blindly assume that the connection is open, instead of open/closing every time an operation is required.
    if 'location' in params:
      self.open_db(params['location'])
    else:
      self.open_db('default.db')

    #Check if {clean: true} is provided as a param.
    if 'clean' in params and params['clean']:
      #reset tables.
      self.c.execute('''DROP TABLE IF EXISTS words''')
      self.c.execute('''DROP TABLE IF EXISTS pages''')
      self.c.execute('''DROP TABLE IF EXISTS links''')
      self.c.execute('''DROP TABLE IF EXISTS indices''')
      #I am not sure if the commit here is necessary, but I want to ensure that all the drops are performed before recreating the tables.
      self.conn.commit()
      #create tables
      self.c.execute('''CREATE TABLE words (word TEXT UNIQUE);''')  
      self.c.execute('''CREATE TABLE pages (url TEXT UNIQUE, rank INTEGER DEFAULT 0);''')
      self.c.execute('''CREATE TABLE links (parent INTEGER, child INTEGER, PRIMARY KEY(parent, child));''')
      self.c.execute('''CREATE TABLE indices (word_id INTEGER, url_id INTEGER, size INTEGER, count INTEGER DEFAULT 0, PRIMARY KEY(word_id, url_id, size));''')
      self.conn.commit()

  def open_db(self, db_location):
    self.conn = sqlite3.connect(db_location)
    self.conn.text_factory = str
    self.c = self.conn.cursor()

  def close_db(self):
    self.c.close()
    self.conn.close()

  def addWord(self, word):
    self.c.execute('''INSERT OR IGNORE INTO words (word) VALUES (?);''', (word,))
    self.conn.commit()

  def addPage(self, url):
    self.c.execute('''INSERT OR IGNORE INTO pages (url) VALUES (?);''', (url,))
    self.conn.commit()

  def addLink(self, parent, child):
    #python suggest we use the ? replacement instead of normal string formatting in order to prevent sql injection attacks. However, it does not seem to support key value linking like normal string formatting. As a result, some of the string substitution can be a bit messy.
    #pull both rowid values from page table
    self.c.execute('''SELECT rowid FROM pages WHERE url=?;''', (parent,))
    parent_id = next(iter(self.c.fetchone()))
    self.c.execute('''SELECT rowid FROM pages WHERE url=?;''', (child,))
    child_id = next(iter(self.c.fetchone()))

    #insert rowid values into link table
    self.c.execute('''INSERT OR IGNORE INTO links (parent, child) VALUES (?,?);''', (parent_id, child_id))
    self.conn.commit()

  def addIndex(self, word, url, size):
    #sqlite3 lacks a proper insert or update on conflict query, so we have to do his messy setup instead.
    #if index exists, increment count value.

    #pull rowid values from page and word tables
    self.c.execute('''SELECT rowid FROM words WHERE word=?;''', (word,))
    word_id = next(iter(self.c.fetchone()))
    self.c.execute('''SELECT rowid FROM pages WHERE url=?;''', (url,))
    url_id = next(iter(self.c.fetchone()))

    #insert relevant id values into indices table. This entry will not go through if an existing index is in place.
    self.c.execute('''INSERT OR IGNORE INTO indices (word_id, url_id, size) VALUES (?,?,?);''', (word_id, url_id, size))
    self.conn.commit()
    #force an update to set count to 1, or increment if existing.
    self.c.execute('''UPDATE indices set count = count+1 WHERE word_id = ? AND url_id = ?''', (word_id, url_id))
    self.conn.commit()

  def doSearch(word):
    #pull rowid from words table
    self.c.execute('''SELECT rowid from words WHERE word=?;''', (word,))
    word_id = next(iter(self.c.fetchone()))

    #This query should only pull unique words from the index list, sorted by 
    self.c.execute('''SELECT DISTINCT url FROM indices LEFT JOIN words ON words.rowid = indices.word_id LEFT JOIN pages on pages.rowid = indices.url_id WHERE word_id = ? ORDER BY rank''', (word_id,))
    return self.c

  def getAllIndices(self):
    #Simple select all query.
    self.c.execute('''SELECT * FROM indices order by rowid;''')
    return self.c.fetchall()

  def updatePageRank(self,url, rank):
    #Just updates pagerank given url.
    self.c.execute('''SELECT rowid FROM pages WHERE url=?;''', (parent,))
    url_id = next(iter(self.c.fetchone()))

    self.c.execute('''UPDATE pages SET rank = ? WHERE url like '?';''', (rank, url_id))
    self.conn.commit()

  def customQuery(self,query):
    #For direct query execution. Returns the raw cursor object. Mostly used for testing.
    self.c.execute(query)
    self.conn.commit()
    return self.c
