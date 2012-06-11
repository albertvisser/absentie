#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import common
from Edex_objects import Leerling, leerlingenlijst, groependetailslijst
from Edex_objects import absenties, absentenlijst

class today: # pre-2.3 support
    def __init__(self):
        t = time.gmtime()
        self.day = t[2]
        self.month = t[1]
        self.year = t[0]

row, endrow = '    <tr>', '    </tr>'
col, endcol = '      <td valign="top">', '</td>'
coltext = '{}%s{}'.format(col, endcol)
button_disabled = '<input type="button"  disabled="disabled" value="Wijzigen" >'
button = '<input type="%s" value="%s" onclick="%s">'
header = """\
<br />Geschiedenis:
<table><tr>
  <th>datum/tijd</th><th>&nbsp;</th><th>status</th><th>&nbsp;</th><th>evt. reden</th>
</tr>
"""
form, endform = '    <form action="%s%s" method="post">', '    </form>'
select, endselect = '        <select name="{0}" id="{0}{1}">', '        </select>'
selected_text = ' selected="selected"'
option = '          <option%s value="%s">%s</option>'
input_text = '        <input type="{0}" name="{1}" id="{1}" value="{2}"/>'
wijzigform = '      <form id="wla-%s" action="%swijzig_llabsent.py" method="post">'
toonform = '    <form action="%stoon_llabsent.py" method="post">'
komtvanform = '<form id="fThis" action="%s%s.py" method="post">'
herkomst = '\n'.join(('    ' + input_text.format('hidden', 'hVan', 'toon_absent'),
    '    ' + input_text.format('hidden', 'hId', '%s')))
target = '\n'.join(('    ' + input_text.format('hidden', '{0}la1-{1}', ''),
    '    ' + input_text.format('hidden', '{0}la2-{1}', '')))
endtable = '</table>'

class ToonAbsenten(object):
  def __init__(self, u, xslevel):
    self.regels = []
    sZoek = ""
    abs = absentenlijst()
    ll = leerlingenlijst()[0]
    gr = groependetailslijst()[0]
    with open(os.path.join(common.filepad, "toon_absent.html")) as fh:
        for x in fh:
            x = x.rstrip()
            if "%s" in x:
                if "stylesheet" in x:
                    self.regels.append(x % common.httppad)
                elif "<script" in x:
                    self.regels.extend(common.get_script())
                elif "action" in x:
                    self.regels.append(x % common.cgipad)
                elif "hVan" in x:
                    self.regels.append(x % sel_id)
                elif "option" in x:
                    for g in groep:
                        self.regels.append(x % (g, g))
            elif "<!-- kop -->" in x:
                self.regels.extend(common.printkop("Lijst absente leerlingen ", u))
            elif "<!-- contents -->" in x:
                aantabs = 0
                for y, z in abs.items():    # absent, gegevens
                    abstat = z[0]
                    if abstat != "0":
                        aantabs = aantabs + 1
                        absrdn = z[1]
                        absdat = z[2]
                        leerl = ll[y]
                        llnm = leerl[0]
                        llgr = gr[leerl[1]]
                        lknm = llgr[2][0]
                        self.regels.append(row)
                        self.regels.append(coltext % str(llnm))
                        self.regels.append(coltext % lknm)
                        if xslevel > 2: # wijzigen niet toegestaan
                            self.regels.append(coltext % common.afwstat[int(abstat)])
                        else:
                            self.regels.append(col)
                            self.regels.append(wijzigform % (y, common.cgipad))
                            self.regels.append(herkomst % y)
                            self.regels.append(target.format('w', y))
                            hh = "doit_sub('wla-{0}','wla1-{0}','wla2-{0}')".format(
                                y)
                            hh = ' onchange="%s"' % hh
                            self.regels.append(select.format('selStat', hh))
                            for ix, z in enumerate(common.afwstat):
                                hs = selected_text if str(ix) == abstat else ''
                                self.regels.append(option % (hs, ix, z))
                            self.regels.append(endselect)
                            self.regels.append(endform)
                            self.regels.append(endcol)
                        self.regels.append(coltext % absdat[:10])
                        if xslevel > 2: # wijzigen niet toegestaan
                            self.regels.append(coltext % button_disabled)
                        else:
                            self.regels.append(col)
                            self.regels.append(toonform % common.cgipad)
                            self.regels.append(herkomst % y)
                            self.regels.append(target.format('t', y))
                            hh = "doit('tla1-{0}','tla2-{0}')".format(y)
                            self.regels.append(button % ('submit', 'Toon/Wijzig', hh))
                            self.regels.append(endform)
                            self.regels.append(endcol)
                        self.regels.append(endrow)
                if aantabs == 0:
                    self.regels.append(niks_gevonden)
            else:
                self.regels.append(x)

