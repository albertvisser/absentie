from globals import filepad

class naamobj:
    def __init__(self,x):
        if x == "":
            self.an = ""
            self.vv = ""
            self.vn = ""
        else:
            self.an = x[0:40].strip()
            self.vv = x[40:50].strip()
            self.vn = x[50:70].strip()
        self.maaknaam()

    def wijzig(self,x,y):
        if x == "vn":
            self.vn = y
        elif x == "vv":
            self.vv = y
        elif x == "an":
            self.an = y
        self.maaknaam()

    def maaknaam(self):
        self.naam = self.getout("vta")

    def getout(self,x):
        if x == "atv":
            s = ("%-40s%-10s%-20s" % (self.an,self.vv,self.vn))
        elif x == "vta":
            t = ""
            if self.vv != "": t = " "
            s = ("%s %s%s%s" % (self.vn,self.vv,t,self.an))
        return s

class datumobj:
    def __init__(self):
        self.dd =""
        self.mm =""
        self.jr =""

    def setAttr(self,x,y):
        if x == "dag":
            self.dd = y
        elif x == "maand":
            self.mm = y
        elif x == "jaar":
            self.jr = y

    def getIn(self,x,y):
        if x == "dmj":
            self.setAttr("dag",y[:2])
            self.setAttr("maand",y[2:4],)
            self.setAttr("jaar",y[4:])
        elif x == "jmd":
            self.setAttr("dag",y[6:])
            self.setAttr("maand",y[4:6],)
            self.setAttr("jaar",y[:4])

    def getOut(self,x):
        if x == "dmj":
            y = self.dd + self.mm + self.jr
        elif x == "d-m-j":
            y = self.dd + "-" + self.mm + "-" + self.jr
        elif x == "jmd":
            y = self.jr + self.mm + self.dd
        return y

class lijstLK:
    "Opbouwen lijst met leerkrachten (alleen voornaam) en hun id's"
    # lk = lijstLK[i]
    # lk[0] is naam, lk[1] is id
    def __init__(self):
        self.laatste = ""
        self.ververs()

    def ververs(self):
        self.lk = []
        fh = open(filepad + "EdexLKw.txt","r")
        for x in fh.readlines():
            if x[:-1] != '':
                lknm = x[50:70].strip()
                lkid = x[70:75]
                if lkid > self.laatste:
                    self.laatste = lkid
                self.lk.append([lknm,lkid])
        fh.close()

class LKgeg:
    "Gegevens m.b.t. een leraar: op basis van id bepalen naam en groep(en)"
    # lk = LKgeg(i)
    # lk.id is id, lk.naam.naam is naam, lk.naam.vn is voornaam, lk.naam.vv is voorvoegsel, lk.naam.an is achternaam
    # lk.groep[i] is groepsid, lk.grpnm[i] is groepsnaam
    def __init__(self,lkid):
        self.id = lkid
        self.found = 0
        self.naam = naamobj("")
        self.read()

    def read(self):
        fh = open(filepad + "EdexLKw.txt","r")
        for x in fh.readlines():
            if x[70:75] == self.id:
                self.found = 1
                break
        fh.close()
        if self.found:
            self.naam = naamobj(x[0:70])
            self.groep = []
            fh = open(filepad + "EdexLGw.txt","r")
            for x in fh.readlines():
                if x[0:5] == self.id:
                    self.groep.append(x[5:10])
            fh.close()
            fh = open(filepad + "EdexGRw.txt","r")
            self.grpnm = []
            for x in range(len(self.groep)):
                self.grpnm.append("")
            for x in fh.readlines():
                z = x[31:36]
                try:
                    h = self.groep.index(z)
                    if h > -1:
                        self.grpnm[h] = x[0:30].strip()
                except:
                    pass
            fh.close()

    def setAttr(self,naam,waarde):
        if naam == "vn":
            self.naam.vn = waarde
        elif naam == "vv":
            self.naam.vv = waarde
        elif naam == "an":
            self.naam.an = waarde

    def write(self):
        fn = filepad + "EdexLKw.txt"
        fno = fn + ".bak"
        from shutil import copyfile
        copyfile(fn,fno)
        s = ("%-40s%-10s%-20s%s    1\n" % (self.naam.an,self.naam.vv,self.naam.vn,self.id))
        if self.found:
            fh = open(fn,"w")
            fho = open(fno,"r")
            for x in fho.readlines():
                if x[70:75] == self.id:
                    fh.write(s)
                else:
                    fh.write(x)
            fho.close()
            fh.close()
        else:
            fh = open(fn,"a")
            fh.write(s)
            fh.close()
        return True

