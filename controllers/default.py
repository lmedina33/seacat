# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

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
        ## If the user is successfully logged in we store the timestamp in the DB.
        db.auth_user[auth.user.id]=dict(last_login=request.now)
        ## Then we redirect to the "Start Page"
        redirect(URL('start'))
    #if form.accepts(request.vars, session):
        #redirect(URL('start'))
    #elif form.errors:
        #response.flash = 'Usuario/Contraseña incorrectos'
    #else:
        #response.flash = 'Por favor, complete el formulario de inicio de sesión o seleccione un botón'
    return dict(message=T("Registration System"), form=form)

def info():
    return dict(info=info)

#@auth.requires_login()
#def ingreso():
#    auth.settings.actions_disabled = [ 'register' ]
#    form = auth.profile()
#    return dict(ingreso=ingreso, form=form)

@auth.requires_login()
def start():
     #response.flash = T("Welcome back ") + auth.user.first_name + " " + auth.user.last_name + "!"
     #response.flash = auth.user.id
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

@auth.requires_permission('create new father', db.auth_user)
def new_father():
    form = SQLFORM.factory(
                           Field('first_name', required=True, requires=IS_NOT_EMPTY(), label=T("First Name")),
                           Field('middle_name', label=T("Middle Name")),
                           Field('last_name', required=True, requires=IS_NOT_EMPTY(), label=T("Last Name")),
                           Field('email', required=True, requires=[IS_EMAIL(),
                                                                   IS_NOT_IN_DB(db, 'auth_user.email',
                                                                                            error_message=T("This email is already in our database, please choose another one"))],
                                                                                            label=T("email")),
                           Field('password', required=True, requires=[IS_MATCH('\d{8}', error_message=T("Please, only numbers")), CRYPT()], label=T("Document")),
                           Field('obs', 'text', label=T("Observations"))
                           )
    if form.process().accepted:
        new_user_id = db.auth_user.insert(first_name=form.vars.first_name,
                                          middle_name=form.vars.middle_name,
                                          last_name=form.vars.last_name,
                                          email=form.vars.email,
                                          password=form.vars.password,
                                          obs=form.vars.obs)
        db.auth_membership.insert(user_id=new_user_id,
                                  group_id=db.auth_group(role='padre').id)
        response.flash = T("new record inserted")
        redirect(URL('start'))
    elif form.errors:
        response.flash = T("Form has errors")
    return dict(form=form)
