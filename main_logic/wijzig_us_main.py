from school_globals import *
from school_user import User
from school_user import UserLijst

class wijzig_us_main:
    def __init__(self,id,nieuw):
        self.ok = False
        self.uid = id
        self.nw = nieuw
        self.start = ''

    def addArg(self,naam,waarde):
        if naam == "type":
            self.utype = waarde
        elif naam == "blok":
            self.blck = waarde
        elif naam == "start":
            h = self.start.split(':')
            if len(h) > 1:
                self.start = waarde + ':' + h[1]
            else:
                self.start = waarde
        elif naam == "met":
            h = self.start.split(':')
            self.start = h[0] + ':' + waarde

    def doe(self):
        self.exists = False
        self.ok = False
        u = User(self.uid)
        u.read()
        if u.found:
            self.exists = True
        if self.nw == '0':
            if not self.exists:
                self.ok = True
                u.setPass('begin') # user wordt hierbij initieel opgevoerd
        else:
            if self.exists:
                self.ok = True
        if self.ok:
            u.utype = self.utype
            u.blck = self.blck
            u.start = self.start
            u.write()

class wijzig_pw_vraag: # opbouwen scherm om wachtwoord te wijzigen
    def __init__(self,uid,van):
        self.regels = []
        fh = open(filepad + "newpw.html")
        for x in fh.readlines():
            h = x.find("%s")
            if h > -1:
                hs = x[:-1].split("%s")
                if x.find("stylesheet") > -1:
                    self.regels.append(httppad.join(hs))
                elif x.find("<script") > -1:
                    self.regels.append(hs[0])
                    f2 = file(filepad + 'check.js')
                    for x in f2.readlines():
                        self.regels.append(x[:-1])
                    f2.close()
                    self.regels.append(hs[1])
                elif x.find('action=') > -1:
                    self.regels.append(cgipad.join(hs))
                elif x.find('id="tNaam"') > -1:
                    self.regels.append(uid.join(hs))
                elif x.find('id="hVan"') > -1:
                    self.regels.append(van.join(hs))
                elif x.find('input type="submit"') > -1:
                    hh = "doit('wu1','wu2','0')"
                    self.regels.append(hh.join(hs))
            else:
                if x[:-1] == "<!-- kop -->":
                    for y in printkop("Wachtwoord wijzigen"):                  # gedefinieerd in school_globals
                        self.regels.append(y)
                #~ elif x[:-1] == "<body>" and editEntry:
                    #~ hh = "window.location='#wijzigdeze'"
                    #~ self.regels.append('<body onload="%s">' % hh)
                else:
                    self.regels.append(x[:-1])
        fh.close()

class wijzig_pw_main:
    def __init__(self,uid,oldpw,newpw):
        # maak user
        u = User(uid,oldpw)
        if u.paswdok:
            # wijzig wachtwoord
            u.setPass(newpw)
        # klaar
        self.ok = u.paswdok

def test():
    #~ pw = wijzig_pw_main('snork','einde','opnieuw')
    #~ print pw.ok
    #~ return
    #~ pw = wijzig_pw_vraag('leerkracht','toon_users')
    #~ f = file("test.html","w")
    #~ for x in pw.regels:
        #~ f.write("%s\n" % x)
    #~ f.close()
    #~ return
    #~ dh = UserLijst()
    #~ for x in dh.Items:
        #~ print x
    nw = "0"
    wu = wijzig_us_main("snork",nw)
    #~ wu.addArg("type","2")
    #~ wu.addArg("blok","N")
    wu.addArg("start","toon_klas")
    wu.addArg("met","Ben")
    wu.doe()
    if nw == "0" and wu.exists:
        print "opgegeven usernaam komt al voor"
    elif nw != "0" and not wu.exists:
        print "opgegeven user niet gevonden"
    elif not wu.ok:
        print "toevoegen/wijzigen is niet gelukt"
    dh = UserLijst()
    for x in dh.Items:
        print x

if __name__ == '__main__':
    test()
