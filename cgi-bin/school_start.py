import cgi
import school_progpad
from start_main import start_main
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
    form_ok = False
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    if form.has_key("tb1") and form.has_key("tb2"):
        u = form["tb1"].value
        s = form["tb2"].value
        h = check_login(u,s)
        if h.SessionOk:
            form_ok = True
            xslevel = h.xslevel
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    if form_ok:
        l = start_main(u,xslevel)
    else:
        l = meld_fout("Er is iets misgegaan",m)
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    for x in l.regels:
      print x

if __name__ == '__main__':
	main()
