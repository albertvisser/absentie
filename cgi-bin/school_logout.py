#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import shared
from start_main import Logout

def main():
    form = cgi.FieldStorage()
    form_ok = False
    u = form.getfirst("lu1", '')
    s = form.getfirst("lu2", '')
    level, meld = shared.check_session(u, s)
    if meld:
        l = shared.MeldFout("Er is iets misgegaan", meld)
    else:
        l = Logout(u, s)
    print("Content-Type: text/html\n")     # HTML is following
    for x in l.regels:
        print(x)

if __name__ == '__main__':
	main()
