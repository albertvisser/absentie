#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import common
from Edex_objects import groependetailslijst, leerkrachtenlijst, Groep

row, endrow = '    <tr>', '    </tr>'
col, endcol = '      <td valign="top">', '      </td>'
coltext = '{}%s{}'.format(col, endcol)
button_disabled = '<input type="button"  disabled="disabled" value="Wijzigen" >'
button = '<input type="%s" value="%s" onclick="%s">'
header = """\
      <td><a name="wijzigdeze"></a>Naam:</td>
      <td>Leerjaar:</td>
      <td>Leerkracht:</td>
      <td>&nbsp;</td>
"""
form, endform = '    <form action="%s%s" method="post">', '    </form>'
select, endselect = '        <select name="{0}" id="{0}">', '        </select>'
selected_text = ' selected="selected"'
option = '          <option%s value="%s">%s</option>'
input_text = '        <input type="{0}" name="{1}" id="{1}" value="{2}"/>'
choose_text = '<option>-- kies --</option>'

def wijzig_groep( id_, naam, jaar, leerkracht):
    ok = False
    grp = Groep(id_)
    grp.read()
    if not grp.found:
        laatste = groependetailslijst()[1]
        grp = Groep("%05i" % int(laatste) + 1)
    wijzig = False
    if naam != grp.naam:
        grp.wijzig("naam", naam)
        wijzig = True
    if jaar != grp.jaar:
        grp.wijzig("jaar", jaar)
        wijzig = True
    if leerkracht != grp.leerkracht_id:
        grp.wijzig("leerkracht", leerkracht)
        wijzig = True
    if wijzig:
        ok = grp.write()
    else:
        ok = True
    return ok

class ToonGroep(object):
    def __init__(self, xslevel, u, s, edit_entry=False, sel_id="0"):
        self.regels = []
        self.xslevel = xslevel
        self.groepen = groependetailslijst()[0]
        self.leerkrachten = leerkrachtenlijst()[0]
        self.toon_prog = "toon_groepen.py"
        self.wijzig_prog = "wijzig_groep.py"
        with open(os.path.join(common.filepad, "groepen.html")) as fh:
            for x in fh.readlines():
                x = x.rstrip()
                if "%s" in x:
                    if "stylesheet" in x:
                        self.regels.append(x % common.httppad)
                    elif "<script" in x:
                        self.regels.extend(common.get_script())
                    elif 'action=' in x:
                        if not edit_entry:
                            self.regels.append(x % common.cgipad)
                    elif 'input type="submit"' in x:
                        self.regels.append(x % "doit_edit('tgr1','tgr2','0')")
                else:
                    if x == "<body>" and edit_entry:
                        hh = "window.location='#wijzigdeze'"
                        self.regels.append('<body onload="%s">' % hh)
                    elif "<!-- kop -->" in x:
                        self.regels.extend(common.printkop("Lijst groepen",u))
                    elif "<!-- contents -->" in x:
                        if edit_entry and sel_id == "0":
                            self.wijzigregel("0", u, s)
                        h = self.groepen.keys()
                        h.sort()
                        for y in h:
                            if edit_entry and y == sel_id:
                                self.wijzigregel(y, u, s)
                            else:
                                self.toonregel(y, edit_entry)
                    elif edit_entry and x == "</form>":
                        pass
                    else:
                        self.regels.append(x)

    def toonregel(self, x, edit_entry):
        naam, jaar, leerk = self.groepen[x]
        leerk_naam, leerk_id = leerk
        self.regels.append(row)
        self.regels.append(coltext % naam)
        self.regels.append(coltext % jaar)
        self.regels.append(coltext % leerk_naam)
        if self.xslevel > 2 or edit_entry: # wijzigen niet toegestaan
            self.regels.append(col + button_disabled)
        else:
            hh = ("doit_edit('tgr1','tgr2','%s')" % x)
            self.regels.append(col + button % ('submit', 'Wijzigen', hh))
        self.regels.append(endrow)

    def wijzigregel(self, x, un, si):
        if x == "0":
            nm = ""
            jr = ""
            lk = "0"
        else:
            nm = self.groepen[x][0]
            jr = self.groepen[x][1]
            lk = self.groepen[x][2][0]
        self.regels.append(row)
        self.regels.append(header)
        self.regels.append(endrow)
        self.regels.append(row)
        self.regels.append(form % (common.cgipad, self.wijzig_prog))
        self.regels.append(coltext % input_text.format('text', 'tnaam', nm))
        #~ self.regels.append('      <td valign="top"><input type="text" name="tjaar" id="tjaar" value="%s"/></td>' % jr)
        self.regels.append(col + select.format('selJR') + choose_text)
        for y in common.grptab:
            sl = selected_text if y == jr else ''
            if y == "H":
                z = "historisch"
            elif y == "S":
                z = "speciaal"
            else:
                z = y
            self.regels.append(option % (sl, y, z))
        self.regels.append(endselect + endcol)
        self.regels.append(col + select.format('selLK') + choose_text)
        for id_, naam in self.leerkrachten:
            sl = selected_text if id_ == lk else ''
            self.regels.append(option % (sl, naam, id_))
        self.regels.append(endselect + endcol)
        self.regels.append(col)
        self.regels.append(input_text.format('hidden', 'hId', x))
        self.regels.append(input_text.format('hidden', 'wgr1', un))
        self.regels.append(input_text.format('hidden', 'wgr2', si))
        h = "doit_woord('tnaam','Groepsnaam','wgr1','wgr2');return doit_retval;"
        self.regels.append(button % ('submit', 'OK', h) + '<br/>')
        self.regels.append(button % ('button', 'Cancel',
            'javascript:history.go(-1)'))
        self.regels.append(endcol)
        self.regels.append(endform)
        self.regels.append(endrow)
