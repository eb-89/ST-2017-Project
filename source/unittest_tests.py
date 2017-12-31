## File for black box testing of the BS4 web scraping library.


## Erik Bertse
## Sara Gustavsson
## Moa Marklund 
## Henrik Thorsell

## Software Testing, 5c
## Autumn 2017 
## Uppsala University

import unittest
from bs4 import BeautifulSoup


class TestBS(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		#Sets up various soups for tests

		cls.soup = BeautifulSoup("", "html.parser")

                #How to get soupify html files: (this is not used in the tests below)
		#cls.html_file = open("html_testfiles/html_test.html")
		#cls.html_file_soup = BeautifulSoup(cls.html_file, "html.parser")

		
                #Directly defined soups.
		
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

		

		##Directly defined tags, to compare with BS output.

                #a generic anchor tag for append testing
                cls.an_append_tag = cls.soup.new_tag("a")
                cls.an_append_tag.string = "Foo"
                cls.an_appended_tag = cls.soup.new_tag("a")
                cls.an_appended_tag.string = "FooBar"

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

		#tag with no name
		cls.no_name_tag = cls.soup.new_tag("")

	

        def test_soup_contents(self):
                ''' Test the contents attribute, which returns the contents of a tag. 
                Note the line break elements
                A string should throw error on contents'''

                tags = ["\n", self.a_tag_first, "\n", self.a_tag_second, "\n", self.a_tag_third, "\n"]

                self.assertEqual(self.a_nested_soup.p.p.p.p.contents, tags)
                self.assertEqual(self.a_nested_soup.p.p.p.p.a.contents, [self.a_tag_first.string])

                with self.assertRaises(AttributeError):
                        self.assertEqual(self.a_nested_soup.p.p.p.p.a.string.contents, 0) 

        
        def test_soup_string(self):
                ''' Test the string attribute for finding the string in a tag '''
                
                markup = '<a>A tag string</a>'
                string = 'A tag string'
                string_soup = BeautifulSoup(markup, "html.parser")
                self.assertEqual(string_soup.a.string, string)

        def test_soup_stringless(self):
                ''' Test soup constructor for nonexisting string '''
                
                markup = "<a></a>"
                stringless_soup = BeautifulSoup(markup, "html.parser")
                self.assertEqual(stringless_soup.a.string, None)

        def test_soup_strings(self):
                ''' Test soup constructor for strings '''
                
                markup = '<html><head>String0</head><body>String1</body>String2</html>'
                soup = BeautifulSoup(markup, "html.parser")

                strings = ["String0", "String1", "String2"]

                soup_strings = []
                for string in soup.strings:
                        soup_strings.append(string)

                self.assertEqual(soup_strings, strings)

                with self.assertRaises(IndexError):
                        soup_strings[3]

        def test_soup_no_strings(self):
                '''Test soup constructor for strings without strings'''

                markup = '<html><head></head><body></body></html>'
                no_strings_soup = BeautifulSoup(markup, "html.parser")
                strings = []
                for string in no_strings_soup.strings:
                        strings.append(string)
                self.assertEqual(strings, [])


        def test_soup_head(self):
                ''' Test attribute navigation for head tag '''
                
                markup = '<html><head>head test</head><body><p>paragraph</p></body></html>'

                head_content_markup = ['head test']
                soup = BeautifulSoup(markup, "html.parser")
                
                head_tag = soup.new_tag("head")
                head_tag.string = "head test"
                
                self.assertEqual(soup.head, head_tag)
                self.assertEqual(soup.head.contents, head_tag.contents)

        def test_soup_headless(self):
                ''' Test attribute navigation without head tag '''
                
                markup = '<html><body><p>paragraph</p></body></html>'
                headless_soup = BeautifulSoup(markup, "html.parser")
                
                self.assertEqual(headless_soup.head, None)

        def test_soup_title(self):
                ''' Test attribute navigation for title tag '''
                
                markup = '<html><head><title>A title</title></head><body></body></html>'
                title_soup = BeautifulSoup(markup, "html.parser")

                title_tag = title_soup.new_tag("title")
                title_tag.string = 'A title'
                
                self.assertEqual(title_soup.title, title_tag)
                self.assertEqual(title_soup.title.string, title_tag.string)

        def test_soup_titleless(self):
                ''' Test attribute navigation for nonexisting title tag '''
                
                markup = '<html><head>asd</head><body>dsa</body></html>'
                title_soup = BeautifulSoup(markup, "html.parser")
                self.assertEqual(title_soup.title, None)
        
        
        def test_soup_children(self):
                ''' The children attribute returns a generator, for iterating over children
                Note that the children attribute returns linebreaks'''
                
                tags = ["\n", self.a_tag_first, "\n", self.a_tag_second, "\n", self.a_tag_third, "\n"]

                index = 0
                for c in self.a_nested_soup.p.p.p.p.children:
                        self.assertEqual(c, tags[index])
                        index += 1 


        def test_soup_descendants(self):
                ''' The descentants attribute returns the all descentants of a tag, including strings '''
               
                markup = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                soup = BeautifulSoup(markup, "html.parser")

                a1 = soup.new_tag("a")
                b1 = soup.new_tag("b")
                b1.string = "bold tag 1"

                b2 = soup.new_tag("b")
                b2.string = "bold tag 2"

                a1.append(b1)
                a1.append(b2)

                desc = [a1, b1, b1.string, b2, b2.string]

                index = 0
                for c in soup.descendants:
                         self.assertEqual(c, desc[index])
                         index += 1

        def test_soup_stripped_strings(self):
                ''' Test stripped_strings, which should remove whitespaces and linebreaks before and after strings '''
                
                markup = '''<html><head>
                             String0    
                         </head><body>   String1  </body> String2
                         </html>'''
                
                soup = BeautifulSoup(markup, "html.parser")

                strings = ["String0", "String1", "String2"]

                soup_strings = []
                for string in soup.stripped_strings:
                        soup_strings.append(string)

                self.assertEqual(strings, soup_strings)

                with self.assertRaises(IndexError):
                        strings[3]

        def test_soup_stripped_strings_empty(self):
                ''' Test stripping an soup with just whitespace'''

                markup = '''<a>     </a>   <a>   
                  </a>'''
                soup = BeautifulSoup(markup, "html.parser")

                strings = []
                for string in soup.stripped_strings:
                        strings.append(string)

                self.assertEqual(strings, [])

        def test_parent(self):
                '''Parent attribute finds the direct parent. This applies to strings as well.
                The parent of a soup is None'''

                markup = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                soup = BeautifulSoup(markup, "html.parser")

                self.assertEqual(soup.a.b.parent, soup.a)
                self.assertEqual(soup.a.parent, soup)
                self.assertEqual(soup.parent, None)

                self.assertEqual(soup.a.b.string.parent, soup.a.b)

        def test_parents(self):
                '''The parents attribute finds all parents of a given tag'''

                markup = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                soup = BeautifulSoup(markup, "html.parser")

                parents = [soup.a.b, soup.a, soup]

                ##Small irragularity here, parents does not go as high as None, although
                ##the documentation states that it should.

                index = 0
                for c in soup.a.b.string.parents:
                        self.assertEqual(c, parents[index])
                        index += 1
        
        def test_find(self):
		'''Find the first anchor tag, DOESN'T return a list '''
		
                self.assertEqual(self.a_simple_soup.find("a"), self.a_tag)
		self.assertEqual(self.a_simple_soup.p.find("a"), self.a_tag)
		self.assertEqual(self.a_nested_soup.find("a"), self.a_tag_first)
		self.assertEqual(self.a_nested_soup.find(""), self.a_nested_soup.html) #finds everything

	def test_find_fail(self):
                '''Test not finding a tag '''
		
                self.assertEqual(self.a_nested_soup.find("b"), None)
		
	def test_find_all(self):
		'''Find all tags, returns a list'''

                result = [self.a_tag_first,self.a_tag_second,self.a_tag_third]
		self.assertEqual(self.a_nested_soup.find_all("a"), result)

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
		self.assertEqual(self.css_select_soup.select(""), None)  

                #The last line crashes, gives IndexError


	def test_find_next(self):
		'''Use find_next to find the next anchor tag, until there are no more'''
		
                self.assertEqual(self.a_nested_soup.a, self.a_tag_first)
		self.assertEqual(self.a_nested_soup.a.find_next(), self.a_tag_second)
		self.assertEqual(self.a_nested_soup.a.find_next().find_next(), self.a_tag_third)
		self.assertEqual(self.a_nested_soup.a.find_next().find_next().find_next(), None)

	def test_find_all_next(self):
		'''Find all following tags using two different usages of find_all_next'''

		self.next_tags = [self.a_tag_second, self.a_tag_third]
		self.first_link = self.a_nested_soup.a
		
                self.assertEqual(self.first_link.find_all_next(), self.next_tags)
		self.assertEqual(self.first_link.find_all_next("a"), self.next_tags)
		self.assertEqual(self.first_link.find_all_next("b"), [])
    
	def test_find_previous(self):
                '''Finds the previous tag of a given name '''

		self.assertEqual(self.a_simple_soup.a.find_previous("html"), self.a_simple_soup.html)

	def test_find_all_previous(self):
                '''Finds all the previous tags of a given name '''

                result = [self.a_nested_soup.p.p.p.p, self.a_nested_soup.p.p.p ,self.a_nested_soup.p.p, self.a_nested_soup.p]
		self.assertEqual(self.a_nested_soup.a.find_all_previous("p"), result)

                '''find previous which is not parent '''
                self.assertEqual(self.a_nested_soup.a.find_all_previous("head"), [self.a_nested_soup.head])

	def test_find_parent(self):
                ''' Finds the parent of a given name'''

		self.assertEqual(self.a_nested_soup.a.find_parent("p"), self.a_nested_soup.p.p.p.p)
		self.assertEqual(self.a_nested_soup.p.p.p.p.find_parent("p"), self.a_nested_soup.p.p.p)


        
        def test_find_parents(self):
                '''Finds all the parents with a given name '''
                
                p_lvl1 = self.a_nested_soup.p
                p_lvl2 = self.a_nested_soup.p.p
                p_lvl3 = self.a_nested_soup.p.p.p
                p_lvl4 = self.a_nested_soup.p.p.p.p

                self.assertEqual(self.a_nested_soup.a.find_parents("p"), [p_lvl4, p_lvl3, p_lvl2, p_lvl1])
                self.assertEqual(self.a_nested_soup.p.find_parents("body"), [self.a_nested_soup.body])

        

        def test_append(self):
                ''' Test the append function by appending an <b>Bar</b> tag'''
                
                soup = BeautifulSoup("<a>Foo</a>", "html.parser")
                tag = soup.new_tag("b")
                tag.string = "Bar"

                soup.a.append(tag)

                self.assertEqual(soup.a.b, tag)
                self.assertEqual("<a>Foo<b>Bar</b></a>", str(soup.a)) 
                
                ''' Test the append function by appending empty string '''
                
                soup_2 = BeautifulSoup("<a>Foo</a>", "html.parser")
                soup_2_app = BeautifulSoup("<a>Foo</a>", "html.parser")
                soup_2.append("")
                self.assertEqual(soup_2.contents, soup_2_app.contents  + [""])


        def test_append_raise(self):
                ''' Assert that append without argument raises a TypeError due to too few arguments '''
                
                append_raise_soup = BeautifulSoup("<a>Foo</a>", "html.parser")
                with self.assertRaises(TypeError):
                        append_raise_soup.a.append()

        def test_insert_before(self):
                ''' Insert_before() test with a <i>Don't</i> tag inserted before string '''
                
                soup = BeautifulSoup("<b><i>Don't</i>stop</b>", "html.parser")
                b_soup = BeautifulSoup("<b>stop</b>", "html.parser")
                
                tag = soup.new_tag("i")
                tag.string = "Don't"
                
                b_soup.b.string.insert_before(tag)
                
                self.assertEqual(soup, b_soup)

                ''' Insert_before test with string argument before tag. '''
                soup_2 = BeautifulSoup("<b>tester soup</b>", "html.parser")
                b_soup_2 = BeautifulSoup("Foo<b>tester soup</b>", "html.parser")
                
                soup_2.b.insert_before("Foo")
                self.assertEqual(soup_2, b_soup_2)

        def test_insert_before_raise(self):
                ''' Insert_before() without argument test.'''
                
                soup = BeautifulSoup("<b>testing soup</b>", "html.parser")
                with self.assertRaises(TypeError):
                        soup.insert_before()

        def test_insert_after(self):
                ''' Insert_after() test with an <i>stop</i> tag after string '''
                
                soup = BeautifulSoup("<b>Don't </b>", "html.parser")
                soup_r = BeautifulSoup("<b>Don't <i>stop</i></b>", "html.parser")
                
                tag = soup.new_tag("i")
                tag.string = "stop"
                
                soup.b.string.insert_after(tag)
                
                self.assertEqual(soup, soup_r)

                ''' Insert_after() test with an string argument after tag. '''
                soup_2 = BeautifulSoup("<b>Don't</b>", "html.parser")
                soup_2_r = BeautifulSoup("<b>Don't</b>TestThis", "html.parser")
                soup_2.b.insert_after("TestThis")
                
                self.assertEqual(soup_2, soup_2_r)

                
                
        def test_insert_after_raise(self): 
                ''' Insert_after () test with no argument, to raise exception. '''

                soup = BeautifulSoup("<b>Don't </b>", "html.parser")
                with self.assertRaises(TypeError):
                        soup.insert_after()

        def test_clear(self):
                ''' Clear the contents of a HTML <a href> tag. '''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                soup = BeautifulSoup(markup, "html.parser")

                soup.a.clear()
                
                cleared_markup = '<a href="http://example.com/"></a>'
                cleared_soup = BeautifulSoup(cleared_markup, "html.parser")

                self.assertEqual(soup, cleared_soup)

        def test_clear_empty(self):
                ''' Clear the contents of an empty HTML <a href> tag. '''
                
                markup = '<a href="http://example.com/"></a>'
                soup = BeautifulSoup(markup, "html.parser")
                soup_2 = BeautifulSoup(markup, "html.parser")

                soup.a.clear()
                
                self.assertEqual(soup, soup_2)

        def test_clear_with_arg(self):
                ''' Call clear with argument, works just as clear(). '''
                
                markup = '<a href="http://example.com/"></a>'
                soup = BeautifulSoup(markup, "html.parser")
                soup_2 = BeautifulSoup(markup, "html.parser")

                soup.a.clear("argument")
                
                self.assertEqual(soup, soup_2)

        def test_extract(self):
                ''' Extract a tag and see if it is correctly returned, and that the original is changed accordingly '''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                extracted_markup = '<a href="http://example.com/">I linked to </a>'
                
                soup = BeautifulSoup(markup, "html.parser")
                extracted_soup = BeautifulSoup(extracted_markup, "html.parser")

                tag = soup.new_tag("i")
                tag.string = "example.com"
                
                extracted_tag = soup.i.extract()
                
                self.assertEqual(extracted_tag.parent, None)
                self.assertEqual(extracted_tag, tag)
                self.assertEqual(soup, extracted_soup)

        def test_extract_raises(self):
                ''' Test extracting a non-existing tag, ensuring that the original isn't changed. '''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                extr_soup = BeautifulSoup(markup, "html.parser")
                extr_null_soup = extr_soup.extract()
                
                self.assertEqual(extr_soup, extr_null_soup)

        def test_extract_with_arg(self):
                ''' Test extracting by calling extract() with a random argument. '''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                extr_arg_soup = BeautifulSoup(markup, "html.parser")
                with self.assertRaises(TypeError):
                        extr_arg_soup_extracted = extr_arg_soup.extract("arg")

        def test_decompose(self):
                ''' Test the decompose function by removing and destroying a tag. '''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                markup_decomposed = '<a href="http://example.com/">I linked to </a>'
                
                soup = BeautifulSoup(markup, "html.parser")
                dec_soup = BeautifulSoup(markup_decomposed, "html.parser")

                soup.i.decompose()
                
                self.assertEqual(soup, dec_soup)

        def test_decompose_empty(self):
                ''' Test the decompose function by removing an empty tag. '''
                
                markup = '<a href="http://example.com/">I linked to <i></i></a>'
                markup_decomposed = '<a href="http://example.com/">I linked to </a>'
                
                soup = BeautifulSoup(markup, "html.parser")
                dec_soup = BeautifulSoup(markup_decomposed, "html.parser")

                soup.i.decompose()
                
                self.assertEqual(soup, dec_soup)

        def test_decmpose_arg(self):
                ''' Test the decompose function by calling decompose with arg. '''
                
                markup = '<a href="http://example.com/">I linked to <i> test </i></a>'
                markup_decomposed = '<a href="http://example.com/">I linked to </a>'
                dec_soup = BeautifulSoup(markup, "html.parser")
                
                with self.assertRaises(TypeError):
                        dec_soup.i.decompose("test_arg")

        def test_replace_with(self):
                ''' Test the replace with function '''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                rep_markup = '<a href="http://example.com/">I linked to <b>new_example.com</b></a>'
                
                soup = BeautifulSoup(markup, "html.parser")
                rep_soup = BeautifulSoup(rep_markup, "html.parser")
                
                new_tag = soup.new_tag("b")
                new_tag.string = "new_example.com"

                soup.a.i.replace_with(new_tag)
                
                self.assertEqual(soup, rep_soup)

        def test_replace_tag_with_string(self):
                ''' Test replacing tag with string '''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                rep_markup = '<a href="http://example.com/">I linked to testText</a>'
                
                soup = BeautifulSoup(markup, "html.parser")
                rep_soup = BeautifulSoup(rep_markup, "html.parser")

                soup.i.replace_with("testText")
                
                self.assertEqual(soup, rep_soup)
                self.assertEqual(str(soup), str(rep_soup))

                #soup.a.contents <--- this gives a list containing 2 elements, one for each string.

        def test_replace_with_no_tag(self):
                ''' Test replace_with() called without argument. '''
                
                markup = '<a href="http://example.com/"I linked to <i>example.com</i></a>'
                no_soup = BeautifulSoup(markup, "html.parser")
                a_tag = no_soup.a
                
                with self.assertRaises(AttributeError):
                        a_tag.i.replace_with()

        def test_wrap(self):
                ''' Test wrap() by wrapping a b tag around an a tag '''

                markup = '<a>Text to be wrapped</a>'
                soup = BeautifulSoup(markup, "html.parser")

                wr_markup = '<b><a>Text to be wrapped</a></b>'
                wr_soup = BeautifulSoup(wr_markup, "html.parser")

                tag = soup.new_tag("b")

                soup.a.wrap(tag)

                self.assertEqual(soup, wr_soup)

        def test_wrap_with_string(self):
                ''' Test wrap() by wrapping a b tag around an a tag, where b contains a string'''

                markup = '<a>Text to be wrapped</a>'

                soup = BeautifulSoup(markup, "html.parser")

                wr_markup = '<b>string<a>Text to be wrapped</a></b>'
                wr_soup = BeautifulSoup(wr_markup, "html.parser")

                tag = soup.new_tag("b")
                tag.string = "string"

                soup.a.wrap(tag)

                self.assertEqual(soup, wr_soup) 

        def test_unwrap(self):
                ''' Test unwrap() function.'''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                soup = BeautifulSoup(markup, "html.parser")

                unwrapped_markup = '<a href="http://example.com/">I linked to example.com</a>'
                unwrapped_soup = BeautifulSoup(unwrapped_markup, "html.parser")
                
                soup.a.i.unwrap()
                
                #The soups are not equal, but as strings they are equal
                self.assertEqual(str(soup), str(unwrapped_soup))
                self.assertEqual(soup, unwrapped_soup)

                #soup.a.string <-- This is None at this point
                #soup.a.contents <--- this gives a list containing 2 elements, one for each string.

        def test_unwrap_with_arg(self):
                ''' Test unwrap() with arg. '''
                
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                unwrap_soup = BeautifulSoup(markup, "html.parser")
                a_tag = unwrap_soup.a
                
                with self.assertRaises(TypeError):
                        a_tag.i.unwrap("a")

        
        def test_unwrap_no_tag(self):
                ''' Test unwrap() on non-exisiting tag. '''
                
                markup = 'htadsasdtp/example.codssdd'
                unwrap_soup = BeautifulSoup(markup, "html.parser")
                
                with self.assertRaises(ValueError):
                        unwrap_soup.unwrap()
        

        def test_wrap_unwrap(self):
                ''' Test wrapping and then unwrapping '''

                markup = '<a>Text to be wrapped</a>'
                soup = BeautifulSoup(markup, "html.parser")
                soup_2 = BeautifulSoup(markup, "html.parser")

                tag = soup.new_tag("b")

                soup.a.wrap(tag)
                soup.b.unwrap()

                self.assertEqual(soup, soup_2)

        def test_no_name_tag(self):
                ''' test returning a name of a tag with no name'''

                self.assertEqual(self.no_name_tag.name, "")

        

if __name__ == '__main__':
	unittest.main()

