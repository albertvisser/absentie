#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import shared
from user_main import wijzig_user, wijzig_password, VraagPassword

def main():
    form = cgi.FieldStorage()
    u = form.getfirst("wu1", '')
    s = form.getfirst("wu2", '')
    xslevel, meld = shared.check_session(u, s)
    if not meld:
        uid = form.getfirst("tNaam", '')
        doe = form.getfirst("hPw", '')
        oldpw = form.getfirst("tPwO", '')
        newpw = form.getfirst("tPw", '')
        van = form.getfirst("hVan", '')
        if uid == '' or van == '':
            meld = ("Geen userid (%s) of scherm (%s) opgegeven" % (uid,van))
    if not meld:
        if doe == "J":
            p = VraagPassword(uid, van)
        elif newpw != '':
            p = wijzig_passw(uid, oldpw, newpw)
            if not p.ok:
                meld = "het opgegeven (oude) wachtwoord is onjuist"
            ## else:
                ## meld = 'uw wachtwoord is gewijzigd'
        else:
            utype = form.getfirst("sType", '')
            blok = form.getfirst("sBlok", '')
            start = form.getfirst("sStart", '')
            met = form.getfirst("tMet", '')
            nieuw = True if doe == '0' else False
            ok, meld = wijzig_user(uid, nieuw, utype, blok, start, met)
            if nieuw and not ok:
                meld = "opgegeven usernaam komt al voor"
            elif not nieuw and not ok:
                meld = "opgegeven user niet gevonden"
            ## elif not ok:
                ## meld = "toevoegen/wijzigen is niet gelukt"
    print("Content-Type: text/html")     # HTML is following
    if meld:
        l = shared.MeldFout("Er is iets misgegaan", meld)
        print()
        for x in l.regels:
            print(x)
    else:
        if doe == "J":
            print()
            for x in p.regels:
                print(x)
        else:
            # doorlinken naar selectiescherm
            # hier moet nog userid en sessionid aan doorgegeven worden
            # van = toon_users: tu1 en tu2
            # andere mogelijkheid: nog niet aanwezig (login pagina?)
            if van == 'toon_users':
                print('Location: http://school.pythoneer.nl/cgi-bin/%s.py?'
                    'tu1=%s&tu2=%s' % (van, u, s))
            print()

if __name__ == '__main__':
    main()

