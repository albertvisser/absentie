# naar het voorbeeld van adres_select_main.py in c:/c van papa/Mijn projecten/adressen

from school_globals import *
from Edex_objects import LKgeg
from Edex_objects import lijstLK
from Edex_objects import lijstGR0

class toon_lk_main:
    def __init__(self,xslevel,u,s,editEntry=False,selId="0"):
        self.regels = []
        self.xslevel = xslevel
        self.lk = lijstLK()
        self.tprog = "toon_leerkrachten.py"
        self.wprog = "wijzig_leerkracht.py"
        fh = open(filepad + "leerkrachten.html")
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
                    if not editEntry:
                        self.regels.append(cgipad.join(hs))
                elif x.find('input type="submit"') > -1:
                    hh = "doit_edit('tlk1','tlk2','0')"
                    self.regels.append(hh.join(hs))
            else:
                if x[:-1] == "<body>" and editEntry:
                    hh = "window.location='#wijzigdeze'"
                    self.regels.append('<body onload="%s">' % hh)
                elif x[:-1] == "<!-- kop -->":
                    for y in printkop("Lijst leerkrachten",u):                  # gedefinieerd in school_globals
                        self.regels.append(y)
                elif x[:-1] == "<!-- contents -->":
                    if editEntry and selId == "0":
                        self.wijzigregel("0",u,s)
                    h = self.lk.lk
                    for y in h:
                        if editEntry:
                            if y[1] == selId:
                                self.wijzigregel(y,u,s)
                            else:
                                self.toonregel(y,True)
                        else:
                            self.toonregel(y,False)
                elif editEntry and x[:-1] == "</form>":
                    pass
                else:
                    self.regels.append(x[:-1])
        fh.close()

#~ lijstLK.lk: [lknm,lkid]
#~ LKgeg.id
        #~ .naam.vn
                #~ .vv
                #~ .an
                #~ .naam
        #~ .groep: [id,id,id]
        #~ .grpnm: [naam,naam,naam]

    def toonregel(self,x,editEntry):
        y = LKgeg(x[1])
        self.regels.append('    <tr>')
        self.regels.append('      <td valign="top">%s</td>' % y.naam.naam)
        if len(y.grpnm) == 0:
            s = "&nbsp;"
        else:
            s = y.grpnm[0]
            for i in range(1,len(y.grpnm)):
                s = ("%s, %s" %  (s,y.grpnm[i]))
        self.regels.append('      <td valign="top">%s</td>' % s)
        if self.xslevel > 2 or editEntry: # wijzigen niet toegestaan
            self.regels.append('      <td valign="top"><input type="button"  disabled="disabled" value="Wijzigen" >')
        else:
            hh = ("doit_edit('tlk1','tlk2','%s')" % y.id)
            self.regels.append('      <td valign="top"><input type="submit" value="Wijzigen" onclick="%s">' % hh)
        self.regels.append('    </tr>')

    def wijzigregel(self,x,un,si):
        lg = lijstGR0()
        if x == "0":
            vn = ""
            vv = ""
            an = ""
            gl = []
        else:
            y = LKgeg(x[1])
            vn = y.naam.vn
            vv = y.naam.vv
            an = y.naam.an
            gl = y.groep
        #-- het navolgende stukje is leuk als je een lijst langer dan een scherm hebt
        self.regels.append('    <tr>')
        self.regels.append('      <td><a name="wijzigdeze"></a>Voornaam / tussenvoegsel / achternaam:</td>')
        self.regels.append('      <td>Groepen:</td>')
        self.regels.append('      <td>&nbsp;</td>')
        self.regels.append('    </tr>')
        self.regels.append('    <tr>')
        self.regels.append('    <form action="%s%s" method="post">' % (cgipad,self.wprog))
        self.regels.append('      <td valign="top">')
        self.regels.append('        <input type="text" name="tvnaam" id="tvnaam" value="%s"/>' % vn)
        self.regels.append('        <input type="text" size="5" name="ttus" id="ttus" value="%s"/>' % vv)
        self.regels.append('        <input type="text" name="tanaam" id="tanaam" value="%s"/>' % an)
        self.regels.append('      </td>')
        if x == "0" or len(y.grpnm) == 0:
            s = "&nbsp;"
        else:
            s = y.grpnm[0]
            for i in range(1,len(y.grpnm)):
                s = ("%s, %s" %  (s,y.grpnm[i]))
        self.regels.append('      <td valign="top">%s</td>' % s)
        self.regels.append('      <td valign="top">')
        self.regels.append('        <input type="hidden" name="hId" id="hId" value="%s" />' % x)
        self.regels.append('        <input type="hidden" name="wlk1" id="wlk1" value="%s" />' % un)
        self.regels.append('        <input type="hidden" name="wlk2" id="wlk2" value="%s" />' % si)
        hh = "doit_naam('tvnaam','tanaam','wlk1','wlk2');return doit_retval"
        self.regels.append('        <input type="submit" value="OK" onclick="%s"/><br />' % hh)
        self.regels.append('        <input type="button" value="Cancel" onclick="javascript:history.go(-1)" />')
        self.regels.append('      </td>')
        self.regels.append('    </form>')
        self.regels.append('    </tr>')

if __name__ == '__main__':
    f = file("test.html","w")
    l = toon_lk_main(1,False,"")
    for x in l.regels:
        f.write("%s\n"% x)
    f.close()