class lijstGR0:
    "lijst met alleen id en naam"
    def __init__(self):
        self.ververs()

    def ververs(self):
        self.lg = []
        fh = open(filepad + "EdexGRw.txt","r")
        for x in fh.readlines():
            grnm = x[:30].strip()
            grid = x[31:36]
            self.lg.append([grnm,grid])
        fh.close()

class lijstGR:
    def __init__(self):
        self.laatste = ""
        self.ververs()

    def ververs(self):
        lh = lijstLK()
        y = {}                          # lijst opbouwen met groepskey en leerkracht naam ipv lkid
        fh = open(filepad + "EdexLGw.txt","r")
        for x in fh.readlines():
            for z in lh.lk:
                if x[:5] == z[1]:       # leerkrachtid vergelijken met id's uit lijstLK
                    y[x[5:10]] = [z[1],z[0]]   # indien gelijk, naam overnemen
                    break
        fh.close()
        self.groep = {}                 # groepsgegevens opbouwen
        fh = open(filepad + "EdexGRw.txt","r")
        for x in fh.readlines():
            if x[:-1] != '':
                id = x[31:36]
                if id > self.laatste:
                    self.laatste = id
                g = GRgeg(id)    # groepsid
                g.setAttr("naam",x[:30].strip())    # groepsnaam
                g.setAttr("jaar",x[30])             # leerjaar
                g.setAttr("leerkracht",y[x[31:36]])       # leerkrachtid
                self.groep[x[31:36]] = g    # groepsid
        fh.close()

class GRgeg:
    "gegevens van groep"
    def __init__(self,grid):
        self.grid = grid
        self.naam = ""
        self.jaar = ""
        self.lkid = ""
        self.lknm = ""

    def read(self):
        self.found = False
        l = lijstGR()
        if l.groep.has_key(self.grid):
            self.found = True
            self.setAttr("naam",l.groep[self.grid].naam)
            self.setAttr("jaar",l.groep[self.grid].jaar)             # leerjaar
            self.setAttr("leerkracht",[l.groep[self.grid].lkid,l.groep[self.grid].lknm])       # leerkrachtid

    def write(self):
        #~ GRw: groepsaanduidingen
        #~ 0-29 naam 30 leerjaar 31-35 groep-id 36-44 jaren
        #~ groepsnaam   max. 30 karakters    positie 1 t/m 30
        #~ jaargroep   1 karakter    positie 31:    1 t/m 8 voor jaargroepen 1 t/m 8    S voor speciaal onderwijs    H voor historische groepen
        #~ groepkey   alfanum, max. 5 karakters    positie 32 t/m 36
        #~ LGw: koppeling groep - leerkracht
        fn = filepad + "EdexGRw.txt"
        fno = fn + ".bak"
        from shutil import copyfile
        copyfile(fn,fno)
        fh = file(fn,"w")
        fho = file(fno,"r")
        gevonden = False
        for x in fho.readlines():
            k = x[31:36]    # groepsid
            if k == self.grid:
                gevonden = True
                y = self.naam.ljust(30) + str(self.jaar ) + k + x[36:]
                #~ if x[:36] == y and x != y:
                    #~ y = x
            else:
                y = x
            fh.write(y)
        if not gevonden:
            x = self.naam.ljust(30) + str(self.jaar ) +self.grid
            fh.write("\n" + x)
        fh.close()
        fho.close()
        fn = filepad + "EdexLGw.txt"
        fno = fn + ".bak"
        fh = file(fn,"r")
        l = fh.readlines()
        fh.close()
        gewijzigd = True
        for x in l:
            if x[5:10] == self.grid:
                # hier gaat het juist om de leerkrachtkey!
                if x[:5] == self.lkid:
                    gewijzigd = False
                else:
                    l[l.index(x)] = self.lkid + l[l.index(x)][5:]
                break
        if gewijzigd:
            copyfile(fn,fno)
            fh = file(fn,"w")
            for x in l:
                fh.write(x)
            if not gevonden:
                fh.write("\n%s%s" % (self.lkid,self.grid))
            fh.close()
        ok = True
        return ok

    def setAttr(self,naam,waarde):
        ok = True
        if naam == "naam":
            self.naam = waarde
        if naam == "jaar":
            self.jaar = waarde
        elif naam == "leerkracht":
            if type(waarde) is str:
                self.lkid = waarde
            else:
                self.lkid = waarde[0]
                self.lknm = waarde[1]
        else:
            ok = False
        return ok

