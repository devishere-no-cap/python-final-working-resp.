import pyhtml
import student_a_level_1
import student_a_level_2
import student_a_level_3
import simple_test_page  # Import the page you just created


pyhtml.need_debugging_help=True

# pyhtml.MyRequestHandler.pages["/"]      =simple_test_page; 

pyhtml.MyRequestHandler.pages["/"]      =student_a_level_1; 
pyhtml.MyRequestHandler.pages["/page2a"]=student_a_level_2; 
pyhtml.MyRequestHandler.pages["/page3a"]=student_a_level_3; 


pyhtml.host_site()

