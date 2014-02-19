#!/usr/bin/env python
#coding: utf-8

import hashlib

def computeMD5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

name = raw_input("Ingrese su nombre: ")
last_name = raw_input("Ingrese su apellido: ")

print type(computeMD5(name+last_name))

