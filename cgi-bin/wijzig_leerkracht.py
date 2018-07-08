#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import shared
from leerkracht_main import wijzig_leerkracht

def main():
    form = cgi.FieldStorage()
    form_ok = False
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    u = s = ''
    for k in form.keys():
        if k.startswith('wlk1'):
            u = form[k].value
        elif k.startswith('wlk2'):
            s = form[k].value
    xslevel, meld = shared.check_session(u, s)
    if not meld:
        sel_id = form.getfirst("hId", '')
        vn = form.getfirst("tvnaam", '')
        vv = form.getfirst("ttus", '')
        an = form.getfirst("tanaam", '')
        if not sel_id or not vn or not an:
            meld = "Alle rubrieken moeten worden ingevuld"
    print("Content-Type: text/html")    # HTML is following
    if meld:
        h = shared.MeldFout("Er is iets misgegaan", meld)
        print()
        for x in h.regels:
            print(x)
        return
    ok = wijzig_leerkracht(sel_id, vn, vv, an)
    if ok:
        # doorlinken naar selectiescherm
        print('Location: http://school.pythoneer.nl/cgi-bin/toon_leerkrachten.py?'
            'tlk1=%s&tlk2=%s' % (u,s))
        print()
    else:
        print()
        print("Wijzigen is niet gelukt")

if __name__ == '__main__':
    main()

