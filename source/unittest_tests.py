import unittest
from bs4 import BeautifulSoup



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

        def test_append(self):
                ''' Test the append function by appending an <a>Bar</a> tag'''
                append_soup = BeautifulSoup("<a>Foo</a>", "html.parser")
                appended_soup = BeautifulSoup("<a>Foo</a><a>Bar</a>", "html.parser")
                append_soup.a.append("Bar")
                self.assertEqual(append_soup.a.contents[0].string, appended_soup.a.contents[0].string)

                ''' Test the append function by appending without value '''
                append_soup2 = BeautifulSoup("<a>Foo</a>", "html.parser")
                appended_soup2 = BeautifulSoup("<a>Foo</a>", "html.parser")
                append_soup2.a.append("")
                self.assertEqual(append_soup2.a.contents[0], appended_soup2.a.contents[0])

                ''' Calling append without argument should raise an error. '''
                append_soup3 = BeautifulSoup("<a>Foo</a>", "html.parser")
                appended_soup3 = BeautifulSoup("<a>Foo</a>", "html.parser")
                try:
                        append_soup3.a.append()
                        self.assertEqual(append_soup3.a.contents[0].string, appended_soup3.a.contents[0].string)
                except:
                        True

        def test_append_raise(self):
                ''' Assert that append without argument raises a TypeError due to too few arguments '''
                append_raise_soup = BeautifulSoup("<a>Foo</a>", "html.parser")
                with self.assertRaises(TypeError):
                        append_raise_soup.a.append()

        def test_insert_before(self):
                ''' Insert_before() test with an <i>Don't</i> tag '''
                insert_before_soup_with_tag = BeautifulSoup("<b><i>Don't</i>stop</b>", "html.parser")
                insert_before_soup = BeautifulSoup("<b>stop</b>", "html.parser")
                insert_before_tag = insert_before_soup.new_tag("i")
                insert_before_tag.string = "Don't"
                insert_before_soup.b.string.insert_before(insert_before_tag)
                self.assertEqual(insert_before_soup.b.contents, insert_before_soup_with_tag.b.contents)

                ''' Insert_before() test with an empty argument. '''
                insert_before_soup2 = BeautifulSoup("<b>tester soup</b>", "html.parser")
                inserted_before_soup = BeautifulSoup("<b>tester soup</b>", "html.parser")
                insert_before_soup2.b.insert_before("")
                self.assertEqual(insert_before_soup2.b.contents[0].string, inserted_before_soup.b.contents[0].string)

        def test_insert_before_raise(self):
                ''' Insert_before() without argument test.'''
                insert_before_raise_soup = BeautifulSoup("<b>testing soup</b>", "html.parser")
                with self.assertRaises(TypeError):
                        insert_before_raise_soup.insert_before()

        def test_insert_after(self):
                ''' Insert_after() test with an <i>stop</i> tag. '''
                insert_after_soup_with_tag = BeautifulSoup("<b>Don't<i>stop</i></b>", "html.parser")
                insert_after_soup = BeautifulSoup("<b>Don't</b>", "html.parser")
                insert_after_tag = insert_after_soup.new_tag("i")
                insert_after_tag.string = "stop"
                insert_after_soup.b.string.insert_after(insert_after_tag)
                self.assertEqual(insert_after_soup.b.contents, insert_after_soup_with_tag.b.contents)

                ''' Insert_after() test with an emtpy argument. '''
                insert_after_soup2 = BeautifulSoup("<b>test insert_after soup</b>", "html.parser")
                inserted_after_soup = BeautifulSoup("<b>test insert_after soup</b>", "html.parser")
                insert_after_soup2.b.insert_after("")
                self.assertEqual(insert_after_soup2.b.contents[0].string, inserted_after_soup.b.contents[0].string)

                ''' Insert_after () test with no argument, to raise exception. '''
                insert_after_raise_soup = BeautifulSoup("<b>raise test soup</b>", "html.parser")
                with self.assertRaises(TypeError):
                        insert_after_raise_soup.insert_after()

        def test_clear(self):
                ''' Clear the contents of a HTML <a href> tag. '''
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                cleared_markup = '<a href="http://example.com/"></a>'
                clear_soup = BeautifulSoup(markup, "html.parser")
                clear_tag = clear_soup.a
                clear_tag.clear()
                self.assertEqual(str(clear_tag), cleared_markup)

        def test_clear_empty(self):
                ''' Clear the contents of an empty HTML <a href> tag. '''
                empty_tag_markup = '<a href="http://example.com/"></a>'
                clear_empty_soup = BeautifulSoup(empty_tag_markup, "html.parser")
                clear_empty_tag = clear_empty_soup.a
                clear_empty_tag.clear()
                self.assertEqual(str(clear_empty_tag), empty_tag_markup)

        def test_clear_with_arg(self):
                ''' Call clear with argument, works just as clear(). '''
                raise_clear_markup = '<a href="http://example.com/">A test tag <i>example.com</i></a>'
                raise_clear_empty_markup = '<a href="http://example.com/"></a>'
                raise_clear_soup = BeautifulSoup(raise_clear_markup, "html.parser")
                raise_clear_tag = raise_clear_soup.a
                raise_clear_tag.clear("asdasda")
                self.assertEqual(str(raise_clear_tag), raise_clear_empty_markup)

        def test_extract(self):
                ''' Extract a tag and see if it is correctly returned, and that the original is changed accordingly '''
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                a_tag_markup = '<a href="http://example.com/">I linked to </a>'
                extracted_tag_markup = '<i>example.com</i>'
                extract_soup = BeautifulSoup(markup, "html.parser")
                #a_tag = extract_soup.a  (not sure why I left this here)
                extracted_tag = extract_soup.i.extract()
                self.assertEqual(extracted_tag.parent, None)
                self.assertEqual(str(extracted_tag), extracted_tag_markup)
                self.assertEqual(str(extract_soup), a_tag_markup)

        def test_extract_raises(self):
                ''' Test extracting a non-existing tag, ensuring that the original isn't changed. '''
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                extr_raise_soup = BeautifulSoup(markup, "html.parser")
                extr_raise_soup_extracted = extr_raise_soup.extract()
                self.assertEqual(str(extr_raise_soup_extracted), markup)

        def test_extract_with_arg(self):
                ''' Test extracting by calling extract() with a random argument. '''
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                extr_arg_soup = BeautifulSoup(markup, "html.parser")
                with self.assertRaises(TypeError):
                        extr_arg_soup_extracted = extr_arg_soup.extract("asd")

        def test_decompose(self):
                ''' Test the decompose function by removing and destroying a tag. '''
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                markup_decomposed = '<a href="http://example.com/">I linked to </a>'
                dec_soup = BeautifulSoup(markup, "html.parser")
                a_tag = dec_soup.a
                dec_soup.i.decompose()
                self.assertEqual(str(a_tag), markup_decomposed)

        def test_decompose_empty(self):
                ''' Test the decompose function by removing an empty tag. '''
                markup = '<a href="http://example.com/">I linked to <i></i></a>'
                markup_decomposed = '<a href="http://example.com/">I linked to </a>'
                dec_soup = BeautifulSoup(markup, "html.parser")
                a_tag = dec_soup.a
                dec_soup.i.decompose()
                self.assertEqual(str(a_tag), markup_decomposed)

        def test_decmpose_arg(self):
                ''' Test the decompose function by calling decompose with arg. '''
                markup = '<a href="http://example.com/">I linked to <i> test </i></a>'
                markup_decomposed = '<a href="http://example.com/">I linked to </a>'
                dec_soup = BeautifulSoup(markup, "html.parser")
                a_tag = dec_soup.a
                with self.assertRaises(TypeError):
                        dec_soup.i.decompose("testArg")

        def test_replace_with(self):
                ''' Test the replace with function '''
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                rep_markup = '<a href="http://example.com/">I linked to <b>new_example.com</b></a>'
                rep_soup = BeautifulSoup(markup, "html.parser")
                a_tag = rep_soup.a
                new_tag = rep_soup.new_tag("b")
                new_tag.string = "new_example.com"
                a_tag.i.replace_with(new_tag)
                self.assertEqual(str(a_tag), rep_markup)

        def test_replace_with_incorrect_tag(self):
                '''
                Test replace with erroneous arg. This works and shows that it is up to the user
                to ensure correct usage and not create incorrect HTML
                '''
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                rep_markup = '<a href="http://example.com/">I linked to testText</a>'
                arg_soup = BeautifulSoup(markup, "html.parser")
                a_tag = arg_soup.a
                a_tag.i.replace_with("testText")
                self.assertEqual(str(a_tag), rep_markup)

        def test_replace_with_no_tag(self):
                ''' Test replcae_with() called without argument. '''
                markup = '<a href="http://example.com/"I linked to <i>example.com</i></a>'
                no_soup = BeautifulSoup(markup, "html.parser")
                a_tag = no_soup.a
                with self.assertRaises(AttributeError):
                        a_tag.i.replace_with()

        def test_unwrap(self):
                ''' Test unrwap() function.'''
                markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
                unwrapped_markup = '<a href="http://example.com/">I linked to example.com</a>'
                unwrap_soup = BeautifulSoup(markup, "html.parser")
                a_tag = unwrap_soup.a
                a_tag.i.unwrap()
                self.assertEqual(str(a_tag), unwrapped_markup)

        def test_unwrap(self):
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

        def test_soup_head(self):
                ''' Test soup constructor for head tag '''
                markup = '<html><head>asd</head><body><p>hej</p></body></html>'
                head_markup = '<head>asd</head>'
                head_content_markup = [u'asd']
                soup_head = BeautifulSoup(markup, "html.parser")
                self.assertEqual(str(soup_head.head), head_markup)
                self.assertEqual(soup_head.head.contents, head_content_markup)

        def test_soup_headless(self):
                '''' Test soup constructor without head tag '''
                markup = '<html><body><p>asd</p></body></html>'
                headless_soup = BeautifulSoup(markup, "html.parser")
                self.assertEqual(headless_soup.head, None)

        def test_soup_title(self):
                ''' Test soup constructor for title tag '''
                markup = '<html><head><title>A title</title></head><body></body></html>'
                title_tag = '<title>A title</title>'
                title_string = 'A title'
                title_soup = BeautifulSoup(markup, "html.parser")
                self.assertEqual(str(title_soup.title), title_tag)
                self.assertEqual(str(title_soup.title.string), title_string)
        
        def test_soup_contents(self):
                ''' The contents attribute returns the contents of a tag. A string should throw error on contents'''
                markup = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                bt1 = '<b>bold tag 1</b>'
                bt2 = '<b>bold tag 2</b>'
                soup = BeautifulSoup(markup, "html.parser")

                self.assertEqual([str(soup.a.contents[0]), str(soup.a.contents[1])] , [bt1,bt2])
                self.assertEqual(soup.a.b.contents, [soup.a.b.string])

                with self.assertRaises(AttributeError):
                        self.assertEqual(soup.a.b.string.contents, 0) 
        
        def test_soup_children(self):
                ''' The children attribute returns a generator, for iterating over children'''
                markup = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                bt_list = ['<b>bold tag 1</b>', '<b>bold tag 2</b>']
                soup = BeautifulSoup(markup, "html.parser")

                index = 0
                for c in soup.a.children:
                         self.assertEqual(str(c), bt_list[index])
                         index += 1


        def test_soup_descendants(self):
                ''' The descentants attribute returns the all descentants of a tag, including strings '''
                markup = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                a1 = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                bt1 = '<b>bold tag 1</b>'
                bt2 = '<b>bold tag 2</b>'
                bt1_str = 'bold tag 1'
                bt2_str = 'bold tag 2'

                desc = [a1, bt1, bt1_str, bt2, bt2_str]

                soup = BeautifulSoup(markup, "html.parser")

                index = 0
                for c in soup.descendants:
                         self.assertEqual(str(c), desc[index])
                         index += 1

        def test_soup_stripped_strings(self):
                ''' stripped_strings should remove whitespaces and linebreaks before and after strings '''
                markup = '''<html><head>
                             String0    
                         </head><body>   String1  </body> String2
                         </html>'''
                string0 = 'String0'
                string1 = 'String1'
                string2 = 'String2'

                strings_soup = BeautifulSoup(markup, "html.parser")
                
                strings = []
                for string in strings_soup.stripped_strings:
                        strings.append(string)

                self.assertEqual(strings[0], string0)
                self.assertEqual(strings[1], string1)
                self.assertEqual(strings[2], string2)

                with self.assertRaises(IndexError):
                        strings[3]

        def test_soup_parent(self):
                '''parent attribute finds the direct parent. This applies to strings as well.
                The parent of a soup is None'''
                markup = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                soup = BeautifulSoup(markup, "html.parser")

                self.assertEqual(soup.a.b.parent, soup.a)
                self.assertEqual(soup.a.parent, soup)
                self.assertEqual(soup.parent, None)

                self.assertEqual(soup.a.b.string.parent, soup.a.b)


        def test_soup_parents(self):
                '''parents attribute finds all the parents '''
                markup = '<a><b>bold tag 1</b><b>bold tag 2</b></a>'
                soup = BeautifulSoup(markup, "html.parser")

                par = ['<b>bold tag 1</b>', '<a><b>bold tag 1</b><b>bold tag 2</b></a>', '[document]']

                ##Small irragularity here, parents does not go as high as None, although
                ##the documentation states that it should.

                index = 0
                for c in soup.a.b.string.parents:
                        if str(c.name) == '[document]':
                                self.assertEqual(c.name, par[-1])
                        else:
                                self.assertEqual(str(c), par[index])
                                index += 1


        def test_soup_titleless(self):
                ''' Test soup constructor for nonexisting title tag '''
                markup = '<html><head>asd</head><body>dsa</body></html>'
                title_soup = BeautifulSoup(markup, "html.parser")
                self.assertEqual(title_soup.title, None)

        def test_soup_string(self):
                ''' Test soup constructor for string tag '''
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
                string0 = 'String0'
                string1 = 'String1'
                string2 = 'String2'

                strings_soup = BeautifulSoup(markup, "html.parser")
                
                strings = []
                for string in strings_soup.strings:
                        strings.append(string)

                self.assertEqual(strings[0], string0)
                self.assertEqual(strings[1], string1)
                self.assertEqual(strings[2], string2)

                with self.assertRaises(IndexError):
                        strings[3]

        def test_soup_no_strings(self):
                '''Test soup constructor for strings without strings'''
                markup = '<html><head></head><body></body></html>'
                no_strings_soup = BeautifulSoup(markup, "html.parser")
                strings = []
                for string in no_strings_soup.strings:
                        strings.append(string)
                self.assertEqual(strings, [])

if __name__ == '__main__':
	unittest.main()

