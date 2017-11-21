import unittest
import bs_func
from bs4 import BeautifulSoup as bs
import bs4.element as el

##Not necessary
pe = el.PageElement()
pe.setup()

#Creates two tags using BS, note that im using BS tags to test BS tags.
#Maybe change this?
tag1 = el.Tag(attrs = (({"id": "first_hr"})), name="hr")
tag2 = el.Tag(attrs = (({"id": "second_hr"})), name="hr")

a_tag = el.Tag(name ="a") 


class TestBS(unittest.TestCase):


	def test_find_all(self):
		output = bs_func.bs_find_all("hr")
		self.assertEqual(output, [tag1, tag2])
		
	def test_find_first(self):
		output = bs_func.bs_find_first_a()
		self.assertEqual(output, a_tag)


if __name__ == '__main__':
	unittest.main()

