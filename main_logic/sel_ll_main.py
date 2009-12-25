from school_globals import *
from Edex_objects import LKgeg
from Edex_objects import zoekLL
from Edex_objects import lijstGR
from Edex_objects import lijstAbsent

class sel_ll_main:
  def __init__(self,zoek,vandaan,u,s,xslevel):
    self.regels = []
    self.lh = zoekLL(zoek, vandaan)
    if len(self.lh.lijst) == 1:
        #~ self.regels.append('Location: %stoon_llabsent.py?hId=%s&tla1=%s&tla2=%s' % (cgipad,self.lh.lijst[0][0],u,s)) hVan = sel_leerling
        hh = "'fThis'"
        self.regels.append('<html><head></head><body onload="document.getElementById(%s).submit()">' % hh)
        #~ self.regels.append('<form id="fThis" action="%shallo.py" method="post">' % cgipad)
        self.regels.append('<form id="fThis" action="%stoon_llabsent.py" method="post">' % cgipad)
        self.regels.append('<input type="hidden" id="hId" name="hId" value="%s"></input>' % self.lh.lijst[0][0])
        self.regels.append('<input type="hidden" id="hVan" name="hVan" value="sel_leerling-%s"></input>' % zoek)
        self.regels.append('<input type="hidden" id="tla1" name="tla1" value="%s"></input>' % u)
        self.regels.append('<input type="hidden" id="tla2" name="tla2" value="%s"></input>' % s)
        self.regels.append('</form></body></html>')
    else:
        self.ll_lijst(zoek,vandaan,u,xslevel)

  def ll_lijst(self,zoek,vandaan,u,xslevel):
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
            elif x.find("option") > -1:
                for g in groep:
                    self.regels.append("%s%s%s%s%s"% (hs[0],g,hs[1],g,hs[2][:-1]))
        else:
            if zoek != "" and x.find('<input type="submit" value="Zoek"') > -1:
                self.regels.append('<input type="button" value="Zoek" disabled="disabled"/>')
            elif x == "<!-- kop -->\n":
#                t = ('Gezocht op: naam(deel): %s' % zoek)
                for y in printkop('Gezocht op: naam(deel)',u,vandaan):                  # gedefinieerd in school_globals
                    self.regels.append(y)
            elif x.find("txtZoek") > -1 and zoek != "":
                self.regels.append(xx.replace("/>",(' value="%s"/>' % zoek)))
            elif x == "    <!-- contents -->\n":
                if len(self.lh.lijst) > 0:
                    for y in self.lh.lijst:
                        self.regels.append('    <tr>')
                        self.regels.append('     <td valign="top">%s</td>' % y[1])
                        self.regels.append('     <td valign="top">%s</td>' % y[2])
                        h = 0
                        if abs.ll.has_key(y[0]):
                            h = int(abs.ll[y[0]][0])
                            absdat = abs.ll[y[0]][2]
                        else:
                            absdat = "&nbsp;"
                        if xslevel > 2: # wijzigen niet toegestaan
                            self.regels.append('      <td valign="top">%s</td>' % afwstat[h])
                        else:
                            self.regels.append('      <td valign="top">')
                            self.regels.append('      <form id="wla-%s" action="%swijzig_llabsent.py" method="post">' % (y[0],cgipad))
                            self.regels.append('       <input type="hidden" name="hVan" id="hVan" value="sel_leerling-%s-%s" />' % (zoek,vandaan))
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
                            self.regels.append('      </form>')
                            self.regels.append('     </td>')
                        hh = '&nbsp;'
                        if h != 0: hh = absdat[:10]
                        self.regels.append('     <td valign="top">%s</td>' % hh)
                        self.regels.append('     <td valign="top">')
                        self.regels.append('     <form action="%stoon_llabsent.py" method="post">' % cgipad)
                        self.regels.append('       <input type="hidden" name="hVan" id="hVan" value="sel_leerling-%s-%s" />' % (zoek,vandaan))
                        self.regels.append('       <input type="hidden" name="hId" id="hId" value="%s" />' % y[0])
                        if xslevel > 2: # wijzigen niet toegestaan
                            self.regels.append('        <input type="submit" disabled="disabled" value="Details"/>')
                        else:
                            self.regels.append('  	  <input type="hidden" name="tla1-%s" id = "tla1-%s"/>' % (y[0],y[0]))
                            self.regels.append('  	  <input type="hidden" name="tla2-%s" id = "tla2-%s"/>' % (y[0],y[0]))
                            hh = ("doit('tla1-%s','tla2-%s')" % (y[0],y[0]))
                            self.regels.append('        <input type="submit" value="Details" onclick="%s"/>' % hh)
                        self.regels.append('      </form>')
                        self.regels.append('     </td>')
                        self.regels.append('    </tr>')
                else:
                    self.regels.append('    <tr><td colspan="3">Geen gegevens gevonden</td></tr>')
            else:
                self.regels.append(xx)
    fh.close()

if __name__ == '__main__':
    zoek = "visser"
    vandaan = ""
    h = sel_ll_main(zoek,vandaan)
    for x in h.regels:
        print x