class lijstLL:
    "alle leerlingen, indien zinvol ook selecties toevoegen"
    def __init__(self):
        self.laatste = ""
        self.ververs()

    def ververs(self):
        self.ll = {}
        fh = open(filepad + "EdexLLw.txt","r")
        for x in fh.readlines():
            llgr = x[85:90]
            llnm = naamobj(x[0:70])
            llid = x[80:85]
            if llid > self.laatste:
                self.laatste = llid
            self.ll[llid] = (llnm,llgr)
        fh.close()

class lijstLLbijLK:
    def __init__(self,lkid):
        self.ververs(lkid)

    def ververs(self,lkid):
        self.lk = LKgeg(lkid)
        self.ll = []
        fh = open(filepad + "EdexLLw.txt","r")
        for x in fh.readlines():
            z = x[85:90]
            try:
                h = self.lk.groep.index(z)
                if h > -1:
                    llnm = naamobj(x[0:70])
                    llid = x[80:85]
                    self.ll.append([llid,llnm])
            except:
                pass
        fh.close()

class lijstAbsent:
    def __init__(self):
        self.ververs()

    def ververs(self):
        self.ll = {}
        found = 1
        try:
            fh = open(filepad + "EdexLAw.txt","r")
        except:
            found = 0
        if found:
            for x in fh.readlines():
                llid = x[0:5]
                if self.ll.has_key(llid):
                    continue
                else:
                    #~ llab = x[5]
                    #~ llrd = x[6:].strip()
                    #~ self.ll[llid] = (llab,llrd)
                    lldt = x[5:24] #-- nieuwe versie: met datum/tijd (?)
                    llab = x[24]
                    llrd = x[25:].strip()
                    self.ll[llid] = (llab,llrd,lldt)
            fh.close()

class AbsentHist:
    def __init__(self,llid):
        self.ververs(llid)

    def ververs(self,llid):
        self.lijst = []
        found = 1
        try:
            fh = open(filepad + "EdexLAw.txt","r")
        except:
            found = 0
        if found:
            for x in fh.readlines():
                ll = x[0:5]
                if ll == llid:
                    dt = x[5:24]
                    code = x[24:25]
                    reden = x[25:].strip()
                    self.lijst.append([dt,code,reden])
            fh.close()
