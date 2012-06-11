#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import shared # voegt pad naar programmtuur toe
from start_main import do_login
## from check_login import check

def main():
    "controleert het verstuurde userid en password en zet een cookie"
    "stuurt door naar het programma dat het scherm opbouwt"
    "dat moet als eerste het cookie controleren"
    form = cgi.FieldStorage()
    user = form.getfirst("txtUser", "")
    paswd = form.getfirst("txtPass", "")
    regels, cregels = do_login(user, paswd)
    for x in cregels:
        print x
    print "Content-Type: text/html"     # HTML is following
    print
    for x in regels:
        print x

if __name__ == "__main__":
    main()
