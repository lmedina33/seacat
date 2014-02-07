# coding: utf8

## This file contains global settings and constants.

import datetime
import locale
locale.setlocale(locale.LC_TIME, '')

####################################################################################################
## DB Settings
####################################################################################################

#DBURI='\'postgres://user:password@host/database\', check_reserved=[\'postgres\']'
DB_ENGINE=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_DB=''
DBURI=DB_ENGINE+'://'+DB_USER+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_DB

####################################################################################################
## To suspend the service for maitenance change this value to "True", this will raise a HTTP 503
## ("Service unavailable")
####################################################################################################

SUSPEND_SERVICE = False

####################################################################################################
## Constants and Lists
####################################################################################################

NOW = datetime.datetime.now()

GENDER_LIST = [T("Male"), T("Female")]

PROVINCES_LIST = ["Buenos Aires",
                  "Catamarca",
                  "Ciudad Autónoma de Buenos Aires",
                  "Chaco",
                  "Chubut",
                  "Corrientes",
                  "Córdoba",
                  "Entre Ríos",
                  "Formosa",
                  "Jujuy",
                  "La Pampa",
                  "La Rioja",
                  "Mendoza",
                  "Misiones",
                  "Neuquén",
                  "Río Negro",
                  "Salta",
                  "San Juan",
                  "San Luis",
                  "Santa Cruz",
                  "Santa Fe",
                  "Santiago del Estero",
                  "Tierra del Fuego, Antártida e Islas del Atlántico Sur",
                  "Tucumán"
                 ]

SCHOOL_NETWORK_LIST = ["San Francisco de Sales", "San Antonio", "San Pedro", "San Juan Evangelista"]

DOC_TYPE_SET = ['DNI', 'LE', 'LC', T("PASSPORT")]

TEL_TYPE_SET = [T("Line"), T("Cell Phone"), T("Other")]

VALID_IMG_EXTENSION_SET = ('jpeg', 'jpg', 'png')

MAX_PHOTO_SIZE = (640, 480)

MAX_AVATAR_SIZE = (300, 300)

DATE_TYPE = [T("meeting"), T("turn"), T("expiration"), T("exam"), T("opening")]

GENERAL_DATE_TYPE = [T("Open Enrollment"),
                     T("Enrollment Deadline"),
                     T("Deadline for Priority"),
                     T("First Parent Meeting (First Date)"),
                     T("First Parent Meeting (Second Date)"),
                     T("Language Exam"),
                     T("Math Exam"),
                     T("Report Cards Presentation Deadline"),
                     T("Pre-Registered List's Publication")
                     ]

DATE_FORMAT = '%d-%m-%Y'

TIME_FORMAT = '%H:%M:%S'

MONTH_TR = {'January':'Enero',
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

DAYS_TR = {'Sunday':'Domingo',
           'Monday':'Lunes',
           'Tuesday':'Martes',
	       'Wednesday':'Miercoles',
	       'Thursday':'Jueves',
	       'Friday':'Viernes',
	       'Saturday':'Sabado'}

def translate_date(date):
    for i in DAYS_TR:
        date = date.replace(i, DAYS_TR[i])
    for i in MONTH_TR:
        date = date.replace(i, MONTH_TR[i])
    return date
