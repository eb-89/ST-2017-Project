from bs4 import BeautifulSoup


html_file = open("html_test.html");
soup = BeautifulSoup(html_file, "html.parser")

#print(soup.prettify())

def bs_find_all(string):
	return soup.find_all(string)

def bs_find_first_a():
	return soup.a
