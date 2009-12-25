from school_globals import *
from Edex_objects import lijstLLbijLK
from Edex_objects import lijstAbsent

class toon_kl_main:
  def __init__(self,selId,u,xslevel):
    self.regels = []
    klas = lijstLLbijLK(selId)
    abs = lijstAbsent()
    fh = open(filepad + "toon_klas.html")
    for x in fh.readlines():
        xx = x[:-1]
        h = x.find("%s")
        if h > -1:
            hs = xx.split("%s")
            if x.find("stylesheet") > -1:
                self.regels.append("%s%s%s" % (hs[0],httppad,hs[1]))
            elif x.find("<script") > -1:
                self.regels.append(hs[0])
                f2 = file(filepad + 'check.js')
                for x in f2.readlines():
                    self.regels.append(x[:-1])
                f2.close()
                self.regels.append(hs[1])
            elif x.find("action") > -1:
                self.regels.append("%s%s%s" % (hs[0],cgipad,hs[1]))
            elif x.find("hVan") > -1:
                self.regels.append("%s%s%s" % (hs[0],selId,hs[1]))
            elif x.find("option") > -1:
                for g in groep:
                    self.regels.append("%s%s%s%s%s"% (hs[0],g,hs[1],g,hs[2][:-1]))
        else:
            if x == "<!-- kop -->\n":
#                t = "Gezocht op: groep van " + klas.lk.naam.split()[0]
                for y in printkop("Gezocht op: groep ",u):                  # gedefinieerd in school_globals
                    self.regels.append(y)
            elif x == "    <!-- contents -->\n":
                lknm = klas.lk.naam.vn
                if len(klas.ll) > 0:
                    for y in klas.ll:
                        self.regels.append('    <tr>')
                        self.regels.append('     <td valign="top">%s</td>' % y[1].naam)
                        self.regels.append('     <td valign="top">%s</td>' % lknm)
                        h = 0
                        if abs.ll.has_key(y[0]):
                            h = int(abs.ll[y[0]][0])
                            absdat = abs.ll[y[0]][2]
                        else:
                            absdat = "&nbsp;"
                        if xslevel > 2: # wijzigen niet toegestaan
                            self.regels.append('     <td valign="top">%s</td>' % afwstat[h])
                        else:
                            self.regels.append('      <td valign="top">')
                            self.regels.append('      <form id="wla-%s" action="%swijzig_llabsent.py" method="post">' % (y[0],cgipad))
                            self.regels.append('       <input type="hidden" name="hVan" id="hVan" value="toon_klas-%s" />' % selId)
                            self.regels.append('       <input type="hidden" name="hId" id="hId" value="%s" />' % y[0])
                            self.regels.append('  	  <input type="hidden" name="wla1-%s" id = "wla1-%s"/>' % (y[0],y[0]))
                            self.regels.append('  	  <input type="hidden" name="wla2-%s" id = "wla2-%s"/>' % (y[0],y[0]))
                            hh = ("doit_sub('wla-%s','wla1-%s','wla2-%s')" % (y[0],y[0],y[0]))
                            self.regels.append('  	  <select name="selStat" id="selStat" onchange="%s" >' % hh)
                            i = 0
                            for z in afwstat:
                                hs = ""
                                if i == h: hs = 'selected="selected" '
                                self.regels.append('	    <option %svalue="%i">%s</option>' % (hs,i,z))
                                i = i + 1
                            self.regels.append('	  </select>')
                            self.regels.append('     </form>')
                            self.regels.append('     </td>')
                        hh = '&nbsp;'
                        if h != 0: hh = absdat[:10]
                        self.regels.append('     <td valign="top">%s</td>' % hh)
                        if xslevel > 2: # wijzigen niet toegestaan
                            self.regels.append('     <td valign="top"><input type="button" value="Details" disabled="disabled"/></td>')
                        else:
                            self.regels.append('      <td valign="top">')
                            self.regels.append('    <form action="%stoon_llabsent.py" method="post">' % cgipad)
                            self.regels.append('       <input type="hidden" name="hVan" id="hVan" value="toon_klas-%s" />' % selId)
                            self.regels.append('       <input type="hidden" name="hId" id="hId" value="%s" />' % y[0])
                            self.regels.append('  	  <input type="hidden" name="tla1-%s" id = "tla1-%s"/>' % (y[0],y[0]))
                            self.regels.append('  	  <input type="hidden" name="tla2-%s" id = "tla2-%s"/>' % (y[0],y[0]))
                            hh = ("doit('tla1-%s','tla2-%s')" % (y[0],y[0]))
                            self.regels.append('        <input type="submit" value="Details" onclick="%s"/>' % hh)
                            self.regels.append('     </form>')
                            self.regels.append('     </td>')
                        self.regels.append('    </tr>')
                else:
                    self.regels.append('<tr><td colspan="3">Geen leerlingen gevonden bij %s</td></tr>' % lknm)
            else:
                self.regels.append(x[:-1])
    fh.close()

if __name__ == '__main__':
    selId = "00003"
    h = toon_kl_main(selId,3)
    for x in h.regels:
        print x
