#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import common
from Edex_objects import leerlingenlijst, Leerling, groepenlijst, Groep
from Edex_objects import Leerkracht, zoek_leerlingen, absentenlijst

row, endrow = '    <tr>', '    </tr>'
col, endcol = '      <td valign="top">', '      </td>'
coltext = '{}%s{}'.format(col, endcol)
disabled_button = '<input type="button" value="{}" disabled="disabled"/>'
button_disabled = '<input type="button"  disabled="disabled" value="Wijzigen" >'
button = '<input type="{}" value="{}" onclick="{}">'
header = """\
      <td class="hl"><a name="wijzigdeze"></a>Voornaam / voorvoegsel / achternaam:</td>
      <td class="hl">Geboortedatum:</td>
      <td class="hl">Geslacht:</td>
      <td class="hl">Groep:</td>
      <td class="hl">&nbsp;</td>
"""
form, endform = '    <form action="%s%s" method="post">', '    </form>'
select = '        <select name="{0}" id="{0}" onchange={1}>'
selected_text = ' selected="selected"'
option = '          <option%s value="%s">%s</option>'
endselect = '        </select>'
input_text = '        <input type="{0}" name="{1}" id="{1}" value="{2}"/>'
gotonext = '\n'.join(("""\
    <html><head></head><body onload="document.getElementById('%s').submit()">
    <form id="fThis" action="%stoon_llabsent.py" method="post">""",
    input_text.format('hidden', 'hId', '%s'),
    input_text.format('hidden', 'hVan', 'sel_leerling-%s'),
    input_text.format('hidden', 'tla1', '%s'),
    input_text.format('hidden', 'tla2', '%s'),
    "</form></body></html>"))
herkomst = '\n'.join((
    input_text.format('hidden', 'hVan', 'sel_leerling-%s-%s'),
    input_text.format('hidden', 'hId', '%s'),
    ))
target = '\n'.join((
    input_text.format('hidden', '{0}la1-{1}', ''),
    input_text.format('hidden', '{0}la2-{1}', ''),
    ))
wijzigform = '      <form id="wla-%s" action="%swijzig_llabsent.py" method="post">'
toonform = '      <form action="%stoon_llabsent.py" method="post">'
no_result = '    <tr><td colspan="3">Geen gegevens gevonden</td></tr>'

class SelectLeerling:
  def __init__(self, zoek, vandaan, u, s, xslevel):
    self.regels = []
    self.lijst = zoek_leerlingen(zoek, vandaan)
    if len(self.lijst) == 1:
        self.regels.append(gotonext % ('fThis', common.cgipad, self.lijst[0][0],
            zoek, u, s))
        return
    abs = absentenlijst()
    with open(os.path.join(common.filepad, "toon_klas.html")) as fh:
        for x in fh.readlines():
            x = x.rstrip()
            if "%s" in x:
                if "stylesheet" in x:
                    self.regels.append(x % common.httppad)
                elif "<script" in x:
                    self.regels.extend(common.get_script())
                elif "action" in x:
                    self.regels.append(x % common.cgipad)
                elif "option" in x:
                    for _id, naam in groepenlijst()[0]:
                        self.regels.append(x % (_id, naam))
            elif zoek != "" and '<input type="submit" value="Zoek"' in x:
                self.regels.append(disabled_button.format('Zoek'))
            elif "<!-- kop -->" in x:
                self.regels.extend(common.printkop('Gezocht op: naam(deel)', u,
                    vandaan))
            elif "txtZoek" in x and zoek != "":
                self.regels.append(x.replace( "/>", ' value="%s"/>' % zoek))
            elif "<!-- contents -->" in x:
                for key, item, text, _, _ in self.lijst:
                    self.regels.append(row)
                    self.regels.append(coltext % item)
                    self.regels.append(coltext % text)
                    if key in abs:
                        h = int(abs[key][0])
                        absdat = abs[key][2]
                        hlp = absdat[:10]
                    else:
                        h = 0
                        absdat = hlp = "&nbsp;"
                    if xslevel > 2: # wijzigen niet toegestaan
                        self.regels.append(coltext % common.afwstat[h])
                    else:
                        self.regels.append(col)
                        self.regels.append(wijzigform % (key, common.cgipad))
                        self.regels.append(herkomst % (zoek, vandaan, key))
                        self.regels.append(target.format('w', key))
                        hh = "doit_sub('wla-{0}','wla1-{0}','wla2-{0}')".format(
                            key)
                        self.regels.append(select.format('selStat', hh))
                        for ix, z in enumerate(common.afwstat):
                            hs = selected_text if ix == h else ''
                            self.regels.append(option % (hs, ix, z))
                        self.regels.append(endselect)
                        self.regels.append('  ' + endform)
                        self.regels.append(endcol)
                    self.regels.append(coltext % hlp)
                    self.regels.append(col)
                    self.regels.append(toonform % common.cgipad)
                    self.regels.append(herkomst % (zoek,vandaan, key))
                    if xslevel > 2: # wijzigen niet toegestaan
                        self.regels.append(disabled_button.format('Details'))
                    else:
                        self.regels.append(target.format('t', key))
                        hh = "doit('tla1-{0}','tla2-{0}')".format(key)
                        self.regels.append('        ' + button.format('submit',
                            'Details', hh))
                    self.regels.append('  ' + endform)
                    self.regels.append(endcol)
                    self.regels.append(endrow)
                if len(self.lijst) == 0:
                    self.regels.append(no_result)
            else:
                self.regels.append(x)

