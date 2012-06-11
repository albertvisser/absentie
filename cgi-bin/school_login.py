#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import shared
from start_main import Login

def main():
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    l = Login()
    for x in l.regels:
      print x

if __name__ == '__main__':
	main()
