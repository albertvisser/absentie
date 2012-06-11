#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from globals import filepad
_leerkrachtenfile = os.path.join(filepad, "EdexLKw.txt")
_leerkrachtgroepenfile = os.path.join(filepad, "EdexLGw.txt")
_groepenfile = os.path.join(filepad, "EdexGRw.txt")
_leerlingenfile = os.path.join(filepad, "EdexLLw.txt")
_absentenfile = os.path.join(filepad, "EdexLAw.txt")

class Naamobj(object):
    """basisobject voor deze verzameling

    bevat attributen en een aantal standaard methoden
    """
    def __init__(self, naam=""):
        self.achternaam = self.voorvoegsel = self.voornaam = ""
        if naam:
            self.get_naamgeg(naam)

    def get_naamgeg(self, data):
        self.achternaam = data[0:40].strip()
        self.voorvoegsel = data[40:50].strip()
        self.voornaam = data[50:70].strip()

    def wijzig(self, naamdeel, data):
        if naamdeel == "vn":
            self.voornaam = data
        elif naamdeel == "vv":
            self.voorvoegsel = data
        elif naamdeel == "an":
            self.achternaam = data

    def __repr__(self):
        return self.displaynaam("vta")

    def displaynaam(self, format):
        if format == "atv":
            uit = "%-40s%-10s%-20s" % (self.achternaam, self.voorvoegsel,
                self.voornaam)
        elif format == "vta":
            hlp = " " if self.voorvoegsel != "" else ""
            uit = "%s %s%s%s" % (self.voornaam, self.voorvoegsel, hlp,
                self.achternaam)
        return uit

class Datumobj(object):
    """basisobject voor deze verzameling

    bevat attributen en een aantal standaard methoden
    """
    def __init__(self, format=None, data=None):
        self.dag = self.maand = self.jaar = ""
        if format and data:
            self.get_in(format, data)

    ## def setAttr(self,x,y):
        ## if x == "dag":
            ## self.dag = y
        ## elif x == "maand":
            ## self.maand = y
        ## elif x == "jaar":
            ## self.jaar = y

    def __repr__(self):
        return self.get_out('d-m-j')

    def get_in(self, format, data):
        if format == "dmj":
            self.dag = data[:2]
            self.maand = data[2:4]
            self.jaar = data[4:]
        elif format == "jmd":
            self.dag = data[6:]
            self.maand = data[4:6]
            self.jaar = data[:4]

    def get_out(self, format):
        if format == "dmj":
            uit = self.dag + self.maand + self.jaar
        elif format == "d-m-j":
            uit = self.dag + "-" + self.maand + "-" + self.jaar
        elif format == "jmd":
            uit = self.jaar + self.maand + self.dag
        return uit

def leerkrachtenlijst():
    "Opbouwen lijst met leerkrachten (alleen voornaam) en hun id's"
    laatste = ""
    lijst = []
    with open(_leerkrachtenfile) as fh:
        for x in fh:
            x = x.strip()
            if x == '':
                continue
            naam = x[50:70].strip()
            _id = x[70:75]
            if _id > laatste:
                laatste = _id
            lijst.append((naam, _id))
    return lijst, laatste

class Leerkracht(object):
    "Gegevens m.b.t. een leraar: op basis van id bepalen naam en groep(en)"
    def __init__(self, _id):
        self.id = _id
        self._fn = _leerkrachtenfile
        self.found = False
        self.naam = Naamobj()
        self.read()

    def read(self):
        with open(self._fn) as fh:
            for x in fh:
                if x[70:75] == self.id:
                    self.found = True
                    break
        if self.found:
            self.naam = Naamobj(x[0:70])
            self.groep = {}
            with open(_leerkrachtgroepenfile) as fh:
                for x in fh:
                    if x[0:5] == self.id:
                        self.groep[x[5:10]] = ""
            with open(_groepenfile) as fh:
                for x in fh:
                    grpid = x[31:36]
                    if grpid in self.groep:
                        self.groep[grpid] = x[0:30].strip()

    def wijzig(self, naamdeel, waarde):
        self.naam.wijzig(naamdeel, waarde)

    def write(self):
        fno = self._fn + ".bak"
        shutil.copyfile(self._fn, fno)
        s = ("%-40s%-10s%-20s%s    1\n" % (self.naam.achternaam,
            self.naam.voorvoegsel, self.naam.voornaam, self.id))
        if self.found:
            with open(self._fn,"w") as fh, open(fno) as fho:
                for x in fho:
                    if x[70:75] == self.id:
                        fh.write(s)
                    else:
                        fh.write(x)
        else:
            with open(self._fn, "a") as fh:
                fh.write(s)
        return True

