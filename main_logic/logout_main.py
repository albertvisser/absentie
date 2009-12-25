from school_globals import *
from school_user import User
from start_main import start_main

class logout_main:
    def __init__(self,userid,session):
        self.regels = []
        dh = User(userid,session,True)
        if dh.endSession():
            fn = filepad + "logout.html"
            kop = "Uitloggen"
        else:
            fn = filepad + "next.html"
            kop = "Login fout"
        f = file(fn,"r")
        for x in f.readlines():
            h = x.find("%s")
            if h > -1:
                hs = x[:-1].split("%s")
                if x.find("stylesheet") > -1:
                    self.regels.append(httppad.join(hs))
                elif x.find("button") > -1:
                    self.regels.append(cgipad.join(hs))
                elif x.find("uitgelogd") > -1:
                    self.regels.append(userid.join(hs))
            elif x[:-1] == "<!-- kop -->":
                for y in printkop(kop,userid):                  # gedefinieerd in school_globals
                    self.regels.append(y)
            elif x[:-1] == "<!-- data -->":
                self.regels.append('<br /><div>%s</div>' % ok)
            else:
                self.regels.append(x[:-1])
        f.close()

def main():
    h = logout_main('woefdram')
    for x in h.regels:
        print x

if __name__ == "__main__":
    main()
