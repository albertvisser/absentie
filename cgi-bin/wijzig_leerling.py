#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import shared
from leerling_main import WijzigLeerling

def main():
    form = cgi.FieldStorage()
    form_ok = False
    u = ''
    s = ''
    for k in form.keys():
        if k.startswith('wll1'):
            u = form[k].value
        elif k.startswith('wll2'):
            s = form[k].value
    xslevel, meld = shared.check_session(u, s)
    if not meld:
        sel_id = form.getfirst("hId", '')
        vn = form["tvnaam"].value
        vv = form["ttus"].value
        an = form["tanaam"].value
        dd = form["tdag"].value
        mm = form["tmaand"].value
        jr = form["tjaar"].value
        gesl = form["selgesl"].value
        aut = form["selaut"].value
        grp = form["selgrp"].value
        if not sel_id or not vn or not an or not jr \
                or not gesl or not aut or not grp:
            meld = "Alle rubrieken moeten worden ingevuld"
    print "Content-Type: text/html"     # HTML is following
    if meld:
        l = shared.MeldFout("Er is iets misgegaan", meld)
        print
        for x in h.regels:
            print x
        return
    naam = (vn, vv, an)
    datum = (dd, mm, jr)
    ok = wijzig_leerling(sel_id, naam, datum, gesl, aut, grp)
    if ok:
        # doorlinken naar selectiescherm
        print ('Location: http://school.pythoneer.nl/cgi-bin/toon_leerlingen.py?tll1=%s&tll2=%s' % (u,s))
        print
    else:
        print
        print "Wijzigen is niet gelukt"

if __name__ == '__main__':
    main()

