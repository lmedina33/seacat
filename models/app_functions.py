# coding: utf8
import datetime
import locale
import hashlib
import os
locale.setlocale(locale.LC_TIME, '')

NOW = now = datetime.datetime.now()

if SUSPEND_SERVICE:
    message = "<html><body><h2>"
    message += T("System is under maitenance, please come back later.")
    message += "</h2><h3>"
    message += T("Sorry for the inconvenience")
    message += "</h3><p>"
    message += str(NOW)
    message += "</p></body></html>"
    raise HTTP(503, message)

def translate_date(date):
    """
    Receives a date an translate into long format from English to Spanish.
    """
    for i in DAYS_TR:
        date = date.replace(i, DAYS_TR[i])
    for i in MONTH_TR:
        date = date.replace(i, MONTH_TR[i])
    return date

def simple_fullname(id):
    """
    Based on ID search on auth_user and returns: "LASTNAME, FIRST_NAME MIDDLE_NAME"
    """
    fullname =  db.auth_user(id=id).last_name+", "+db.auth_user(id=id).first_name+" "+db.auth_user(id=id).middle_name
    return fullname

def fullname(id):
    """
    Based on ID search on auth_user and returns: "LASTNAME, FIRST_NAME MIDDLE_NAME (ID)"
    """
    fullname =  simple_fullname(id)+" ("+str(id)+")"
    return fullname

## To install dateutil: sudo pip install python-dateutil.
from dateutil import relativedelta as rdelta
def diff_in_years(date):
    """
    Calculate the difference in years between date and now.
    If "date" isn't an instance of datetime.date it returns None.
    """
    try:
        return rdelta.relativedelta(datetime.datetime.today().date(), date).years
        #return rdelta.relativedelta(datetime.datetime.today().date(), row['personal_data']['dob']).years
    except:
        return None

def send_welcome_mail(form, id):
    mensaje = "Estimad"

    if db.auth_user(db.auth_user.id==id).gender == "F":
        mensaje += "a"
    else:
        mensaje += "o"

    mensaje += """ %(first_name)s,
gracias por registrarte en el Pío IX, estamos muy contentos de nos hayas elegido.

Para continuar tienes que hacer click sobre el siguiente link: https://10.1.0.21:8000/SEACAT_ingresos
e ingresar al sitio con tu dirección de correo electrónico: %(email)s
Tu contraseña será tu número de documento: %(doc)s
(No te preocupes! Te vamos a pedir que cambies tu contraseña inmediatamente después de que ingreses por primera vez).

Tenés una semana para completar este primer paso de la inscripción. Después de ese tiempo tendrás que acercarte de nuevo al colegio o llamar para renovar tu usuario.

Saludos,
La Comunidad del Pío IX.""" % {'first_name': form.vars.first_name, 'email': form.vars.email, 'doc': form.vars.doc}

    message = """
Dear %(first_name)s,
thanks for registering in Pío IX, we are pleased that you have chosen us.

For this to continue you must go to the following link: http://inscripciones.pioix.edu.ar/
and login with your email: %(email)s
Your password will be your document number: %(doc)s
(don't panic! You will be asked to change your password immediately after the first login).

You have a week to complete the first step of registration. After this you will have to call or go to the school to renew your user.

Greetings,
The Pío IX Community.""" % {'first_name': form.vars.first_name, 'email': form.vars.email, 'doc': form.vars.doc}

    mail.send(to=[form.vars.email],
              subject=T("Welcome to Pío IX registration system (SEACAT)"),
              reply_to='no_responder@pioix.edu.ar',
              message=mensaje
    )
    auth.log_event(description="Mail sent to %s" % fullname(id))

def select_user_from_group(role):
    db((db.auth_user.id==db.auth_membership.user_id)&
       (db.auth_membership.group_id==db.auth_group.id)&
       (db.auth_group.role==role)).select()

def computeMD5(string):
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

def email(sender,to,subject='test',message='test',server='localhost:25',auth=None):
        """
        Sends an email. Returns True on success, False on failure.
        """
        if not isinstance(to,list): to=[to]
        try:
            try:
                from google.appengine.api import mail
                mail.send_mail(sender=sender,
                               to=to,
                               subject=subject,
                               body=message)
            except ImportError:
                msg="From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"%(sender,\
                    ", ".join(to),subject,message)
                import smtplib, socket
                host, port=server.split(':')
                # possible bug fix? socket.setdefaulttimeout(None)
                server = smtplib.SMTP(host,port)
                #server.set_debuglevel(1)
                if auth:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    username, password=auth.split(':')
                    server.login(username, password)
                server.sendmail(sender, to, msg)
                server.quit()
        except Exception,e:
            return False
        else: return True

def is_odd(num):
    return num & 0x1

def calculate_participants(date_id):
    """
    This functin receives a date ID an returns the amount of row in the table turn with the given ID
    """
    count_id = db.turn.uid.count()
    registro = db((db.date.id==db.turn.date)
                  &(db.date.id==date_id)).select(count_id, groupby=[db.date.id, db.date.date]).first()
    return registro._extra[count_id]