class zoekLL:
    def __init__(self,zoek,van):
        self.zoek = zoek
        h = van.split("-")
        if len(h) == 1:
            self.van = van
            self.ingrp = []
        elif len(h) == 2:               # komt van scherm met leerkrachtnummer
            self.van = h[0]
            self.bij = h[1]
            if self.van == "toon_klas":
                lh = LKgeg(self.bij)
                self.ingrp = lh.groep
        gh = lijstGR()
        self.lijst = []
        fh = open(filepad + "EdexLLw.txt","r")
        for x in fh.readlines():
            s = x[0:70].upper()
            z = self.zoek.upper()
            if s.find(z) > -1:
                h = naamobj(x[0:70])
                llnm = h.naam
                llid = x[80:85]
                insel = 1
                llgr = gh.groep[x[85:90]].lknm # of .lkid
                if len(self.ingrp) > 0:
                    llgrp = x[85:90]
                    try:
                        h = self.ingrp.index(llgrp)
                    except:
                        insel = 0
                if insel:
                    self.lijst.append([llid,llnm,llgr])
        fh.close()

class LLgeg:
    def __init__(self,llid):
        self.llid = llid
        self.code = 0
        self.reden = ""
        self.found = 0
        self.naam = naamobj("")
        self.geboren = datumobj()
        self.read()

    def read(self):
        fh = open(filepad + "EdexLLw.txt","r")
        for x in fh.readlines():
            if x[80:85] == self.llid:
                self.found = 1
                break
        fh.close()
        if self.found:
            self.naam = naamobj(x[0:70])
            self.geboren.getIn("dmj",x[70:78])
            self.gesl = x[78]
            self.auto = x[79]
            self.groep = x[85:90]
            dh = lijstAbsent()
            if dh.ll.has_key(self.llid):
                s = dh.ll[self.llid]
                self.code = s[0]
                self.reden = s[1].strip()

    def lastAbsentie(self):
        fn = filepad + "EdexLAw.txt"
        try:
            fh = open(fn,"r")
        except:
            return
        lines = fh.readlines()
        for i in lines:
            if i[0:5] == self.llid:
                regel = i
        fh.close()


    def wijzigcode(self,code):
        self.code = code

    def wijzigreden(self,reden):
        self.reden = reden

    def update(self,code,reden,datetime):
        "absentie updaten"
        fn = filepad + "EdexLAw.txt"
        fno = filepad + "EdexLAw.bak"
        try:
            fh = open(fn,"r")
        except:
            foundf = False
        else:
            foundf = True
        newline = ("%s%s%s%s") % (self.llid,datetime,code,reden)
        if newline[:-1] != "\n":
            newline = newline + "\n"
        lines = []
        i = 0
        regel = ""
        if foundf:
            from shutil import copyfile
            fh.close()
            copyfile(fn,fno)
            fh = open(fno,"r")
            lines = fh.readlines()
            fh.close()
            foundl = False
            for i in range(len(lines)):
                if lines[i][0:5] == self.llid:
                    foundl = True
                    break
            print foundl,lines[i][:-1],newline[:-1]
            if foundl:
                if lines[i][24:] == newline[24:]:
                    del lines[i]
        lines.insert(i,newline)
        fh = open(fn,"w")
        for x in lines:
            fh.write(x)
        fh.close()


    def setAttr(self,naam,waarde,dmj="dmj"):
        if naam in ["vn","vv","an"]:
            self.naam.wijzig(naam,waarde)
        elif naam == "geb":
            self.geboren.getIn(dmj,waarde)
        elif naam == "gesl":
            self.gesl = waarde
        elif naam == "auto":
            self.auto = waarde
        elif naam == "groep":
            self.groep = waarde

    def write(self):
        fn = filepad + "EdexLLw.txt"
        fno = fn + ".bak"
        from shutil import copyfile
        copyfile(fn,fno)
        s = ("%s%s%s%s%s%s" % (self.naam.getout("atv"),self.geboren.getOut("dmj"),self.gesl,self.auto,self.llid,self.groep))
        if self.found:
            fh = open(fn,"w")
            fho = open(fno,"r")
            for x in fho.readlines():
                if x[80:85] == self.llid:
                    fh.write("%s\n" % s)
                else:
                    fh.write(x)
            fho.close()
            fh.close()
        else:
            fh = open(fn,"a")
            fh.write("\n%s" % s)
            fh.close()
        return True

