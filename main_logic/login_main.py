from school_globals import *
from school_user import User
from start_main import start_main

class login_main:
    def __init__(self,userid="",paswd=""):
        ok = 'ok'
        if userid != '':
            if paswd != '':
                dh = User(userid, paswd)
                if dh.found:
                    if dh.paswdok:
                        if dh.blck == "J":
                            ok = 'Uw gebruikers-id is geblokkeerd'
                    else:
                        ok = "Het wachtwoord dat u heeft ingevuld is niet correct"
                else:
                    ok = "De gebruikersnaam die u heeft ingevuld is niet bekend"
            else:
                paswd = ""
                ok = "U heeft geen wachtwoord ingevuld"
        else:
            ok = "U heeft geen gebruikersnaam ingevuld"
        self.cregels = []
        self.regels = []
        if ok == 'ok':
            s = dh.startSession()
            from Cookie import SimpleCookie
            from Cookie import _getdate
            c = SimpleCookie()
            c["usernaam"] = userid
            c["usernaam"]["path"] = ""
            c["usernaam"]["expires"] = _getdate(90000) # 3600 is huidige tijd (GMT + 1 uur): 86400 is 24 uur: samen dus morgen
            c["sessionid"] = s
            c["sessionid"]["path"] = ""
            c["sessionid"]["expires"] = _getdate(90000)
            self.cregels.append(c.output())
            ok = 'Het wachtwoord dat u heeft ingevuld is correct.<br /><br />U bent nu aangelogd'
            xslevel = dh.getLevel()
            f = dh.getAttr('start')
            if not f: f = snames[0]
            sp = f.split(':')
            if sp[0] == snames[0]:	# startscherm
                from start_main import start_main
                l = start_main(userid,xslevel)
            elif sp[0] == snames[1]: 	# toon_klas
                from toon_kl_main import toon_kl_main
                l = toon_kl_main(sp[1],userid,xslevel)
            elif sp[0] == snames[2]: 	# sel_leerling
                from sel_ll_main import sel_ll_main
                l = sel_ll_main(sp[1],snames[0],userid,s,xslevel)
            elif sp[0] == snames[3]: 	# toon_klas
                from toon_abs_main import toon_abs_main
                l = toon_abs_main(userid,xslevel)
            for x in l.regels:
                self.regels.append(x)
                #~ print x
        else:
            kop = "Login fout"
            f = file(filepad + "next.html","r")
            for x in f.readlines():
                h = x.find("%s")
                if h > -1:
                    hs = x[:-1].split("%s")
                    if x.find("stylesheet") > -1:
                        self.regels.append(httppad.join(hs))
                elif x[:-1] == "<!-- kop -->":
                    for y in printkop(kop):                  # gedefinieerd in school_globals
                        self.regels.append(y)
                elif x[:-1] == "<!-- data -->":
                    self.regels.append('<br /><div>%s</div>' % ok)
                else:
                    self.regels.append(x[:-1])

def main():
    h = login_main('woefdram','magiokis')
    for x in h.cregels:
        print x

if __name__ == "__main__":
    main()
