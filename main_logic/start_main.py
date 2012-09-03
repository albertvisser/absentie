import os
import sys
import common
from Edex_objects import leerkrachtenlijst

import common
from Cookie import SimpleCookie, _getdate
from school_user import User
from klas_main import ToonKlas
from select_leerling_main import SelectLeerling
from absentie_main import ToonAbsenten
okmelding = 'Het wachtwoord dat u heeft ingevuld is correct.<br /><br />' \
            'U bent nu aangelogd'

def do_login(userid="", paswd=""):
    ok = 'ok'
    if userid == '':
        ok = "U heeft geen gebruikersnaam ingevuld"
    elif paswd == '':
        ok = "U heeft geen wachtwoord opgegeven"
    else:
        dh = User(userid, paswd)
        if not dh.found:
            ok = "De gebruikersnaam die u heeft ingevuld is niet bekend"
        elif not dh.paswdok:
            ok = "Het wachtwoord dat u heeft ingevuld is niet correct"
        elif dh.blocked == "J":
            ok = 'Uw gebruikers-id is geblokkeerd'
    cregels = []
    regels = []
    if ok == 'ok':
        s = dh.start_session()
        c = SimpleCookie()
        c["usernaam"] = userid
        c["usernaam"]["path"] = ""
        c["usernaam"]["expires"] = _getdate(90000) # 3600 is huidige tijd (GMT + 1 uur): 86400 is 24 uur: samen dus morgen
        c["sessionid"] = s
        c["sessionid"]["path"] = ""
        c["sessionid"]["expires"] = _getdate(90000)
        cregels.append(c.output())
        ok = okmelding
        xslevel = dh.get_level()
        f = dh.get_attr('start')
        if not f:
            f = common.start_names[0]
        sp = f.split(':')
        if sp[0] == common.start_names[0]:	# startscherm
            l = Start(userid, xslevel)
        elif sp[0] == common.start_names[1]: 	# toon_klas
            l = ToonKlas(sp[1], userid, xslevel)
        elif sp[0] == common.start_names[2]: 	# sel_leerling
            l = SelectLeerling(sp[1], common.start_names[0], userid, s, xslevel)
        elif sp[0] == common.start_names[3]: 	# toon_klas
            l = ToonAbsenten(userid, xslevel)
        for x in l.regels:
            regels.append(x)
            #~ print x
        if not regels:
            regels = ['Welkom {}, '.format(userid), okregel]
    else:
        with open(os.path.join(common.filepad, "next.html"), "r") as f:
            for x in f:
                x = x.rstrip()
                if "%s" in x:
                    if "stylesheet" in x:
                        regels.append(x % common.httppad)
                elif "<!-- kop -->" in x:
                    regels.extend(common.printkop("Login fout"))
                elif "<!-- data -->" in x:
                    regels.append('<br /><div>%s</div>' % ok)
                else:
                    regels.append(x)
    return regels, cregels

class Start(object):
  def __init__(self, u, xslevel):
    self.regels = []
    with open(os.path.join(common.filepad, "start.html")) as fh:
        for x in fh:
            x = x.rstrip()
            if "%s" in x:
                if "stylesheet"in x:
                    self.regels.append(x % common.httppad)
                elif "<script" in x:
                    self.regels.extend(common.get_script())
                elif ".py" in x:
                    self.regels.append(x % common.cgipad)
                elif "option" in x:
                    for naam, id in leerkrachtenlijst()[0]:
                        self.regels.append(x % (id, naam))
                elif "Gebruikers" in x:
                    if xslevel in (1, '1'):
                        hj = 'submit'
                    else:
                        hj = 'hidden'
                    self.regels.append(x % hj)
            elif "<!-- kop -->" in x:
                for y in common.printkop("Startscherm", u):
                    self.regels.append(y)
            else:
                self.regels.append(x)

class Login(object):
  def __init__(self):
    self.regels = []
    with open(os.path.join(common.filepad, "login.html")) as fh:
        for x in fh:
            x.rstrip()
            if "%s" in x:
                if "stylesheet" in x:
                    self.regels.append(x % common.httppad)
                elif "<script" in x:
                    self.regels.extend(common.get_script())
                elif ".py" in x:
                    self.regels.append(x % common.cgipad)
            elif "<!-- kop -->" in x:
                self.regels.extend(common.printkop("Login"))
            else:
                self.regels.append(x)

class Logout(object):
    def __init__(self, userid, session):
        self.regels = []
        dh = User(userid, session, True)
        if dh.end_session():
            fn = os.path.join(common.filepad, "logout.html")
            kop = "Uitloggen"
        else:
            fn = os.path.join(common.filepad, "next.html")
            kop = "Login fout"
        with open(fn) as f:
            for x in f:
                if "%s" in x:
                    x = x.rstrip()
                    if "stylesheet" in x:
                        self.regels.append(x % common.httppad)
                    elif "button" in x:
                        self.regels.append(x % common.cgipad)
                    elif "uitgelogd" in x:
                        self.regels.append(x % userid)
                elif "<!-- kop -->" in x:
                    for y in common.printkop(kop, userid):
                        self.regels.append(y)
                elif "<!-- data -->" in x:
                    self.regels.append('<br /><div>%s</div>' % ok)
                else:
                    self.regels.append(x.strip())

