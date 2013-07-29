#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import shared
from groep_main import WijzigGroep
from Edex_objects import GRgeg

def main():
    form = cgi.FieldStorage()
    form_ok = False
    u = s = ''
    for k in form.keys():
        if k.startswith('wgr1'):
            u = form[k].value
        elif k.startswith('wgr2'):
            s = form[k].value
    xslevel, meld = shared.check_session(u, s)
    if not meld:
        id = form.getfirst("hId", '')
        nm = form.getfirst("tnaam", '')
        jr = form.getfirst("selJR", '')
        lk = form.getfirst("selLK", '')
        if not id or not nm or not jr or not lk:
            meld = "Alle rubrieken moeten worden ingevuld"
    print("Content-Type: text/html")    # HTML is following
    if meld:
        l = shared.MeldFout("Er is iets misgegaan", meld)
        print()
        for x in l.regels:
            print(x)
        return
    ln = WijzigGroep(id, nm, jr, lk)
    if ln.ok:
        # doorlinken naar selectiescherm
        print('Location: http://school.pythoneer.nl/cgi-bin/toon_groepen.py?'
            'tgr1=%s&tgr2=%s' % (u,s))
        print()
    else:
        print()
        print ("Wijzigen is niet gelukt")

if __name__ == '__main__':
    main()

