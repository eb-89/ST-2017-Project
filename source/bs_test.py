from bs4 import BeautifulSoup
import bs4.element as el

#The html file
html_doc = """
<html>
<head>
	<title>The Dormouse's story</title>
</head>

<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

#This will test code in the bs4 package declaration (the __init__ file in the folder bs4)
soup = BeautifulSoup(html_doc, 'html.parser')
soup.find_all('a')

########################
# Below is code for how to use the constructors for classes defined inside the element.py file

#this code never runs, specifically to test that Coverage reports correctly here
if (False):
	print("absc")

# a new page element, this class contains _find_all and attributeChecker
pe = el.PageElement()

# needs to run for initalization of the pageElement.
pe.setup()

# How to use the tag constructor, the name attribute must always be defined.
tag1 = el.Tag(pe, attrs = (("a", "valueofa"), ("b", "valueofb")), name="name1")
tag2 = el.Tag(pe, attrs = ({"notA": "valueofnotA", "notB": "valueofnotB"}), name="name2")
tag3 = el.Tag(pe, attrs = ({"notA": "valueofnotA"}), name="name2")


print(pe.format_string("test_string_0"))

 #format_sting always runs with this attr.
print(pe.format_string( "test_string_0", formatter="minimal"))


# _attribute_checker returns a lambda function (https://en.wikipedia.org/wiki/Anonymous_function)
ac = pe._attribute_checker("=", "a", value="valueofa") #true if this attribute is there, otherwise false
ac2 = pe._attribute_checker("=", "notB", value="valueofnotB") #true if this attribute is there, otherwise false


print(tag1.get("a")) ##prints "valueofa"

print(ac(tag1)) #tag 1 contains attribute "a = valueofa", returns true
print(ac(tag2)) #tag 2 doesnt, returns false
print(ac2(tag2)) #True
print(ac2(tag3)) #False

##this calls _find_all within the pageElement object, see Tag constructor.
# I haven't found a way to call that func directly, in a sane way, yet.
tag1.find_all("test_string_2") 


#print(soup.find(class = 'sister'))
#print(soup.find(id = 'link1'))