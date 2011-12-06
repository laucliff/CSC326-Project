import db_sqlite3
import unittest

class TestSqlite3Functions(unittest.TestCase):

  addWord = ('word1', 'word2', 'word1', 'word1')
  addWordAnswer = set('word1', 'word2') 

  db = db_sqlite3({'clean': True, 'location': 'testdb'})

  for word in addWord:
    db.addWord(addWord)
  
  db.customQuery('select * from words')
  
