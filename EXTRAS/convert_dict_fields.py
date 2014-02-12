#!/usr/bin/env python
# coding: utf8

import datetime

form_vars = {"Apertura_de_Inscripciones_date":datetime.date(2014, 2, 3),
             "Apertura_de_Inscripciones_start_time":datetime.time(18, 30),
             "Apertura_de_Inscripciones_end_time":datetime.time(19, 00),
             "Cierre_de_Inscripciones_date":None,
             "Cierre_de_Inscripciones_end_time":None,
             "Cierre_de_Inscripciones_start_time":None,
             "Examen_de_Lengua_date":None,
             "Examen_de_Lengua_end_time":None,
             "Examen_de_Lengua_start_time":None,
             "Examen_de_Matemática_date":None,
             "Examen_de_Matemática_end_time":None,
             "Examen_de_Matemática_start_time":None,
             "Fecha_Límite_de_Prioritarios_date":datetime.date(2014, 6, 5),
             "Fecha_Límite_de_Prioritarios_end_time":None,
             "Fecha_Límite_de_Prioritarios_start_time":None,
             "Fecha_Límite_de_entrega_de_Boletines_date":None,
             "Fecha_Límite_de_entrega_de_Boletines_end_time":None,
             "Fecha_Límite_de_entrega_de_Boletines_start_time":None,
             "Primera_Reunión_de_Padres_(Primera_Fecha)_date":datetime.date(2014,
                                                                             6,
                                                                             8),
             "Primera_Reunión_de_Padres_(Primera_Fecha)_end_time":datetime.time(20,
                                                                                 30),
             "Primera_Reunión_de_Padres_(Primera_Fecha)_start_time":datetime.time(19,
                                                                                   00),
             "Primera_Reunión_de_Padres_(Segunda_Fecha)_date":None,
             "Primera_Reunión_de_Padres_(Segunda_Fecha)_end_time":None,
             "Primera_Reunión_de_Padres_(Segunda_Fecha)_start_time":None,
             "Publicación_de_la_Lista_de_Preinscriptos_date":None,
             "Publicación_de_la_Lista_de_Preinscriptos_end_time":None,
             "Publicación_de_la_Lista_de_Preinscriptos_start_time":None,
             "id":None,
             "year":2014
            }

#print form_vars
year = form_vars['year']

print "The selected year is: %d" % year
print "Hay %d registros para analizar" % len(form_vars)
i = 0

for field, value in form_vars.items():
    fieldtype = ""
    date = ""
    start_time = ""
    end_time = ""
    i += 1
#    print "Analizando registro número {0}: {1} {2}".format(i, field, value)
#    print "\tAnalizando registro número %d: %s %s" % (i, field, value)
    if not value:
        continue
    if "_date" in field:
        fieldname = field.split("_date")
        fieldtype = fieldname[0].replace('_',' ')
        date = value
#        print fieldtype
        start_time = form_vars[fieldname[0]+"_start_time"]
        end_time = form_vars[fieldname[0]+"_end_time"]
    elif "_start_time" in field:
        continue
#        fieldname = field.split("_start_time")
#        if fieldtype == fieldname[0].replace('_',' '):
#            print "Start Time for " + fieldtype + ": " + str(value)
#            start_time = value
    elif "_end_time" in field:
        continue
#        fieldname = field.split("_end_time")
#        if fieldtype == fieldname[0].replace('_',' '):
#            print "End Time for " + fieldtype + ": " + str(value)
#            end_time = value
    elif "year" in field:
        continue
    else:
#        fieldtype = field
        pass
    print "\t\tFila: %s %d %s %s %s" % (fieldtype, year, date, start_time, end_time)
