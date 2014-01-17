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
        ## If the user is successfully logged in we store the timestamp in the 'auth_user' table.
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

@auth.requires_membership('root')
def admin_users():
    grid = SQLFORM.smartgrid(db.auth_user,
                             fields=[db.auth_user.id,
                                     db.auth_user.first_name,
                                     db.auth_user.middle_name,
                                     db.auth_user.last_name,
                                     db.auth_user.email,
                                     db.auth_user.obs,
                                     db.auth_user.last_login,
                                     db.auth_user.personal_data_id,
                                     db.auth_user.address_id],
                             maxtextlengths={'auth_user.email': 50},
                             showbuttontext=False,
                             orderby='auth_user.last_name',
                             paginate=50,
                             links_in_grid=False,
                             exportclasses=dict(csv=True, csv_with_hidden_cols=False, json=False, tsv=False, tsv_with_hidden_cols=False, xml=True))
    return locals()

@auth.requires_membership('root')
def admin_user_groups():
    grid = SQLFORM.grid(db.auth_group,
                        maxtextlengths={'auth_group.description': 50},
                        showbuttontext=False,
                        orderby='auth_group.role',
                        paginate=50,
                        links_in_grid=False,
                        exportclasses=dict(csv=True, csv_with_hidden_cols=False, json=False, tsv=False, tsv_with_hidden_cols=False, xml=True))
    return locals()

@auth.requires_membership('root')
def admin_user_memberships():
    grid = SQLFORM.smartgrid(db.auth_membership,
                             maxtextlengths={'auth_membership.user_id': 50},
                             showbuttontext=False,
                             #orderby=db.auth_user.last_name,
                             paginate=50,
                             links_in_grid=False,
                             exportclasses=dict(csv=True, csv_with_hidden_cols=False, json=False, tsv=False, tsv_with_hidden_cols=False, xml=True))
    return locals()

@auth.requires_membership('root')
def admin_user_permissions():
    grid = SQLFORM.smartgrid(db.auth_permission,
                             maxtextlengths={'auth_permission.name': 50},
                             showbuttontext=False,
                             paginate=50,
                             links_in_grid=False,
                             exportclasses=dict(csv=True, csv_with_hidden_cols=False, json=False, tsv=False, tsv_with_hidden_cols=False, xml=True))
    return locals()

@auth.requires_membership('root')
def upload_image():
    grid = SQLFORM.smartgrid(db.images)
    return locals()

@auth.requires_permission('create new father', db.auth_user)
def new_father():
    form = SQLFORM.factory(db.auth_user, db.priority_father)
    if form.process().accepted:
        new_user_id = db.auth_user.insert(**db.auth_user._filter_fields(form.vars))
        db.auth_membership.insert(user_id=new_user_id,
                                  group_id=db.auth_group(role='padre').id)
        db.priority_father.insert(father_id=new_user_id, **db.priority_father._filter_fields(form.vars))
        db.auth_user[new_user_id]=dict(created_on=request.now)
        response.flash = T("new record inserted")
        redirect(URL('start'))
    elif form.errors:
        response.flash = T("Form has errors")
    return dict(form=form)

@auth.requires_permission('create new user', db.auth_user)
def new_user():
    form = SQLFORM.factory(db.auth_user,
                           Field('role', required=True, requires=IS_IN_DB(db, 'auth_group.role', '%(description)s'), notnull=True, label=T("Role"))
                          )

    if form.process().accepted:
        ## After proccessing the form, we insert the data in the 'auth_user' table.
        new_user_id = db.auth_user.insert(**db.auth_user._filter_fields(form.vars))
        ## And then we insert the membership of the new user.
        db.auth_membership.insert(user_id=new_user_id,
                                  group_id=db.auth_group(role=form.vars.role).id)
        ## We set the 'created_on' field to the current datetime.
        db.auth_user[new_user_id]=dict(created_on=request.now)
        response.flash = T("new record inserted")
        redirect(URL('start'))
    elif form.errors:
        response.flash = T("Form has errors")
    return dict(form=form)

