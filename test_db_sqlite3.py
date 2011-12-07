import db_sqlite3 as db_lib
import unittest

class TestSqlite3Functions(unittest.TestCase):

  #TODO doSearch, once properly implemented, and sanitize, once I work that out.

  def setUp(self):
    self.db = db_lib.db_sql3({'clean': True, 'location': 'test.db'})

  def test_addWord(self):
    pass
    #Test addWord function, and unique enforcement. and proper store.
    db = self.db

    db.addWord('word1')
    results = db.customQuery('select * from words').fetchall()
    self.assertEqual(results, [('word1',)])

    db.addWord('word1')
    results = db.customQuery('select * from words').fetchall()
    self.assertEqual(results, [('word1',)])

    db.addWord('word2')
    results = db.customQuery('select * from words order by rowid').fetchall()
    self.assertEqual(results, [('word1', ),('word2',)])

  def test_addPage(self):
    pass
    #Functionally identical to test_addWord
    db = self.db

    db.addPage('url1')
    results = db.customQuery('select url from pages').fetchall()
    self.assertEqual(results, [('url1',)])

    db.addPage('url1')
    results = db.customQuery('select url from pages').fetchall()
    self.assertEqual(results, [('url1',)])

    db.addPage('url2')
    results = db.customQuery('select url from pages order by rowid').fetchall()
    self.assertEqual(results, [('url1',), ('url2',)])


  def test_addLink(self):
    pass
    #Test basic addLink functionality, and composite primary key values
    db = self.db

    db.addPage('url1')
    db.addPage('url2')
    db.addPage('url3')
    db.addPage('url4')

    db.addLink('url1', 'url2')
    results = db.customQuery('select parent, child from links order by rowid').fetchall()
    self.assertEqual(results, [(1,2)])

    db.addLink('url1', 'url2')
    results = db.customQuery('select parent, child from links order by rowid').fetchall()
    self.assertEqual(results, [(1,2)])
    
    db.addLink('url1', 'url3')
    results = db.customQuery('select parent, child from links order by rowid').fetchall()
    self.assertEqual(results, [(1,2),(1,3)])

    db.addLink('url3', 'url4')
    results = db.customQuery('select parent, child from links order by rowid').fetchall()
    self.assertEqual(results, [(1,2),(1,3),(3,4)])


  def test_Index(self):
    #Test addIndex, getAllIndices
    db = self.db

    db.addWord('word1')
    db.addWord('word2')
    db.addPage('url1')
    db.addPage('url2')

    db.addIndex('word1', 'url1', 1)
    results = db.customQuery('select word_id, url_id, size, count from indices order by rowid').fetchall()
    self.assertEqual(results, [(1, 1, 1, 1)])

    db.addIndex('word1', 'url1', 1)
    results = db.customQuery('select word_id, url_id, size, count from indices order by rowid').fetchall()
    self.assertEqual(results, [(1, 1, 1, 2)])
    
    #Last two queries should be identical

    db.addIndex('word2', 'url2', 1)
    results = db.customQuery('select word_id, url_id, size, count from indices order by rowid').fetchall()
    self.assertEqual(results, [(1, 1, 1, 2), (2, 2, 1, 1)])

    
    results = db.getAllIndices()
    self.assertEqual(results, [(1, 1, 1, 2), (2, 2, 1, 1)])

    def test_updateRank(self):
      #Tests update rank.
      db = self.db

      db.addPage('url1')

      db.updateRank('url1', 5)
      results = db.customQuery('select url, rank from pages').fetchall()
      self.assertEqual(results, [(1, 1, 5)])



if __name__ == '__main__' :
  unittest.main()