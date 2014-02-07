#!/usr/bin/env python
# coding: utf8
import datetime

today = datetime.datetime.now().strftime("%A %d de %B de %Y")

meses = {'January':'Enero',
         'Febrary':'Febrero',
         'March':'Marzo',
         'April':'Abril',
         'June':'Junio',
         'July':'Julio',
         'August':'Agosto',
         'September':'Septiembre',
         'October':'Octubre',
         'November':'Noviembre',
         'December':'Diciembre'}

dias = {'Sunday':'Domingo',
        'Monday':'Lunes',
        'Tuesday':'Martes',
	'Wednesday':'Miercoles',
	'Thursday':'Jueves',
	'Friday':'Viernes',
	'Saturday':'Sabado'}

partes = today.split()

hoy = ''

for parte in partes:
    if parte in dias:
        hoy += dias[parte]
        print dias[parte]
    elif parte in meses:
        hoy += meses[parte]
        print meses[parte]
    else:
        hoy += parte
        print parte
    hoy += " "

print hoy+"traducida!"

fecha = today

for dia in dias:
    fecha = fecha.replace(dia, dias[dia])
for mes in meses:
    fecha = fecha.replace(mes, meses[mes])
print fecha


