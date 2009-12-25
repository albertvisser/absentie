import cgi
import school_progpad
from check_login import check_login
from check_login import meld_fout
from logout_main import logout_main

def main():
    form = cgi.FieldStorage()
    form_ok = False
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    if form.has_key("lu1") and form.has_key("lu2"):
        u = form["lu1"].value
        s = form["lu2"].value
        h = check_login(u,s)
        if h.SessionOk:
            form_ok = True
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    if form_ok:
        l = logout_main(u,s)
    else:
        l = meld_fout("Er is iets misgegaan",m)
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    for x in l.regels:
      print x

if __name__ == '__main__':
	main()
