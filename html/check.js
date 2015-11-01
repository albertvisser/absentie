// js-functie aanroepen in html en python
// start.html: doit(), doit_sel() - start_main.py: gebruikt check.js
// toon_klas.html: doit_sel() - sel_ll_main.py: gebruikt check.js voor doit_sub() en doit()
// - toon_kl_main.py: gebruikt check.js voor doit_sub() en doit()
// toon_absent.html: doit_sel() - toon_abs_main.py: gebruikt check.js voor  doit_sub() en doit()
// toon_leerling.html: doit(), isChanged(), isUnchanged() - toon_llabs_main.py: gebruikt check.js voor
// users.html: %s - toon_us_main.py: gebruikt check.js voor doit_edit(), doit_edit(), doit_wpw() en doit_woord()
// login.html: check_login() - start_main.py: gebruikt check.js
// newpw.html: check_npw() - wijzig_us_main.py: gebruikt check_js voor doit()
// groepen.html: %s - toon_gr_main.py: gebruikt check.js voor doit_edit(), doit_edit() en doit_woord()
// leerlingen.html: %s - toon_ll_main.py: gebruikt check.js voor doit_edit(), doit_edit() en doit_naam()
// leerkrachten.html: %s - toon_lk_main.py: gebruikt check.js voor doit_edit(), doit_edit() en doit_naam()
// school_globals.py: printkop() zet in document kop doit()

function getCookieVal (offset) {
    var endstr = document.cookie.indexOf (";", offset);
    if (endstr == -1)
        endstr = document.cookie.length;
    return unescape(document.cookie.substring(offset, endstr));
    }
function GetCookie (name) {
    var arg = name + "=";
    var alen = arg.length;
    var clen = document.cookie.length;
    var i = 0;
    while (i < clen) {
        var j = i + alen;
        if (document.cookie.substring(i, j) == arg)
            return getCookieVal (j);
        i = document.cookie.indexOf(" ", i) + 1;
        if (i == 0) break;
        }
    return null;
    }
function doit(naam1,naam2) {
    document.getElementById(naam1).value = GetCookie('usernaam') ;
    document.getElementById(naam2).value = GetCookie('sessionid');
    return true;
    }
function doit_sel(naam1,naam2,naam3) {
    var fout = '';
    var v = document.getElementById(naam1);
    var w = document.getElementById("chkAbs");
    if (v.value == '' && w.checked == false) {
        fout = 'U moet wel invullen waar u naar zoeken wilt';
        alert(fout);
        v.focus();
        }
    else
        doit(naam2,naam3);
    doit_retval = (fout == '');
    }
function doit_woord(naam1,tekst,naam2,naam3) {
    var fout = '';
    var v = document.getElementById(naam1);
    if (v.value == '') {
        fout = tekst + ' invullen s.v.p.';
        alert(fout);
        v.focus();
        }
    else
        doit(naam2,naam3);
    doit_retval = (fout == '');
    }
function doit_naam(naam1,naam2,naam3,naam4) {
    var fout = '',pos='';
    var v = document.getElementById(naam1);
    if (v.value == '')
        fout = 'voor'
    else {
        v = document.getElementById(naam2);
        if (v.value == '')
            fout = 'achter'
        }
    if (fout != '') {
        fout = 'voor- en achternaam beide invullen s.v.p.';
        alert(fout);
        v.focus();
        }
    else
        doit(naam3,naam4);
    doit_retval = (fout == '');
    }
function doit_sub(fnaam,naam1,naam2) {
    doit(naam1,naam2);
    document.getElementById(fnaam).submit()
    return true;
    }
// komt uit toon_us_main: t.b.v. naar wijzigen password
function doit_wpw(naam1,naam2,idnr) {
    doit(naam1,naam2);
    document.getElementById('hPw').value = 'J';
    return true;
    }
// komt uit toon_us_main: screening combinatie beginscherm/zoekstring
// werkte niet? wordt in elk geval niet meer gebruikt
function doit3(naam1,naam2) {
    var i='',j='',fout='';
    i = document.getElementById(naam1).value;
    j = document.getElementById(naam2).value;
    if ((i == 'toon_klas') || (i = 'sel_leerling'))
        if (j == '')
            fout = 'Bij dit scherm is een zoekargument verplicht';
    else
        if (j != '')
            fout = 'Bij dit scherm geen zoekargument opgeven';
    document.doit3_returnValue = (fout == '');
    }