def test_naamobj():
    n = naamobj("")
    print "init leeg naamobj:",n.vn,n.vv,n.an,"(",n.naam,")"
    n.wijzig("vn","Willem")
    print "na instellen voornaam:",n.vn,n.vv,n.an,"(",n.naam,")"
    n.wijzig("vv","van")
    print "na instellen tussenvoegsel:",n.vn,n.vv,n.an,"(",n.naam,")"
    n.wijzig("an","Snorkesteijn")
    print "na instellen achternaam:",n.vn,n.vv,n.an,"(",n.naam,")"
    n.wijzig("vn","")
    print "na weghalen voornaam:",n.vn,n.vv,n.an,"(",n.naam,")"
    n.wijzig("vv","")
    print "na weghalen tussenvoegsel:",n.vn,n.vv,n.an,"(",n.naam,")"
    n.wijzig("an","")
    print "na weghalen achternaam:",n.vn,n.vv,n.an,"(",n.naam,")"

def test_datumobj():
    n = datumobj()
    print "init leeg datumobj",n.dd,n.mm,n.jr
    n.getIn("dmj","31122001")
    print "na input als dmj: 31122001",n.dd,n.mm,n.jr
    n.getIn("jmd","19960709")
    print "na input als jmd: 19960709",n.dd,n.mm,n.jr
    n.setAttr("dag","12")
    print "na wijzigen dag in 12:",n.dd,n.mm,n.jr
    n.setAttr("maand","02")
    print "na wijzigen maand in 07:",n.dd,n.mm,n.jr
    n.setAttr("jaar","1999")
    print "na wijzigen jaar in 1999:",n.dd,n.mm,n.jr
    print "datum",n.getOut("dmj")
    print "datum",n.getOut("d-m-j")
    print "datum",n.getOut("jmd")

def test_lijstLK():
    f = file("Edex_objects.txt","r")
    hh = lijstLK()
    for x in hh.lk:
        print x
    f.close()

def test_LKgeg():
    #~ lk = x[1]
    #~ lh = LKgeg(lk)
    #~ print("%s\n" % lh.naam)
    #~ s = ""
    #~ for x in lh.groep:
        #~ s = ("%s%s," % (s,x))
    #~ print s
    #~ s = ""
    #~ for x in lh.grpnm:
        #~ s = ("%s%s," % (s,x))
    #~ print s
    lk = LKgeg('0')
    lk.read()
    if not lk.found:
        h = lijstLK()
        id = ("%05i" % (int(h.laatste) + 1))            # bepaal laatste leerkrachtid
        lk = LKgeg(id)
    print lk.naam.vn,lk.naam.vv,lk.naam.an
    w = False
    vn = "Wwiilleemm"
    vv = "Vvaann"
    an = "Oorraannjjee"
    if vn != lk.naam.vn:
        lk.setAttr("vn",vn)
        w = True
    if vv != lk.naam.vv:
        lk.setAttr("vv",vv)
        w = True
    if an != lk.naam.an:
        lk.setAttr("an",an)
        w = True
    if w:
        ok = lk.write()
    else:
        ok = True
    print w,ok,lk.naam.vn,lk.naam.vv,lk.naam.an

def test_LLbijLK():
    f = file("Edex_objects.txt","w")
    lh = lijstLLbijLK(lk)
    for x in lh.lk.naam:
        f.write("%s\n"% x)
    for x in lh.lk.groep:
        f.write("%s\n"% x)
    for x in lh.ll:
        f.write("%s\n"% x)
    f.close()

def test_lijstAbsent():
    lh = lijstAbsent()
    if len(lh.ll) == 0:
        print "Geen absenten"
    else:
        f = file("Edex_objects.txt","w")
        for x in lh.ll.keys():
            f.write("%s %s\n"% (x, lh.ll[x]))
        f.close()

