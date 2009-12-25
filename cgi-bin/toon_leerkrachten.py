import cgi
from school_progpad import *
from toon_lk_main import toon_lk_main
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
    form_ok = 0
    selId = ''
    # op basis van de inhoud van de velden tk1 en tk2 de login checken
    # aan de login database
    if form.has_key("tlk1") and form.has_key("tlk2"):
        u = form["tlk1"].value
        s = form["tlk2"].value
        h = check_login(u,s)
        if h.SessionOk:
            form_ok = True
            xslevel = h.xslevel
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    editEntry = False
    if form_ok:
        if form.has_key("edit"):
            editEntry = True
            selId = form["edit"].value
        l = toon_lk_main(xslevel,u,s,editEntry,selId)
    else:
        l = meld_fout("Er is iets misgegaan",m)
    # het navolgende is leuk als je een lijst langer dan het scherm hebt
    #~ if editEntry:
        #~ f = file(filepad + "lk_temp.html","w")
        #~ for x in l.regels:
            #~ f.write(x + "\n")
        #~ f.close()
        #~ print "Content-Type: text/html"     # HTML is following
        #~ print "Location: http://school.pythoneer.nl/lk_temp.html#wijzigdeze"
        #~ print
        #~ print "Location: http://school.pythoneer.nl/../cgi-bin/lk_temp.html#wijzigdeze"
    #~ else:
    if True: # always
        print "Content-Type: text/html"     # HTML is following
        print
        for x in l.regels:
            print x

if __name__ == '__main__':
    main()