def groepenlijst(): # was lijstGR0
    "lijst met alleen id en naam"
    lijst = []
    with open(_groepenfile) as fh:
        lijst = [(x[:30].strip(), x[31:36]) for x in fh]
    return lijst

def groependetailslijst(): # was lijstGR
    laatste = ""
    y = {}
    with open(_leerkrachtgroepenfile) as fh:
        for x in fh:
            leerk_id = x[:5]
            grp_id = x[5:10]
            for naam, _id in leerkrachtenlijst()[0]:
                if _id == leerk_id:
                    y[grp_id] = (naam, _id)
                    break
    lijst = {}                 # groepsgegevens opbouwen
    with open(_groepenfile) as fh:
        for x in fh:
            if x.rstrip() == '':
                continue
            grp_id = x[31:36]
            if grp_id > laatste:
                laatste = grp_id
            naam = x[:30].strip()
            jaar = x[30]
            leerkracht = y[grp_id]
            lijst[grp_id] = (naam, jaar, leerkracht)
    return lijst, laatste

class Groep(object):
    "gegevens van groep"
    def __init__(self, grp_id):
        self._id = grp_id
        self.data, self.laatste = groependetailslijst()
        self.naam = self.jaar = self.leerkracht_id = self.leerkracht_naam = ""
        self.found = False

    def read(self):
        if self._id in self.data.keys():
            self.found = True
            self.naam, self.jaar, leerk = self.data[self._id]
            self.leerkracht_naam, self.leerkracht_id = leerk

    def write(self):
        ok = False
        fn = _groepenfile
        fno = fn + ".bak"
        shutil.copyfile(fn, fno)
        with open(fn, "w") as fh, open(fno) as fho:
            gevonden = False
            for x in fho:
                key = x[31:36]    # groepsid
                if key == self.id:
                    gevonden = True
                    y = self.naam.ljust(30) + str(self.jaar) + key + x[36:]
                else:
                    y = x
                fh.write(y)
            if not gevonden:
                x = self.naam.ljust(30) + str(self.jaar) + self.id
                fh.write("\n" + x)
        fn = _leerkrachtgroepenfile
        with open(fn) as fh:
            data = fn.readlines()
        gewijzigd = False
        for ix, x in enumerate(data):
            gr_id, leerk_id = x[5:10], x[:5]
            if gr_id == self.id and leerk_id != self.leerkracht_id:
                self.gewijzigd = True
                data[ix][:5] = self.leerkracht_id
                break
        if gewijzigd:
            fno = fn + ".bak"
            shutil.copyfile(fn, fno)
            with open(fn, "w") as fh:
                fh.writelines(data)
        ok = True
        return ok

    def wijzig(self, naam, waarde):
        ok = False
        if naam == "naam":
            self.naam = waarde
        if naam == "jaar":
            self.jaar = waarde
        elif naam == "leerkracht":
            if isinstance(waarde, str):
                self.leerkracht_id = waarde
                self.leerkracht_naam = Leerkracht(waarde).naam.voornaam
            else:
                self.leerkracht_id, self.leerkracht_naam = waarde
        else:
            return
        ok = True
        return ok

def leerlingenlijst(leerkracht=None, groep=None):
    "alle leerlingen, indien zinvol ook selecties toevoegen"
    lijst, laatste, leerk = {}, '', None
    groepen = ()
    if leerkracht is not None:
        leerk = Leerkracht(leerkracht)
        groepen = leerk.groep.keys()
    elif groep is not None:
        groepen = (groep,)
    with open(_leerlingenfile) as fh:
        for x in fh:
            grp_id = x[85:90]
            naam = Naamobj(x[0:70])
            _id = x[80:85]
            if _id > laatste:
                laatste = _id
            if not groepen or grp_id in groepen:
                lijst[_id] = (naam, grp_id)
    return lijst, laatste, leerk

