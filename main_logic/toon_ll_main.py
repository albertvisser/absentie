# naar het voorbeeld van adres_select_main.py in c:/c van papa/Mijn projecten/adressen

from school_globals import *
from Edex_objects import lijstLL
from Edex_objects import LLgeg
from Edex_objects import lijstGR0
from Edex_objects import GRgeg

class toon_ll_main:
    def __init__(self,xslevel,u,s,editEntry=False,selId="0"):
        self.regels = []
        self.xslevel = xslevel
        self.ll = lijstLL()
        self.tprog = "toon_leerlingen.py"
        self.wprog = "wijzig_leerling.py"
        fh = open(filepad + "leerlingen.html")
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
                    hh = "doit_edit('tll1','tll2','0')"
                    self.regels.append(hh.join(hs))
            else:
                if x[:-1] == "<body>" and editEntry:
                    hh = "window.location='#wijzigdeze'"
                    self.regels.append('<body onload="%s">' % hh)
                elif x[:-1] == "<!-- kop -->":
                    for y in printkop("Lijst leerlingen",u):                  # gedefinieerd in school_globals
                        self.regels.append(y)
                elif x[:-1] == "<!-- contents -->":
                    if editEntry and selId == "0":
                        self.wijzigregel("0",u,s)
                    h = self.ll.ll.keys()
                    #-- dit is het punt waarop de sortering kan worden aangepast
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

#~ LLgeg[id].naam.naam
                    #~ .vn
                    #~ .vv
                    #~ .an
            #~ .geboren (ddmmjjee)
            #~ .gesl (M,V)
            #~ .auto (0,1)
            #~ .groep (id)

    def toonregel(self,x,editEntry):
        y = LLgeg(x)
        z = GRgeg(y.groep)
        z.read()
        self.regels.append('    <tr>')
        self.regels.append('      <td valign="top">%s</td>' % y.naam.naam)
        self.regels.append('      <td valign="top">%s-%s-%s</td>' % (y.geboren.dd,y.geboren.mm,y.geboren.jr))
        self.regels.append('      <td valign="top">%s</td>' % gsltab[y.gesl])
        #~ self.regels.append('      <td valign="top">%s</td>' % auttab[y.auto])
        self.regels.append('      <td valign="top">%s</td>' % (z.lknm))
        if self.xslevel > 2 or editEntry: # wijzigen niet toegestaan
            self.regels.append('      <td valign="top"><input type="button"  disabled="disabled" value="Wijzigen">')
        else:
            hh = ("doit_edit('tll1','tll2','%s')" % x)
            self.regels.append('      <td valign="top"><input type="submit" value="Wijzigen" onclick="%s">' % hh)
        self.regels.append('    </tr>')

    def wijzigregel(self,x,un,si):
        if x == "0":
            vn = ""
            vv = ""
            an = ""
            dd = ""
            mm = ""
            jr = ""
        else:
            y = LLgeg(x)
            vn = y.naam.vn
            vv = y.naam.vv
            an = y.naam.an
            dd = y.geboren.dd
            mm = y.geboren.mm
            jr = y.geboren.jr
        self.regels.append('    <tr>')
        self.regels.append('      <td class="hl"><a name="wijzigdeze"></a>Voornaam / voorvoegsel / achternaam:</td>')
        self.regels.append('      <td class="hl">Geboortedatum:</td>')
        self.regels.append('      <td class="hl">Geslacht</td>:')
        #~ self.regels.append('      <td class="hl">Oorsprong</td>:')
        self.regels.append('      <td class="hl">Groep</td>:')
        self.regels.append('      <td class="hl">&nbsp;</td>')
        self.regels.append('    </tr>')
        self.regels.append('    <tr>')
        self.regels.append('    <form action="%s%s" method="post">' % (cgipad,self.wprog))
        self.regels.append('      <td valign="top">')
        self.regels.append('        <input type="text" name="tvnaam" id="tvnaam" value="%s"/>' % vn)
        self.regels.append('        <input type="text" size="5" name="ttus" id="ttus" value="%s"/>' % vv)
        self.regels.append('        <input type="text" name="tanaam" id="tanaam" value="%s"/>' % an)
        self.regels.append('      </td>')
        self.regels.append('      <td valign="top">')
        self.regels.append('        <input type="text" name="tdag" id="tdag" size="2" value="%s"/>-' % dd)
        self.regels.append('        <input type="text" name="tmaand" id="tmaand" size="2" value="%s"/>-' % mm)
        self.regels.append('        <input type="text" name="tjaar" id="tjaar" size="4" value="%s"/></td>' % jr)
        self.regels.append('      </td>')
        s = '      <td valign="top"><select name="selgesl">'
        for z in gsltab.keys():
            sl = ""
            if x != "0":
                if z == y.gesl: sl = 'selected="selected" '
            ss = ('<option %svalue="%s">%s</option>' % (sl,z,gsltab[z]))
            s = ('%s%s' % (s,ss))
        self.regels.append('%s</select></td>' % s)
        #~ s = '      <td valign="top"><select name="selaut">'
        #~ for z in auttab.keys():
            #~ sl = ""
            #~ if x != "0":
                #~ if z == y.auto: sl = 'selected="selected" '
            #~ ss = ('<option %svalue="%s">%s</option>' % (sl,z,auttab[z]))
            #~ s = ('%s%s' % (s,ss))
        #~ self.regels.append('%s</select></td>' % s)
        s = '      <td valign="top"><select name="selgrp">'
        lg = lijstGR0()
        for z in lg.lg:
            sl = ""
            if x != "0":
                if z[1] == y.groep: sl = 'selected="selected" '
            ss = ('<option %svalue="%s">%s</option>' % (sl,z[1],z[0]))
            s = ('%s%s' % (s,ss))
        self.regels.append('%s</select></td>' % s)
        self.regels.append('      <td valign="top">')
        self.regels.append('        <input type="hidden" name="hId" id="hId" value="%s" />' % x)
        self.regels.append('        <input type="hidden" name="wll1" id="wll1" value="%s" />' % un)
        self.regels.append('        <input type="hidden" name="wll2" id="wll2" value="%s" />' % si)
        hh = "doit_naam('tvnaam','tanaam','wll1','wll2');return doit_retval"
        self.regels.append('        <input type="submit" value="OK" onclick="%s"/><br />' % hh)
        self.regels.append('        <input type="button" value="Cancel" onclick="javascript:history.go(-1)" />')
        self.regels.append('      </td>')
        self.regels.append('    </form>')
        self.regels.append('    </tr>')

if __name__ == '__main__':
    f = file("test.html","w")
    l = toon_ll_main(True,"0")
    for x in l.regels:
        f.write("%s\n"% x)
    f.close()
