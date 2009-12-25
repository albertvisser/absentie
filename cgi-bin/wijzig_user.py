import cgi
import school_progpad
from wijzig_us_main import wijzig_us_main
from wijzig_us_main import wijzig_pw_main
from wijzig_us_main import wijzig_pw_vraag
from check_login import check_login
from check_login import meld_fout

def main():
    form = cgi.FieldStorage()
    form_ok = False
    #~ print "Content-Type: text/html"     # HTML is following
    #~ print
    #~ print "<html>"
    #~ print "<head></head>"
    #~ print "<body>"
    #~ keys = form.keys()
    #~ keys.sort()
    #~ print
    #~ print "<H3>Form Contents:</H3>"
    #~ if not keys:
        #~ print "<P>No form fields."
    #~ print "<DL>"
    #~ for key in keys:
        #~ print "<DT>" + cgi.escape(key) + ":",
        #~ value = form[key]
        #~ print "<i>" + cgi.escape(`type(value)`) + "</i>"
        #~ print "<DD>" + cgi.escape(`value`)
    #~ print "</DL>"
    #~ print
    #~ print "</body></html>"
    #~ return
    if form.has_key("wu1") and form.has_key("wu2"):
        u = form["wu1"].value
        s = form["wu2"].value
        h = check_login(u,s)
        if h.SessionOk:
            xslevel = h.xslevel
            form_ok = True
        else:
            m = ("%s, uw login (%s) is klaarblijkelijk verlopen" % (u,s))
    else:
        m = "Geen usernaam en/of sessie-id meegegeven"
    if form_ok:
        uid = ''
        doe = ''
        van = ''
        newpw = ''
        if form.has_key("tNaam"):
            uid = form["tNaam"].value
        if form.has_key("hPw"):     #~ hPw "J" betekent wachtwoord wijzigen, "0" betekent nieuwe user
            doe = form["hPw"].value
        if form.has_key("tPwO"): # huidige wachtwoord
            oldpw = form["tPwO"].value
        if form.has_key("tPw"): # nieuwe wachtwoord
            newpw = form["tPw"].value
        if form.has_key("hVan"):
            van = form["hVan"].value
        if uid == '' or van == '':
            m = ("Geen userid (%s) of scherm (%s) opgegeven" % (uid,van))
            form_ok = False
        #~ else:
            #~ m = ("Userid is %s, komt van scherm %s (doe = '%s'" % (uid,van,doe))
            #~ form_ok = False
    if form_ok:
        if doe == "J":
            p = wijzig_pw_vraag(uid,van)
        elif newpw != '':
            p = wijzig_pw_main(uid,oldpw,newpw)
            if not p.ok:
                form_ok = False
                m = "het opgegeven (oude) wachtwoord is onjuist"
        else:
            uh = wijzig_us_main(uid,doe)
            if form.has_key("sType"):
                uh.addArg("type",form["sType"].value)
            if form.has_key("sBlok"):
                uh.addArg("blok",form["sBlok"].value)
            if form.has_key("sStart"):
                uh.addArg("start",form["sStart"].value)
            if form.has_key("tMet"):
                uh.addArg("met",form["tMet"].value)
            uh.doe()
            if doe == '0' and uh.exists:
                form_ok = False
                m = "opgegeven usernaam komt al voor"
            elif doe != '0' and not uh.exists:
                form_ok = False
                m = "opgegeven user niet gevonden"
            elif not uh.ok:
                form_ok = False
                m = "toevoegen/wijzigen is niet gelukt"
    if form_ok:
        if doe == "J":
            print "Content-Type: text/html"     # HTML is following
            print
            for x in p.regels:
                print x
        else:
            print "Content-Type: text/html"     # HTML is following
            # doorlinken naar selectiescherm
            # hier moet nog userid en sessionid aan doorgegeven worden
            # van = toon_users: tu1 en tu2
            # andere mogelijkheid: nog niet aanwezig (login pagina?)
            if van == 'toon_users':
                print ('Location: http://school.pythoneer.nl/cgi-bin/%s.py?tu1=%s&tu2=%s' % (van,u,s))
            print
    else:
        l = meld_fout("Er is iets misgegaan",m)
        print "Content-Type: text/html"     # HTML is following
        print
        for x in l.regels:
            print x

if __name__ == '__main__':
    main()

