Files in this directory
=======================

cgi-bin
-------
    cgi scripts

    school_login.py
        opbouwen login pagina
        gebruikt cgi
        importeert school_progpad
            login_main uit start_main
    school_logout.py
        opbouwen pagina na (automatische) logout?
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            logout_main uit logout_main
    school_progpad.py
        pad naar de programmatuur en data
    school_start.py
        opbouwen startpagina
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            start_main uit start_main
    sel_leerling.py
        opbouwen scherm selecteren leerling
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            sel_ll_main uit sel_ll_main
    toon_absent.py
        opbouwen absentiescherm
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            toon_abs_main uit toon_abs_main
    toon_groepen.py
        opbouwen scherm selecteren groep
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            toon_gr_main uit toon_gr_main
    toon_klas.py
        opbouwen scherm toon leerlingen in klas
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            toon_kl_main uit toon_kl_main
    toon_leerkrachten.py
        opbouwen scherm toon leerkrachten
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            toon_lk_main uit toon_lk_main
    toon_leerlingen.py
        opbouwen scherm toon_leerlingen
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            toon_ll_main uit toon_ll_main
    toon_llabsent.py
        opbouwen scherm toon absente leerlingen
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            toon_llabs_main uit toon_llabs_main
    toon_users.py
        opbouwen scherm toon users
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            toon_us_main uit toon_us_main
    wijzig_groep.py - linkt door naar?
        wijzig groep, bij ok doorlinken naar toon_groepen.py
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            wijzig_gr_main uit wijzig_gr_main
            GRgeg uit Edex_objects (niet nodig)
    wijzig_leerkracht.py
        wijzigen leerkracht, bij ok doorlinken naar toon_leerkrachten.py
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            wijzig_lk_main uit wijzig_lk_main
    wijzig_leerling.py
        wijzigen leerling, bij ok doorlinken naar toon_leerlingen.py
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            wijzig_ll_main uit wijzig_ll_main
    wijzig_llabsent.py
        wijzigen absentie, tonen opgebouwde regels
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            toon_llabs_main uit toon_llabs_main
            wijzig_llabs_main uit wijzig_llabs_main
    wijzig_user.py
        wijzigen user, bij ok doorlinken naar ingestelde programma (toon_users.py)
        gebruikt cgi
        importeert school_progpad
            check_login, meld_fout uit check_login
            wijzig_us_main, wijzig_pw_main, wijzig_pw_vraag uit wijzig_us_main

data
----
    data manipulatie routines, aangeroepen vanuit verwerkingsroutines

    Edex_objects.py
        alles behalve de user administratie
        gebruikt copyfile uit shutil
        importeert filepad uit globals
    globals.py
        pad naar de data
    school_user.py
        de user administratie
        gebruikt xml.sax
        importeert xmlpad uit globals

html
----
    html sources e.d.

    about.html
        info pagina
    check.js
        javascript login/sessie check
    favicon.ico
        site icon
    groepen.html
        lijst groepen
    index.html
        opstarten startscherm
    kop.html
        schermkop met link naar about.html
    leerkrachten.html
        lijst leerkrachten
    leerlingen.html
        lijst leerlingen (na zoeken op naam(deel)?)
    login.html
        login scherm
    logout.html
        'u bent uitgelogd' scherm
    mheenlogo.gif
        school logo
    Mylogo3.gif
        applicatie logo
    newpw.html
        wijzigen wachtwoord
    next.html
        tonen foutmelding bij login
    school.css
        styling
    start.html
        startscherm
    toon_absent.html
        lijst absenties
    toon_klas.html
        lijst leerlingen in klas
    toon_leerling.html
        toon leerlinggegevens met absentie
    users.html
        gebruikers scherm
    users_new.html
        nieuwe versie met de controls in de html, nergens gebruikt

main_logic
----------
    verwerkingsroutines, aangeroepen vanuit cgi responses
    deze vullen de html sources verder in
    aan de hand van de opgehaalde gegevens

    check_login.py
        controleren login en evt foutmelding geven
        gebruikt next.html
        importeert school_globals; User uit school_user
    login_main.py   zit ook in start_main
        gebruikt next.html
        importeert school_globals, User uit school_user
            start_main uit start_main
            toon_kl_main uit toon_kl_main
            sel_ll_main uit sel_ll_main
            toon_abs_main uit toon_abs_main
    logout_main.py
        gebruikt logout.html, next.html
        importeert school_globals, User uit school_user
            start_main uit start_main (niet gebruikt)
    meldfout.py
        meld_fout routine in een aparte module
    school_globals.py
        pad naar data; diverse standaard instellingen en routines
        w.o. schermkop routine
        gebruikt kop.html

    sel_ll_main.py
        gebruikt toon_klas.html
        importeert school_globals
            LKgeg, zoekLL, lijstGR en lijstAbsent uit Edex_objects
    start_main.py
        gebruikt login.html, start.html
        importeert school_globals, lijstLK uit Edex_objects
    toon_abs_main.py
        gebruikt toon_absent.html
        importeert school_globals
            lijstLL, lijstGR, lijstAbsent uit Edex_objects
    toon_gr_main.py
        gebruikt groepen.html
        importeert school_globals
            lijstGR, lijstLK uit Edex_objects
    toon_kl_main.py
        gebruikt toon_klas.html
        importeert school_globals
            lijstLLbijLK, lijstAbsent uit Edex_objects
    toon_lk_main.py
        gebruikt leerkrachten.html
        importeert school_globals
            LKgeg, lijstLK, lijstGRO uit Edex_objects
    toon_llabs_main.py
        gebruikt toon_leerling.html
        importeert school_globals
            LLgeg, AbsentHist uit Edex_objects
    toon_ll_main.py
        gebruikt leerlingen.html
        importeert school_globals
            lijstLL, LLgeg, lijstGRO, GRgeg uit Edex_objects
    toon_us_main.py
        gebruikt users.html
        importeert school_globals
            UserLijst, User uit school_user
    toon_us_main_new.py
        andere opzet van vorige
        gebruikt users.html
        importeert school_globals
            UserLijst, User uit school_user
    wijzig_gr_main.py
        importeert school_globals
            lijstGR (niet gebruikt), GRgeg uit Edex_objects
    wijzig_lk_main.py
        importeert school_globals
            LKgeg, lijstLK uit Edex_objects
    wijzig_llabs_main.py
        importeert school_globals
            LLgeg uit Edex_objects
            localtime uit time
    wijzig_ll_main.py
        importeert school_globals
            LLgeg, lijstLL uit Edex_objects
    wijzig_us_main.py
        gebruikt newpw.html
        importeert school_globals
            UserLijst, User uit school_user