def test_lijstLL():
    f = file("Edex_objects.txt","w")
    hh = lijstLL()
    for x in hh.ll:
        print x,hh.ll[x]

def test_LLgeg():
    ll = LLgeg("00052")
    if ll.found:
        print ll.naam.vn,ll.naam.vv,ll.naam.an,"(",ll.naam.naam,")"
        print ll.geboren.getOut("d-m-j"),ll.gesl,ll.auto,ll.groep
        print ll.code,ll.reden
        ll.setAttr("vn","Willem")
        ll.setAttr("vv","van")
        ll.setAttr("an","Snurkesteijn")
        ll.setAttr("geb","01010101")
        ll.setAttr("gesl","X")
        ll.setAttr("auto","5")
        ll.setAttr("groep","00037")
        print ll.naam.vn,ll.naam.vv,ll.naam.an,"(",ll.naam.naam,")"
        print ll.geboren.getOut("d-m-j"),ll.gesl,ll.auto,ll.groep
        print ll.code,ll.reden
        ll.write()
        ll.read()
        print ll.naam.vn,ll.naam.vv,ll.naam.an,"(",ll.naam.naam,")"
        print ll.geboren.getOut("d-m-j"),ll.gesl,ll.auto,ll.groep
        print ll.code,ll.reden
    else:
        print "leerling niet gevonden"
    #~ lh.wijzigcode("3")
    #~ lh.wijzigreden("")
    #~ lh.update()

def test_zoekLL():
    f = file("Edex_objects.txt","w")
    zh = zoekLL("jansen","start")
    for x in zh.lijst:
      f.write("%s\n"% x)
    f.close()

def test_lijstGr0():
    lh = lijstGR0()
    print lh.__dict__
    f = file("Edex_objects.txt","w")
    for x in lh.lg:
        f.write("%s\n"% x)
    f.close()

def test_lijstGR():
    lh = lijstGR()
    f = file("Edex_objects.txt","w")
    for x in lh.groep.keys():
        f.write("%s %s %s %s %s\n"% (x, lh.groep[x].naam, lh.groep[x].jaar, lh.groep[x].lkid, lh.groep[x].lknm))
    f.close()

def test_GRgeg():
    #~ # probleempje... een groep kan kennelijk bij twee leerkrachten horen (in dit geval ook annelies)
    gr = GRgeg("00048")
    gr.read()
    if gr.found:
        print "naam:",gr.naam
        print "jaar:",gr.jaar
        print "leerkracht:",gr.lkid,gr.lknm
    return
    gr.setAttr("naam","andere naam")
    gr.write()
    gr.read()
    if gr.found:
        print "naam:",gr.naam
        print "jaar:",gr.jaar
        print "leerkracht:",gr.lkid,gr.lknm

def test_AbsentHist():
    zh = AbsentHist("00089")
    f = file("Edex_objects.txt","w")
    for x in zh.lijst:
        f.write("%s\n"% x)
    f.close()

def test(h):
    if h == "naamobj":
        test_naamobj()
    elif h == "datumobj":
        test_datumobj()
    elif h == "lijstLK":
        test_lijstLK()
    elif h == "LKgeg":
        test_LKgeg()
    elif h == "LLbijLK":
        test_LLbijLK()
    elif h == "lijstabsent":
        test_lijstabsent()
    elif h == "LLgeg":
        ll = LLgeg("00052")
        ll.update("3","teruggezet","01-03-2001;01:01:01")
    elif h == "zoekLL":
        test_zoekLL()
    elif h == "lijstGR0":
        test_lijstGR0()
    elif h == "lijstGR":
        test_lijstGR()
    elif h == "GRgeg":
        test_GRgeg()
    elif h == "absenthist":
        test_absenthist()

if __name__ == '__main__':
    h = "LLgeg"
    test(h)
