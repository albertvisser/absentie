#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import shared
from klas_main import ToonKlas

def main():
    form = cgi.FieldStorage()
    form_ok = False
    u = form.getfirst("tk1", '')
    s = form.getfirst("tk2", '')
    xslevel, meld = shared.check_session(u, s)
    if not meld:
        sel_id = form.getfirst("selKlas", '')
        if sel_id:
            h = ToonKlas(sel_id, u, xslevel)
        else:
            meld = "Geen klas-id opgegeven"
    if meld:
        h = shared.MeldFout("Er is iets misgegaan", meld)
    print("Content-Type: text/html\n")     # HTML is following
    for x in h.regels:
      print(x)

if __name__ == '__main__':
    main()

