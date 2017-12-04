import unittest
from bs4 import BeautifulSoup

#import bs4.element as el

##Not necessary
#pe = el.PageElement()
#pe.setup()

#Creates two tags using BS, note that im using BS tags to test BS tags.
#Maybe change this?
#tag1 = el.Tag(attrs = (({"id": "first_hr"})), name="hr")
#tag2 = el.Tag(attrs = (({"id": "second_hr"})), name="hr")


#find_all_previous()
#find_previous()

#find_parents()
#find_parent()

#a_tag = el.Tag(name ="bla") 


class TestBS(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		#Sets up various soups for tests

		cls.soup = BeautifulSoup("", "html.parser")


		#How to get soupify html files:
		cls.html_file = open("html_testfiles/html_test.html")
		cls.html_file_soup = BeautifulSoup(cls.html_file, "html.parser")

		#Directly defined soups.
		
		#Removed single tags.
		#THIS IS A BAD IDEA, BS DOESNT HANDLE SINGLETON TAGS WITHOUT THE XML PARSER!!
		
		cls.a_simple_soup = BeautifulSoup(
		'''
		<html>
			<head>
			</head>
		<body>
			<p>
				<a>An anchor tag</a>
			</p>
		</body>
		</html>
                ''', "html.parser")

		cls.a_nested_soup = BeautifulSoup(
		'''
		<html>
			<head>
			</head>
		<body>
			<p id = "p_lvl1">
				<p id = "p_lvl2">
					<p id = "p_lvl3">
						<p id = "p_lvl4">
							<a>First anchor tag</a>
							<a>Second anchor tag</a>
							<a>Third anchor tag</a>
						</p>
					</p>
				</p>
			</p>
		</body>
		</html>
		''', "html.parser")

		cls.css_select_soup = BeautifulSoup(
		'''
		<html>
			<head>
			</head>
		<body>
			<p class = "my_CSS_class">Here is my styled paragraph</p>
			<a id = "my_link"></a>
		</body>
		</html>
		''', "html.parser")


		cls.wrap_soup = BeautifulSoup(
		'''
		<p>Text to be wrapped</p>
		''', "html.parser")




		##Directly defined tags, to compare with BS output.

		#a generic anchor tag
		cls.a_tag = cls.soup.new_tag("a") 
		cls.a_tag.string = "An anchor tag"

		#First, second, third anchor
		cls.a_tag_first = cls.soup.new_tag("a") 
		cls.a_tag_first.string = "First anchor tag"

		cls.a_tag_second = cls.soup.new_tag("a") 
		cls.a_tag_second.string = "Second anchor tag"

		cls.a_tag_third = cls.soup.new_tag("a") 
		cls.a_tag_third.string = "Third anchor tag"

		#a-tag with id
		cls.a_tag_id = cls.soup.new_tag("a", id="my_link") 

		#p-tag with class attribute
		cls.p_tag_css = cls.soup.new_tag("p", **{'class':'my_CSS_class'})
		cls.p_tag_css.string = "Here is my styled paragraph"

		#wrapped tag
		cls.p_tag_wrapped = BeautifulSoup("<tag><p>Text to be wrapped</p></tag>", "html.parser").tag

		#tag with no name
		cls.no_name_tag = cls.soup.new_tag("") 

	def test_no_name_tag(self):
		self.assertEqual(self.no_name_tag.name, "")


	def test_find(self):
		'''Find the first anchor tag, DOESN'T return a list '''
		self.assertEqual(self.a_simple_soup.find("a"), self.a_tag)
		self.assertEqual(self.a_simple_soup.p.find("a"), self.a_tag)
		self.assertEqual(self.a_nested_soup.find("a"), self.a_tag_first)
		self.assertEqual(self.a_nested_soup.find(""), self.a_nested_soup.html) #finds everything

	def test_find_fail(self):
		self.assertEqual(self.a_nested_soup.find("b"), None)
		
	def test_find_all(self):
		'''Find all tags, returns a list'''
		self.assertEqual(self.a_nested_soup.find_all("a"), [self.a_tag_first,self.a_tag_second,self.a_tag_third])

	def test_find_all_not_found(self):
		'''Search for non-existing tags'''
		self.assertEqual(self.a_nested_soup.find_all("b"), []) 
		self.assertEqual(self.a_nested_soup.find_all(""), [])  #finds nothing

	def test_css_select(self):
		'''Find tags based on CSS selectors, returns a list'''
		self.assertEqual(self.css_select_soup.select(".my_CSS_class"), [self.p_tag_css])
		self.assertEqual(self.css_select_soup.select("a#my_link"), [self.a_tag_id])
		self.assertEqual(self.css_select_soup.select('a[id="my_link"]'), [self.a_tag_id])
		self.assertEqual(self.css_select_soup.select('#my_link'), [self.a_tag_id])
		self.assertEqual(self.css_select_soup.select('a[id~="my_link"]'), [self.a_tag_id])
		#self.assertEqual(self.css_select_soup.select(""), None)  #simply crashes.

	def test_wrap(self):
		'''Return the wrapped tag'''
		self.assertEqual(self.wrap_soup.p.wrap(self.soup.new_tag("tag")), self.p_tag_wrapped)

	def test_find_next(self):
		'''Use find_next to find the next anchor tag, until there are no more'''
		self.first_link = self.a_nested_soup.a
		self.second_link = self.first_link.find_next()
		self.third_link = self.second_link.find_next()
		self.assertEqual(self.a_nested_soup.a, self.a_tag_first)
		self.assertEqual(self.first_link.find_next(), self.a_tag_second)
		self.assertEqual(self.second_link.find_next(), self.a_tag_third)
		self.assertEqual(self.third_link.find_next(), None)

	def test_find_all_next(self):
		'''Find all following tags using two differente usages of find_all_next'''
		self.next_tags = [self.a_tag_second, self.a_tag_third]
		self.first_link = self.a_nested_soup.a
		self.assertEqual(self.first_link.find_all_next(), self.next_tags)
		self.assertEqual(self.first_link.find_all_next("a"), self.next_tags)
		self.assertEqual(self.first_link.find_all_next("b"), [])
    
	def test_find_previous(self):
		self.assertEqual(self.a_simple_soup.a.find_previous("p"), self.a_simple_soup.p)

	def test_find_all_previous(self):
		self.assertEqual(self.a_simple_soup.a.find_all_previous("p"), [self.a_simple_soup.p])

	def test_find_parent(self):
		self.assertEqual(self.a_nested_soup.a.find_parent("p"), self.a_nested_soup.find("p", id = "p_lvl4"))
		self.assertEqual(self.a_nested_soup.p.p.p.p.find_parent("p"), self.a_nested_soup.p.p.p)

	def test_find_parents(self):
		p_lvl1 = self.a_nested_soup.find("p", id = "p_lvl1")
		p_lvl2 = self.a_nested_soup.find("p", id = "p_lvl2")
		p_lvl3 = self.a_nested_soup.find("p", id = "p_lvl3")
		p_lvl4 = self.a_nested_soup.find("p", id = "p_lvl4")
		self.assertEqual(self.a_nested_soup.a.find_parents("p"), [p_lvl4, p_lvl3, p_lvl2, p_lvl1])
		self.assertEqual(self.a_nested_soup.p.find_parents("body"), [self.a_nested_soup.body])


if __name__ == '__main__':
	unittest.main()

