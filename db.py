# words, indices, pages, links

def open():

def close():

def addWord(word):
  #insert if not exists word into words

def addPage(url):
  #insert if not exists url into pages

def addLink(parent, child):
  #addPage(parent)
  #addPage(child)
  #insert if not exists (parent, child) into links
  #insert select...

def addIndex(word, url):
  #addWord(word)
  #addPage(url)
  #insert select (id from words where word like 'word', id from pages where url like 'url')

def doSearch(query):

def getAllIndices():
  #select * from indices

def updatePageRank(url, rank):
  #update table pages set rank = rank where url = url