def absentenlijst():
    lijst = {}
    if not os.path.exists(_absentenfile):
        return lijst
    with open(_absentenfile) as fh:
        for x in fh:
            leerl_id = x[0:5]
            if leerl_id in lijst:
                continue # eerdere absenties overslaan
            else:
                datum = x[5:24]
                reden = x[24]
                oms = x[25:].strip()
                lijst[leerl_id] = (reden, oms, datum)
    return lijst

def absenties(leerl_id):
    lijst = []
    if not os.path.exists(_absentenfile):
        return lijst
    with open(_absentenfile) as fh:
        for x in fh:
            leerl = x[0:5]
            if leerl == leerl_id:
                datum = x[5:24]
                reden = x[24:25]
                oms = x[25:].strip()
                lijst.append((datum, reden, oms))
    return lijst

def zoek_leerlingen(zoek, van):
    h = van.split("-")
    if len(h) == 1:
        ingrp = []
    elif len(h) == 2:               # komt van scherm met leerkrachtnummer
        van, bij = h
        if van == "toon_klas":
            lh = Leerkracht(bij)
            ingrp = lh.groep
    groepen, _ = groependetailslijst()
    lijst = []
    with open(_leerlingenfile) as fh:
        for x in fh:
            naam = x[0:70]
            if zoek.upper() in naam.upper():
                leerl_naam = str(Naamobj(x[0:70]))
                leerl_id = x[80:85]
                leerl_grp = x[85:90]
                ## insel = 1
                ## llgr = gh.groep[x[85:90]].lknm # of .lkid
                if not ingrp or leerl_grp in ingrp:
                    grp_naam, grp_jaar, leerk = groepen[leerl_grp]
                    lijst.append((leerl_id, leerl_naam, leerl_grp, grp_naam,
                        grp_jaar))
    return lijst

class Leerling:
    def __init__(self, leerl_id):
        self._id = leerl_id
        self.code = 0
        self.reden = self.absdat = ""
        self.found = False
        self.naam = Naamobj()
        self.geboren = Datumobj()
        self.read()

    def read(self):
        with open(_leerlingenfile) as fh:
            for x in fh:
                if x[80:85] == self._id:
                    self.found = True
                    break
        if self.found:
            self.naam = Naamobj(x[0:70])
            self.geboren = Datumobj("dmj", x[70:78])
            self.geslacht = x[78]
            self.herkomst = x[79]
            self.groep = x[85:90]
            ## test = self.laatste_absentie()
            ## if test:
                ## self.absdat, self.code, self.reden = test

    def get_absenties(self):
        self.absenties = absenties(self._id)

    def laatste_absentie(self):
        self.get_absenties()
        if self.absenties:
            return self.absenties[0]

    def add_absentie(self, code, reden, datetime):
        "absentie updaten"
        fn = _absentenfile
        fno = fn + '.bak'
        newline = self._id + datetime + code + reden
        if newline[:-1] != "\n":
            newline = newline + "\n"
        lines = []
        i = 0
        regel = ""
        replace = False
        if os.path.exists(fn):
            shutil.copyfile(fn,fno)
            with open(fno) as fh:
                lines = fh.readlines()
                fh.close()
            for ix, line in enumerate(lines):
                if line[24:] == newline[24:]:
                    replace = True
                    lines[ix] = newline
        if not replace:
            lines.insert(0,newline)
        with open(fn, "w") as fh:
            fh.writelines(lines)

    def wijzig(self, naam, waarde, dmj="dmj"):
        if naam in ["vn","vv","an"]:
            self.naam.wijzig(naam,waarde)
        elif naam == "geb":
            self.geboren.get_in(dmj, waarde)

    def write(self):
        fn = _leerlingenfile
        fno = fn + ".bak"
        shutil.copyfile(fn, fno)
        s = (self.naam.get_out("atv") + self.geboren.get_out("dmj") +
            self.geslacht + self.herkomst + self.leerl_id + self.groep)
        if self.found:
            with open(fn, "w") as fh, open(fno) as fho:
                for x in fho:
                    if x[80:85] == self.leerl_id:
                        fh.write("%s\n" % s)
                    else:
                        fh.write(x)
        else:
            with open(fn,"a") as fh:
                fh.write("\n%s" % s)
        return True
