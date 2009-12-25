# naar het voorbeeld van adres_select_main.py in c:/c van papa/Mijn projecten/adressen

from school_globals import *
from school_user import UserLijst
from school_user import User

class toon_us_main:
    def __init__(self,xslevel,u,s,editEntry=False,selId="0"):
        self.editEntry = editEntry
        newUser = False
        if selId == "0":
            newUser = True
        self.regels = []
        self.xslevel = xslevel
        self.ul = UserLijst()
        self.tprog = "toon_users.py"
        self.wprog = "wijzig_user.py"
        fh = open(filepad + "users.html")
        spaar = False
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
                    if not self.editEntry:
                        self.regels.append(cgipad.join(hs))
                elif x.find('input type="submit"') > -1:
                    hh = "doit_edit('tu1','tu2','0')"
                    self.regels.append(hh.join(hs))
            else:
                if x[:-1] == "<body>" and self.editEntry:
                    hh = "window.location='#wijzigdeze'"
                    self.regels.append('<body onload="%s">' % hh)
                elif x[:-1] == "<!-- kop -->":
                    for y in printkop("Lijst gebruikers",u):                  # gedefinieerd in school_globals
                        self.regels.append(y)
                elif "wijzigdeze" in x:
                    spaar = True
                    self.trgls = [x[:-1]]
                elif spaar:
                    self.trgls.append(x[:-1])
                    if "</form>" in x:
                        spaar = False
                        if self.editEntry and self.newUser:
                            y = ['','',xtypes.keys()[1],btypes.keys()[1],snames[0]] # defaults
                            self.maakregel(y,u,s)
                        h = self.ul.Items
                        for y in h:
                            if self.editEntry and y[0] == selId:
                                self.maakregel(y,u,s)
                            else:
                                self.maakregel(y)
                else:
                    self.regels.append(x[:-1])
        fh.close()

    def maakregel(self,x,un="",so=""):
        for y in self.trgls:
            s = y.split("$s")
            if "wijzigdeze" in y and self.editEntry:
                self.regels.append(y)
            elif "<form" in y:
                if self.editEntry:
                    self.regels.append("".join(s) % (cgipad,self.wprog))
                else:
                    self.regels.append(s[0])
            elif "tNaam" in y:
                if self.editEntry:
                    self.regels.append("".join(s) % x[0])
                else:
                    self.regels.append("%s%s%s" % (s[0],xtypes[x[2]],s[-1]))
            elif "sType" in y:
                if self.editEntry:
                    self.regels.append("%s%s" % s[0],s[1])
                    for i in xtypes.keys():
                        si = ''
                        if i == x[2]:
                            si = ' selected="selected"'
                        self.regels.append(s[2] % (si,i,xtypes[i]))
                    self.regels.append("%s%s" % s[-2],s[-1])
                else:
                    self.regels.append("%s%s%s" % (s[0],xtypes[x[2]],s[-1]))
            elif "sStart" in y:
                if self.editEntry:
                    self.regels.append("%s%s" % s[0],s[1])
                    h = x[4].split(':')
                    if h[0] == '':
                        h[0] = snames[0]
                    for i in range(4):
                        si = ''
                        if snames[i] == h[0]:
                            si = ' selected="selected"'
                        self.regels.append(s[2] % (si,snames[i],snames[i]))
                    self.regels.append("%s%s" % s[-2],s[-1])
                else:
                    h = x[4].split(':')
                    if h[0] == '': h[0] = snames[0]
                    self.regels.append("%s%s%s" % (s[0],h[0],s[-1]))
            elif "tMet" in y:
                if self.editEntry:
                h = x[4].split(':')
                hh = ''
                if len(h) > 1: hh = h[1]
                self.regels.append(y % hh)
                    self.regels.append("".join(s) % )
                else:
                    hh = '&nbsp;'
                    if len(h) > 1: hh = h[1]
                    self.regels.append("%s%s%s" % (s[0],hh,s[-1]))
            elif "sBlok" in y:
                if self.editEntry:
                    self.regels.append("%s%s" % s[0],s[1])
                    for i in btypes.keys():
                        si = ''
                        if i == x[3]:
                            si = ' selected="selected"'
                        self.regels.append(s[2] % (si,i,btypes[i]))
                        self.regels.append()
                    self.regels.append("%s%s" % s[-2],s[-1])
                else:
                    self.regels.append("%s%s%s" % (s[0],btypes[x[3]],s[-1]))
            elif "hPw" in y:
                if self.editEntry:
                    if newuser:
                        h = (s[1] % "0")
                        self.regels.append('%s%sVoor een nieuwe gebruiker wordt automatisch een standaard wachtwoord opgevoerd%s' % (s[0],h),s[-1])
                    else:
                        h = (s[1] % "N")
                        hh = (s[-2] % "doit_wpw('wu1','wu2','J')")
                        self.regels.append('%s%s%s%s' % (s[0],h,hh,s[-1]))
                else:
                    h = x[1]
                    if h == '': h = '&nbsp;'
                    self.regels.append("%s%s%s" % (s[0],h,s[-1]))
            elif "hVan" in y:
                # <input type="hidden" name="wu1" id="wu1" value="%s" />
                # <input type="hidden" name="wu2" id="wu2" value="%s" />
                # <input type="submit" value="OK" onclick="%s"/>
                # <input type="button" value="Cancel" onclick="javascript:history.go(-1)" />
                if self.editEntry:
                    hh = ("doit_woord('tNaam','Gebruikersnaam','wu1','wu2');return document.doit_retval")
                    h = s[2] % (un,so,hh)
                    self.regels.append("%s%s%s" % (s[0],s[1],h,s[-1]))
                else:
                    if self.xslevel > 2 or editEntry: # wijzigen niet toegestaan
                        h = (s[1] % ('button','disabled="disabled')
                    else:
                        hh = ("doit_edit('tu1','tu2','%s')" % x[0])
                        h = (s[1] % ('submit',('onclick="%s"' % hh)))
                    self.regels.append("%s%s%s" % (s[0],h,s[-1]))
            elif "</form>" in y:
                if self.editEntry:
                    self.regels.append("".join(s))
                else:
                    self.regels.append(s[1])

if __name__ == '__main__':
    f = file("test.html","w")
    l = toon_us_main(1,'woefdram','magiokis',False,"0")
    for x in l.regels:
        f.write("%s\n"% x)
    f.close()