class ToonAbsentie(object):
  def __init__(self, u, sel_id, meld, vandaan, selopt=""):
    self.regels = []
    ll = Leerling(sel_id)
    #~ from datetime import date
    #~ dmy = date.today()
    dmy = today()
    with open(os.path.join(common.filepad, "toon_leerling.html")) as fh:
        for x in fh.readlines():
            x = x.strip()
            if "%s" in x:
                if "stylesheet" in x:
                    self.regels.append(x % common.httppad)
                elif "<script" in x:
                    self.regels.extend(common.get_script())
                elif "form action" in x:
                    self.regels.append(x % common.cgipad)
                elif "Naam" in x:
                    self.regels.append(x % ll.naam)
                elif "hTerug" in x:
                    self.regels.append(x % vandaan)
                elif "option"in x:
                    for ix, s in enumerate(common.afwstat):
                        sh = ""
                        if (selopt and ix == int(selopt)) or ix == int(ll.code):
                            sh = selected_text
                        self.regels.append(option % (sh, ix, s))
                elif "textarea" in x:
                    self.regels.append(x % ll.reden)
                elif "hId" in x:
                    self.regels.append(x % sel_id)
                elif "colspan" in x:
                    if meld != "":
                        self.regels.append(x % meld)
            else:
                if "<!-- kop -->" in x:
                    self.regels.extend(common.printkop("Details van leerling", u,
                        vandaan))
                elif "selDag" in x:
                    self.regels.append(x)
                    for i in range(1,32):
                        y = selected_text if i == dmy.day else ''
                        self.regels.append(option % (y, i, i))
                elif "selMnd" in x:
                    self.regels.append(x)
                    for i in range(1,13):
                        y = selected_text if i == dmy.month else ''
                        self.regels.append(option % (y, i, i))
                elif "selJaar"  in x:
                    self.regels.append(x)
                    for i in range(dmy.year - 1, dmy.year + 2):
                        y = selected_text if i == dmy.year else ''
                        self.regels.append(option % (y, i, i))
                elif "<!-- AbsentHist -->" in x:
                    self.regels.append(header)
                    for x in absenties(sel_id):
                        h1 = common.afwstat[int(x[1])]
                        h2 = x[2] or "&nbsp;"
                        self.regels.append('<tr><td>%s</td><td>&nbsp;</td><td>%s'
                            '</td><td>&nbsp;</td><td>%s</td></tr>' % (x[0], h1, h2))
                    self.regels.append(endtable)
                else:
                    self.regels.append(x)


htmlbegin = '<html><head></head><body onload="document.getElementById(%s).submit()">'
htmleind = '</form></body></html>'
class WijzigAbsentie(object):
    def __init__(self, sel_id, newstat, reden, komt_van, u, s, kwam_van, newdata=""):
        self.fout = ""
        if sel_id == "0":
            self.fout = "U moet wel een sleutelwaarde opgeven"
        elif newstat == "":
            self.fout = "U moet wel een status opgeven"
        elif reden == "" and newstat == "2":
            self.fout = "U moet wel een reden opgeven"

        sel_klas = kwam_van = sel_van = ''
        if komt_van != "":
            h = komt_van.split("-")
            if len(h) > 0:
                komt_van = h[0]
            if len(h) > 1:
                sel_klas = h[1]
            if len(h) > 2:
                kwam_van = h[2]
            if len(h) > 3:
                sel_van = h[3]
        else:
            komt_van = "toon_leerling"
        if kwam_van != "":
            h = kwam_van.split("-")
            if len(h) > 1:
                sel_van = h[1]
        else:
            kwam_van = "toon_leerling"
        if sel_van != '':
            kwam_van += '.' + sel_van

        if self.fout == "":
            ll = Leerling(sel_id)
            h = time.localtime()
            if newdata != "":
                dt = '-'.join((newdata[6:],newdata[4:6],newdata[:4]))
            else:
                dt = '%02i-%02i-%04i'% (h[2], h[1], h[0])
            dt += ";%02i:%02i:%02i" % (h[3],h[4],h[5])
            ll.add_absentie(newstat, reden, dt)

        self.regels = []
        self.regels.append(htmlbegin % "'fThis'")
        self.regels.append(komtvanform % (common.cgipad, komt_van))
        if komt_van == "toon_llabsent":
            self.regels.append(input_text.format('hidden', 'hId', sel_id))
            self.regels.append(input_text.format('hidden', 'txtMeld', self.fout))
            self.regels.append(input_text.format('hidden', 'hVan', kwam_van))
            self.regels.append(input_text.format('hidden', 'tla1', u))
            self.regels.append(input_text.format('hidden', 'tla2', s))
        elif komt_van == "toon_klas":
            self.regels.append(input_text.format('hidden', 'selKlas', sel_klas))
            self.regels.append(input_text.format('hidden', 'tk1', u))
            self.regels.append(input_text.format('hidden', 'tk2', s))
        elif komt_van == "toon_absent":
            self.regels.append(input_text.format('hidden', 'ta1', u))
            self.regels.append(input_text.format('hidden', 'ta2', s))
        elif komt_van == "sel_leerling":
            self.regels.append(input_text.format('hidden', 'hVan', kwam_van))
            self.regels.append(input_text.format('hidden', 'txtZoek', sel_klas))
            self.regels.append(input_text.format('hidden', 'sl1', u))
            self.regels.append(input_text.format('hidden', 'sl2', s))
        self.regels.append(htmleind)
