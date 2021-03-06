#! /usr/bin/env python3
import cgi
import cgitb
cgitb.enable()
import shared
from start_main import Start

def main():
    form = cgi.FieldStorage()
    form_ok = False
    u = form.getfirst("tb1", '')
    s = form.getfirst("tb2", '')
    xslevel, meld = shared.check_session(u, s)
    if meld:
        l = shared.MeldFout("Er is iets misgegaan", meld)
    else:
        l = Start(u, xslevel)
    print("Content-Type: text/html\n")     # HTML is following
    for x in l.regels:
        print(x)

if __name__ == '__main__':
	main()
