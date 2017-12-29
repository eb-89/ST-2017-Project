import unittest
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

class TestBS(unittest.TestCase):


	#tag = self.a_simple_soup.find("")

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
		<html><html>
                ''', "html.parser")

		#Here we call find directly
		tag = self.a_simple_soup.find("a")

		#Here we call find all directly
		tag = self.a_simple_soup.find_all("a")

		#Here we call find all directly
		tag = self.a_simple_soup.find_all()

		#here kwarg contains "string", and there is no text argument.
		tag = self.a_simple_soup.find_all(string = "a")

		#here we define a custom SoupStrainer
		strainer = SoupStrainer("a")
		tag = self.a_simple_soup.find_all(strainer)

		#here we find with limit
		tag = self.a_simple_soup.find_all("a", limit = 1)

		#Putting recursive to False makes BS only look one level down from the 
		#tag from which the search started.
		tag = self.tiny_soup.find_all("a", recursive = False)

		
		
		


if __name__ == '__main__':
	unittest.main()