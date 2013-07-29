#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
cgitb.enable()
import shared
from start_main import Login

def main():
    print("Content-Type: text/html\n")     # HTML is following
    l = Login()
    for x in l.regels:
      print(x)

if __name__ == '__main__':
	main()
