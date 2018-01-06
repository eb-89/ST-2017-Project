## File for white box testing of the BS4 web scraping library.
## This code provides full branch coverage of the functions find and find_all
## as well as the internal function _find_all


## Erik Bertse
## Sara Gustavsson
## Moa Marklund 
## Henrik Thorsell

## Software Testing, 5c
## Autumn 2017 
## Uppsala University


import unittest
import itertools
from bs4 import BeautifulSoup
from bs4 import SoupStrainer


## WARNING ## This is a badly written iterator, specifically for breaking _find_all ###
## DONT USE THIS CODE IF YOU NEED AN ITERATOR 
class EvilIter():
  def __init__(self,breaker):
    self.current = breaker
  
  def __iter__(self):
    return self

  def next(self):
    if self.current == 0:
      raise StopIteration
    else:
      self.current = self.current - 1
      return self

  def  __len__(self):
    return 0


class TestBS(unittest.TestCase):

  def test_soup_branch(self):

    self.a_simple_soup = BeautifulSoup(
    '''
    <html>
      <head>
      </head>
    <body>
      <p>
        <a href="http://example.com"><b>A bold anchor tag</b></a>
      </p>
    </body>
    </html>
                ''', "html.parser")

    self.tiny_soup = BeautifulSoup(
    '''
    <html></html>
                ''', "html.parser")
    
    a_tag = self.a_simple_soup.a
    
    #Here we call find directly
    tag = self.a_simple_soup.find("a")
    self.assertEqual(tag, a_tag)

    #Here we call find all directly
    tag = self.a_simple_soup.find_all("a")
    self.assertEqual(tag, [a_tag])

    #Here we call find all directly, with no argument
    html = self.a_simple_soup.html
    head = self.a_simple_soup.head
    body = self.a_simple_soup.body
    p = self.a_simple_soup.p
    a = self.a_simple_soup.a
    b = self.a_simple_soup.b

    tag = self.a_simple_soup.find_all()
    self.assertEqual(tag, [html, head, body, p, a, b])

    #here kwarg contains "string", and there is no text argument.
    tag = self.a_simple_soup.find_all(string = "a")
    self.assertEqual(tag, [])

    #here we define a custom SoupStrainer
    strainer = SoupStrainer("a")
    tag = self.a_simple_soup.find_all(strainer)
    self.assertEqual(tag, [a_tag])

    #here we find with limit
    tag = self.a_simple_soup.find_all("a", limit = 1)
    self.assertEqual(tag, [a_tag])

    #Putting recursive to False makes BS only look one level down from the 
    #tag from which the search started.
    tag = self.tiny_soup.find_all("a", recursive = False)
    self.assertEqual(tag, [])

    #This is far outside of normal BS usage
    iterator = EvilIter(3)
    tag = self.tiny_soup._find_all("a", None, None, None, recursive = False, generator = iterator)
    self.assertEqual(tag, [])

if __name__ == '__main__':
  unittest.main()