def new_personal_data():
    username = auth.user.last_name + ", " + auth.user.first_name + " " + auth.user.middle_name
    form = SQLFORM.factory(
                           Field('first_name', required=True, notnull=True, label=T("First Name"), writable=False, default=auth.user.first_name),
                           Field('middle_name', label=T("Middle Name"), writable=False, default=auth.user.middle_name),
                           Field('last_name', required=True, notnull=True, label=T("Last Name"), writable=False, default=auth.user.last_name),
                           Field('mail1', required=True, requires=IS_EMAIL(), notnull=True, label=T("Principal email"), writable=False, default=auth.user.email),
                           Field('doc_type', required=True, requires=IS_IN_SET(doc_type_set), notnull=True, default=doc_type_set[0], label=T("Document Type")),
                           Field('doc', 'string', length=8, required=True, requires=IS_MATCH('\d{8}'), notnull=True, unique=True, label=T("Document"), comment=T("Insert only numbers without dots. i.e.: 12654897")),
                           Field('nac', required=True, notnull=True, default="Argentina", label=T("Nacionality")),
                           Field('cuil', 'string', length=11, requires=IS_MATCH('\d{11}'), notnull=True, unique=True, label="CUIL"),
                           Field('mail2', requires=IS_EMPTY_OR(IS_EMAIL()), label=T("Alternative email"), comment=T("Another contact mail")),
                           Field('tel1_type', required=True, requires=IS_IN_SET(tel_type_set), notnull=True, default=tel_type_set[0], label=T("Principal Phone Type")),
                           Field('tel1', length=8, required=True, requires=IS_MATCH('\d{8}'), notnull=True, label=T("Principal Phone Number")),
                           Field('tel2_type', requires=IS_IN_SET(tel_type_set), default=tel_type_set[0], label=T("Alternative Phone Type")),
                           Field('tel2', length=8, requires=IS_MATCH('\d{8}'), label=T("Alternative Phone Number")),
                           Field('street', required=True, notnull=True, label=T("Street")),
                           Field('building', 'integer', label=T("Building")),
                           Field('floor', label=T("Floor")),
                           Field('door', label=T("Door")),
                           Field('apartment', label=T("Apartment")),
                           Field('street1', label=T("Street 1")),
                           Field('street2', label=T("Street 2")),
                           Field('zip_code', label=T("ZIP Code")),
                           Field('loc', default=provinces[2], label=T("Locality")),
                           Field('prov', requires=IS_IN_SET(provinces), default=provinces[2], label=T("Province")),
                           Field('obs', 'text', label=T("Observations")),
                           Field('photo', 'upload', requires=IS_EMPTY_OR(IS_IMAGE(extensions=valid_image_extensions, maxsize=photo_size)), label=T("Photo")),
                           Field('avatar', 'upload', requires=IS_EMPTY_OR(IS_IMAGE(extensions=valid_image_extensions, maxsize=avatar_size)), label=T("Avatar")),
                           Field('twitter', requires=IS_EMPTY_OR(IS_URL()), label=T("Twitter Profile")),
                           Field('facebook', requires=IS_EMPTY_OR(IS_URL()), label=T("Facebook Profile")),
                           Field('obs', 'text', label=T("Observations")),
                          )
    if form.process().accepted:
        data_id = db.personal_data.insert(**db.personal_data._filter_fields(form.vars))
        addr_id = db.address.insert(**db.address._filter_fields(form.vars))
        db.auth_user[auth.user.id]=dict(personal_data_id=data_id, address_id=addr_id)
        response.flash = T("Record inserted")
    return dict(form=form, user=username)

@auth.requires(auth.has_permission('view fathers list', db.auth_user) or auth.has_permission('view users list', db.auth_user))
def users_list():
    form = SQLFORM.factory(Field('role', requires=IS_IN_DB(db, 'auth_group.role', '%(description)s'), label=T("Role")))
    query = (db.auth_membership.group_id==db.auth_group.id)&(db.auth_membership.user_id==db.auth_user.id)&(db.auth_group.role==request.vars.role)
    fields = [db.auth_user.id,
              db.auth_user.first_name,
              db.auth_user.middle_name,
              db.auth_user.last_name,
              db.auth_user.email,
              db.auth_user.created_on,
              db.auth_user.last_login,
              db.auth_group.description]
    #rows = db(query).select()
    grid = SQLFORM.grid(query,
                        fields=fields,
                        maxtextlengths={'auth_user.id': 5,
                                        'auth_user.first_name': 20,
                                        'auth_user.middle_name': 20,
                                        'auth_user.last_name': 20,
                                        'auth_user.email': 50,
                                        'auth_user.created_on': 20,
                                        'auth_user.last_login': 20},
                        create=False,
                        deletable=False,
                        details=False,
                        editable=False,
                        searchable=False,
                        csv=False,
                        paginate=50)
    return dict(form=form, grid=grid)
