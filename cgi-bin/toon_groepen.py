#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import shared
from groep_main import ToonGroep

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    selId = ''
    u = form.getfirst("tgr1", '')
    s = form.getfirst("tgr2", '')
    xslevel, meld = shared.check_session(u, s)
    if meld:
        l = shared.MeldFout("Er is iets misgegaan", meld)
    else:
        sel_id = form.getfirst("edit", '')
        edit_entry = bool(sel_id) or False
        l = ToonGroep(xslevel, u, s, edit_entry, sel_id)
    print("Content-Type: text/html\n")     # HTML is following
    for x in l.regels:
        print(x)

if __name__ == '__main__':
    main()

