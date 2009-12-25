import cgi
import school_progpad
from start_main import login_main

def main():
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    l = login_main()
    for x in l.regels:
      print x

if __name__ == '__main__':
	main()
