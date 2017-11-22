from bs4 import BeautifulSoup


html_file = open("html_testfiles/html_test.html");
soup = BeautifulSoup(html_file, "html.parser")

#print(soup.prettify())

#print(soup.find_all(id ="atag"))

def bs_find_all(string):
	return soup.find_all(id ="atag")

def bs_find_first_a():
	return soup.a

def bs_find_id(string):
	return soup.find_all(id = string)