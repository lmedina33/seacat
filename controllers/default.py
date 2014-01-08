# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

response.title = 'SEACAT'
response.subtitle = 'v.0.0.1b'
response.meta.author = 'Leandro E. Colombo Viña'
response.meta.description = 'Sistema de Inscripciones para el Colegio Pío IX'
response.meta.keywords = 'Inscripciones Pío IX'
#response.menu = [ [ 'Página Principal', True, URL('index') ] ]
response.logo = A(IMG(_src=URL('static', 'Logo_seacat_mini.png'), _alt="Logo de SEACAT"), _class="brand", _href="http://www.web2py.com/")

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Bienvenido al Sistema Escolar de Administración de Calificaciones y Acompañamiento Tutorial (SEACAT)")
    if not auth.is_logged_in():
        form = auth()
    else:
        redirect(URL('start'))
    #if form.accepts(request.vars, session):
        #redirect(URL('start'))
    #elif form.errors:
        #response.flash = 'Usuario/Contraseña incorrectos'
    #else:
        #response.flash = 'Por favor, complete el formulario de inicio de sesión o seleccione un botón'
    return dict(message='Sistema de Inscripciones', form=form)

def info():
    return dict(info=info)

@auth.requires_login()
def ingreso():
    auth.settings.actions_disabled = [ 'register' ]
    form = auth.profile()
    return dict(ingreso=ingreso, form=form)

@auth.requires_membership('root')
def start():
     return dict(start=start)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    auth.settings.actions_disabled = [ 'register' ]
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def test():
    grid = SQLFORM.smartgrid(db.auth_user)
    return locals()

@auth.requires_membership('root')
def admin_user_groups():
    grid = SQLFORM.grid(db.auth_group)
    return locals()

def admin_user_memberships():
    grid = SQLFORM.smartgrid(db.auth_membership)
    return locals()

def upload_image():
    grid = SQLFORM.smartgrid(db.image)
    return locals()
