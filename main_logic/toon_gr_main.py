# naar het voorbeeld van adres_select_main.py in c:/c van papa/Mijn projecten/adressen

from school_globals import *
from Edex_objects import lijstGR
from Edex_objects import lijstLK

class toon_gr_main:
    def __init__(self,xslevel,u,s,editEntry=False,selId="0"):
        self.regels = []
        self.xslevel = xslevel
        self.lg = lijstGR().groep
        self.lk = lijstLK()
        self.tprog = "toon_groepen.py"
        self.wprog = "wijzig_groep.py"
        fh = open(filepad + "groepen.html")
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
                    hh = "doit_edit('tgr1','tgr2','0')"
                    self.regels.append(hh.join(hs))
            else:
                if x[:-1] == "<body>" and editEntry:
                    hh = "window.location='#wijzigdeze'"
                    self.regels.append('<body onload="%s">' % hh)
                elif x[:-1] == "<!-- kop -->":
                    for y in printkop("Lijst groepen",u):                  # gedefinieerd in school_globals
                        self.regels.append(y)
                elif x[:-1] == "<!-- contents -->":
                    if editEntry and selId == "0":
                        self.wijzigregel("0",u,s)
                    h = self.lg.keys()
                    h.sort()
                    for y in h:
                        if editEntry:
                            if y == selId:
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

    def toonregel(self,x,editEntry):
        y = self.lg[x]
        self.regels.append('    <tr>')
        self.regels.append('      <td valign="top">%s</td>' % y.naam)
        self.regels.append('      <td valign="top">%s</td>' % y.jaar)
        self.regels.append('      <td valign="top">%s</td>' % y.lknm)
        if self.xslevel > 2 or editEntry: # wijzigen niet toegestaan
            self.regels.append('      <td valign="top"><input type="button"  disabled="disabled" value="Wijzigen">')
        else:
            hh = ("doit_edit('tgr1','tgr2','%s')" % x)
            self.regels.append('      <td valign="top"><input type="submit" value="Wijzigen" onclick="%s">' % hh)
        self.regels.append('    </tr>')

    def wijzigregel(self,x,un,si):
        if x == "0":
            nm = ""
            jr = ""
            lk = "0"
        else:
            nm = self.lg[x].naam
            jr = self.lg[x].jaar
            lk = self.lg[x].lknm
        self.regels.append('    <tr>')
        self.regels.append('      <td><a name="wijzigdeze"></a>Naam:</td>')
        self.regels.append('      <td>Leerjaar:</td>')
        self.regels.append('      <td>Leerkracht:</td>:')
        self.regels.append('      <td>&nbsp;</td>')
        self.regels.append('    </tr>')
        self.regels.append('    <tr>')
        self.regels.append('    <form action="%s%s" method="post">' % (cgipad,self.wprog))
        self.regels.append('      <td valign="top"><input type="text" name="tnaam" id="tnaam" value="%s"/></td>' % nm)
        #~ self.regels.append('      <td valign="top"><input type="text" name="tjaar" id="tjaar" value="%s"/></td>' % jr)
        s = '      <td valign="top"><select name="selJR"><option>-- kies --</option>'
        for y in grptab:
            sl = ""
            if y == jr: sl = 'selected="selected" '
            if y == "H":
                z = "historisch"
            elif y == "S":
                z = "speciaal"
            else:
                z = y
            ss = ('<option %svalue="%s">%s</option>' % (sl,y,z))
            s = ('%s%s' % (s,ss))
        self.regels.append('%s</select></td>' % s)
        s = '      <td valign="top"><select name="selLK"><option>-- kies --</option>'
        for y in self.lk.lk:
            sl = ""
            if y[0] == lk: sl = 'selected="selected" '
            ss = ('<option %svalue="%s">%s</option>' % (sl,y[1],y[0]))
            s = ('%s%s' % (s,ss))
        self.regels.append('%s</select></td>' % s)
        self.regels.append('      <td valign="top">')
        self.regels.append('        <input type="hidden" name="hId" id="hId" value="%s" />' % x)
        self.regels.append('        <input type="hidden" name="wgr1" id="wgr1" value="%s" />' % un)
        self.regels.append('        <input type="hidden" name="wgr2" id="wgr2" value="%s" />' % si)
        h = "doit_woord('tnaam','Groepsnaam','wgr1','wgr2');return doit_retval;"
        self.regels.append('        <input type="submit" value="OK" onclick="%s"/><br />' % h)
        self.regels.append('        <input type="button" value="Cancel" onclick="javascript:history.go(/1)" />')
        self.regels.append('      </td>')
        self.regels.append('    </form>')
        self.regels.append('    </tr>')

if __name__ == '__main__':
    f = file("test.html","w")
    l = toon_gr_main(False,"")
    for x in l.regels:
        f.write("%s\n"% x)
    f.close()
