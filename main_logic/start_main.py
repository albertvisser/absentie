from school_globals import *
print sys.path
from Edex_objects import lijstLK

class login_main:
  def __init__(self):
    #~ lk = lijstLK()
    self.regels = []
    fh = open(filepad + "login.html")
    for x in fh.readlines():
        h = x.find("%s")
        if h > -1:
            hs = x[:-1].split("%s")
            if x.find("stylesheet") > -1:
                self.regels.append("%s%s%s" % (hs[0],httppad,hs[1]))
            elif x.find("<script") > -1:
                self.regels.append(hs[0])
                f2 = file(filepad + 'check.js')
                for x in f2.readlines():
                    self.regels.append(x[:-1])
                f2.close()
                self.regels.append(hs[1])
            elif x.find(".py") > -1:
                self.regels.append("%s%s%s" % (hs[0],cgipad,hs[1]))
        else:
            if x[:-1] == "<!-- kop -->":
                for y in printkop("Login"):                  # gedefinieerd in school_globals
                    self.regels.append(y)
            else:
                self.regels.append(x[:-1])
    fh.close()

class start_main:
  def __init__(self,u,xslevel):
    lk = lijstLK()
    self.regels = []
    fh = open(filepad + "start.html")
    for x in fh.readlines():
        h = x.find("%s")
        if h > -1:
            hs = x[:-1].split("%s")
            if x.find("stylesheet") > -1:
                self.regels.append("%s%s%s" % (hs[0],httppad,hs[1]))
            elif x.find("<script") > -1:
                self.regels.append(hs[0])
                f2 = file(filepad + 'check.js')
                for x in f2.readlines():
                    self.regels.append(x[:-1])
                f2.close()
                self.regels.append(hs[1])
            elif x.find(".py") > -1:
                self.regels.append("%s%s%s" % (hs[0],cgipad,hs[1]))
            elif x.find("option") > -1:
                for x in lk.lk:
                    self.regels.append("%s%s%s%s%s" % (hs[0],x[1],hs[1],x[0],hs[2]))
            elif x.find("Gebruikers") > -1:
                #~ print xslevel
                if xslevel == 1 or xslevel == '1':
                    hj = 'submit'
                else:
                    hj = 'hidden'
                #~ print hj
                self.regels.append(hj.join(hs))
        else:
            if x[:-1] == "<!-- kop -->":
                for y in printkop("Startscherm",u):                  # gedefinieerd in school_globals
                    self.regels.append(y)
            else:
                self.regels.append(x[:-1])
    fh.close()

def main():
    l = start_main("1")
    f = file("test.html","w")
    for x in l.regels:
      f.write("%s\n" % x)
    f.close()

if __name__ == '__main__':
	main()