function doit_edit(naam1,naam2,idnr) {
    doit(naam1,naam2);
    document.getElementById('edit').value = idnr;
    return true;
    }
// controleer of alle velden (tPwO, tPw, tPw2) gevuld zijn, bovendien of tPw en tPw2 gelijk zijn
function check_npw() { //v4.0
    var x='',y='',z='',errors='';
    x=document.getElementById('tPwO').value;
    y=document.getElementById('tPw').value;
    z=document.getElementById('tPw2').value;
    if (x==''||y==''||z=='') {
        errors = 'leeg';
        alert('Alle velden moeten worden ingevuld');
        }
    else {
        if (z!=y) {
            errors = 'ongelijk';
            alert('Het nieuwe wachtwoord is niet correct herhaald, probeer opnieuw');
        }
    }
    doit('wu1','wu2');
    document.MM_returnValue = (errors == '');
}
function check_login(naam1,naam2) { //v4.0
  var i='',j='',error='';
  i = document.getElementById(naam1).value;
  j = document.getElementById(naam2).value;
  if (i=='' && j=='')
  	error = 'Zowel gebruikersnaam als wachtwoord moeten worden ingevuld' ;
	else
	if (j=='')
		error = 'U moet wel een wachtwoord opgeven' ;
	else
		if (i=='')
			error = 'U moet wel een gebruikersnaam opgeven' ;
  if (error)
  	alert(error);
  document.MM_returnValue = (error == '');
}
function isChanged() {
    var x = document.getElementById('bWijz');
    if (x.disabled)
         x.disabled=false;
    var x = document.getElementById('bReset');
    if (x.disabled)
         x.disabled=false;
}
function isUnchanged() {
    var x = document.forms.fWijzig;
    x.reset()
    x = document.getElementById('bWijz');
    if (x.disabled==false)
         x.disabled=true;
    x = document.getElementById('bReset');
    if (x.disabled==false)
         x.disabled=true;
}
function check_llabs() {
    var i='',j='',error='';
    var x = document.getElementById('selStat');
    i = x.options[x.selectedIndex].index;
    j = document.getElementById('txtReden').value;
    if (i=='2' && j=='')
        error='U moet wel een reden opgeven';
    if (error)
        alert(error);
    else
        doit('wla1','wla2');
    document.check_retval = (error == '');
}
function isDateOK() {
    var d=0,m=0,j=0,err='';
    var x = document.getElementById('selDag');
    d = x.options[x.selectedIndex].index + 1;
    x = document.getElementById('selMnd');
    m = x.options[x.selectedIndex].index + 1;
    x = document.getElementById('selJaar');
    j = x.options[x.selectedIndex].index + 1;
    if ((m==4||m==6||m==9||m==11) && (d==31))
        err='fout';
    else
        if ((m==2)&&(d>29))
            err='fout';
        else
            if ((m==2)&&(d>28)&&(j!=4*floor(j/4)))
                err='fout';
    if (err)
        alert('Foute datum');
    else
        isChanged();
    document.MM_returnValue = (err == '');
}
function isEnddatOK() {
    // alle indexen zijn 1 hoger omdat hier ook een waarde 'niet van toepassing' mogelijk is
    var d=0,m=0,j=0,err='';
    var x = document.getElementById('eindDag');
    d = x.options[x.selectedIndex].index;
    x = document.getElementById('eindMnd');
    m = x.options[x.selectedIndex].index;
    x = document.getElementById('eindJaar');
    j = x.options[x.selectedIndex].index;
    if ((d==0&&(m!=0||j!=0))||(m==0&&(d!=0||j!=0))||(j==0&&(d!=0||m!=0)))
        err='nietleeg';
    else
        if ((m==4||m==6||m==9||m==11) && (d==31))
            err='fout';
        else
            if ((m==2)&&(d>29))
                err='fout';
            else
                if ((m==2)&&(d>28)&&(j!=4*floor(j/4)))
                    err='fout';
    if (err) {
        tekst = 'Foute datum';
        if (err!='fout')
            tekst += ' (niet leeg)';
        alert(tekst);
        }
    else
        isChanged();
    document.MM_returnValue = (err == '');
}