class ToonLeerling(object):
    def __init__(self, xslevel, u, s, edit_entry=False, sel_id="0"):
        self.regels = []
        self.xslevel = xslevel
        self.toon_prog = "toon_leerlingen.py"
        self.wijzig_prog = "wijzig_leerling.py"
        with open(os.path.join(common.filepad, "leerlingen.html")) as fh:
            for x in fh:
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
                        self.regels.append(x % "doit_edit('tll1','tll2','0')")
                else:
                    if x == "<body>" and edit_entry:
                        self.regels.append('<body onload="%s">' %
                            "window.location='#wijzigdeze'")
                    elif x == "<!-- kop -->":
                        self.regels.extend(common.printkop("Lijst leerlingen", u))
                    elif x == "<!-- contents -->":
                        if edit_entry and sel_id == "0":
                            self.wijzigregel("0", u, s)
                        h = leerlingenlijst()[0].keys()
                        #-- dit is het punt waarop de sortering kan worden aangepast
                        h.sort()
                        for y in h:
                            if edit_entry:
                                if y == sel_id:
                                    self.wijzigregel(y, u, s)
                                else:
                                    self.toonregel(y, True)
                            else:
                                self.toonregel(y, False)
                    elif edit_entry and x == "</form>":
                        pass
                    else:
                        self.regels.append(x)

    def toonregel(self, x, edit_entry):
        y = Leerling(x)
        z = Groep(y.groep)
        z.read()
        self.regels.append(row)
        self.regels.append(coltext % str(y.naam))
        self.regels.append(coltext % y.geboren.get_out('d-m-j'))
        self.regels.append(coltext % common.gsltab[y.geslacht])
        #~ self.regels.append('      <td valign="top">%s</td>' % auttab[y.auto])
        self.regels.append(coltext % z.leerkracht_naam)
        if self.xslevel > 2 or edit_entry: # wijzigen niet toegestaan
            hh =  disabled_button.format('Wijzigen')
        else:
            hh = "doit_edit('tll1','tll2','%s')" % x
            hh = button.format('submit', 'Wijzigen', hh)
            self.regels.append(coltext % hh)
        self.regels.append(endrow)

    def wijzigregel(self, x, un, si):
        if x == "0":
            vn = vv = an = dd = mm = jr = ""
        else:
            y = Leerling(x)
            vn, vv, an = y.naam.voornaam, y.naam.voorvoegsel, y.naam.achternaam
            dd, mm, jr = y.geboren.dag, y.geboren.maand, y.geboren.jaar
        self.regels.append(row)
        self.regels.append(header)
        self.regels.append(endrow)
        self.regels.append(row)
        self.regels.append(form % (common.cgipad, self.wijzig_prog))
        self.regels.append(col)
        self.regels.append(input_text.format('text', 'tvnaam', vn))
        self.regels.append(input_text.format('text" size="5', 'ttus', vv))
        self.regels.append(input_text.format('text', 'tanaam', an))
        self.regels.append(endcol)
        self.regels.append(col)
        self.regels.append(input_text.format('text" size="2', 'tdag', dd) + '-')
        self.regels.append(input_text.format('text" size="2', 'tmaand', mm) + '-')
        self.regels.append(input_text.format('text" size="4', 'tjaar', jr))
        self.regels.append(endcol)
        self.regels.append(col + select.format('selgesl', ''))
        for z in common.gsltab.keys():
            sl = selected_text if x != "0" and z == y.geslacht else ''
            self.regels.append(option % (sl, z, common.gsltab[z]))
        self.regels.append(endselect + endcol)
        #~ s = '      <td valign="top"><select name="selaut">'
        #~ for z in auttab.keys():
            #~ sl = ""
            #~ if x != "0":
                #~ if z == y.auto: sl = 'selected="selected" '
            #~ ss = ('<option %svalue="%s">%s</option>' % (sl,z,auttab[z]))
            #~ s = ('%s%s' % (s,ss))
        #~ self.regels.append('%s</select></td>' % s)
        self.regels.append(col + select.format('selgrp', ''))
        for naam, _id in groepenlijst():
            sl = selected_text if x != "0" and _id == y.groep else ''
            self.regels.append(option % (sl, _id, naam))
        self.regels.append(endselect + endcol)
        self.regels.append(col)
        self.regels.append(input_text.format('hidden', 'hId', x))
        self.regels.append(input_text.format('hidden', 'wll1', un))
        self.regels.append(input_text.format('hidden', 'wll2', si))
        hh = "doit_naam('tvnaam','tanaam','wll1','wll2');return doit_retval"
        self.regels.append('        ' + button.format("submit", "OK", hh))
        self.regels.append('        ' + button.format("button", "Cancel",
            "javascript:history.go(-1)"))
        self.regels.append(endcol)
        self.regels.append(endform)
        self.regels.append(endrow)

def wijzig_leerling(id_, (vn, vv, an), (dd, mm, jr), gesl, aut, grp):
    ok = wijzigen = False
    ll = Leerling(id_)
    ll.read()
    if not ll.found:
        id_ = ("%05i" % (int(leerlingenlijst()[1]) + 1))
        ll = Leerling(id_)
    wijzigen = False
    if vn != ll.naam.vn:
        ll.setAttr("vn",vn)
        wijzigen = True
    if vv != ll.naam.vv:
        ll.setAttr("vv",vv)
        wijzigen = True
    if an != ll.naam.an:
        ll.setAttr("an",an)
        wijzigen = True
    datum = dd + mm + jr
    datum2 = ll.geboren.get_out("dmj")
    if datum != datum2:
        ll.setAttr("geb",datum)
        wijzigen = True
    if gesl != ll.gesl:
        ll.setAttr("gesl",gesl)
        wijzigen = True
    #~ if aut != ll.auto:
        #~ ll.setAttr("auto",aut)
        #~ wijzigen = True
    if grp != ll.groep:
        ll.setAttr("groep",grp)
        wijzigen = True
    if wijzigen:
        ok = ll.write()
    else:
        ok = True
    return ok
