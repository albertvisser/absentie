import cgi
import school_progpad
from toon_abs_main import toon_abs_main
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
    form_ok = False
    if form.has_key("ta1") and form.has_key("ta2"):
        u = form["ta1"].value
        s = form["ta2"].value
        h = check_login(u,s)
        if h.SessionOk:
            form_ok = True
            xslevel = h.xslevel
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    if form_ok:
        l = toon_abs_main(u,xslevel)
        #~ m = ('gebruiker %s heeft toegangsniveau %s' % (u,xslevel))
        #~ l = meld_fout("Er is iets misgegaan",m)
    else:
        l = meld_fout("Er is iets misgegaan",m)
    print "Content-Type: text/html"     # HTML is following
    print
    for x in l.regels:
      print x

if __name__ == '__main__':
    main()

