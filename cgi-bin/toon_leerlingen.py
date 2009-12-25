import cgi
from school_progpad import *
from toon_ll_main import toon_ll_main
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    selId = ''
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    if form.has_key("tll1") and form.has_key("tll2"):
        u = form["tll1"].value
        s = form["tll2"].value
        h = check_login(u,s)
        if h.SessionOk:
            xslevel = h.xslevel
            form_ok = True
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    editEntry = False
    if form_ok:
        if form.has_key("edit"):
            editEntry = True
            selId = form["edit"].value
        l = toon_ll_main(xslevel,u,s,editEntry,selId)
    else:
        l = meld_fout("Er is iets misgegaan",m)
    #~ if editEntry:
        #~ f = file(filepad + "ll_temp.html","w")
        #~ for x in l.regels:
            #~ f.write(x)
        #~ f.close()
        #~ print "Content-Type: text/html"     # HTML is following
        #~ print "Location: http://school.pythoneer.nl/ll_temp.html#wijzigdeze"
        #~ print
    #~ else:
    if True: # always
        print "Content-Type: text/html"     # HTML is following
        print
        for x in l.regels:
            print x

if __name__ == '__main__':
    main()

