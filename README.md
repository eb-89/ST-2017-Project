# ST-2017-Project
Software testing project

Files for Software Testing Project 2017, Uppsala University

The files bs_test.py and bs_func.py are now legacy. You can open them if you want, but no code from these files are run during the tests. bs_test.py contains calls to some constructors defined in the elements.py module, and some calls to internal functions. 

The file plan_for_test.txt contains a list of functionality planned for testing.

##To add tests, do the following:

1. Add a HTML file to the html_testfile folder or write one directly in the initialization code for the test class in unittest_tests.py

2. Turn it into soup by calling the BS constructor.

3. Add tests.

Check the unittest_tests.py to see examples.


##To run the tests on the BS project, do the following:

1. Download the BS project (clone it with git, this is probably easiest).

2. Copy the file "unittest_test.py" to the BS root directory.

3. Copy the folder "html_testfiles" to the BS root directory

4. Open your terminal.

   To just run the tests, run:
   python unittest_tests.py

   To have Coverage produce a report, run:
   coverage run unittest_tests.py

   To have Coverage print out a nice html-report, run:
   coverage html








