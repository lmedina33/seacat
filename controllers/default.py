#-*- coding: utf-8 -*-
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
    if not auth.is_logged_in():
        form = auth()
    else:
        ## If the user is successfully logged in we store the timestamp in the 'auth_user' table.
        db.auth_user[auth.user.id]=dict(last_login=request.now)
        ## Then we redirect to the "Start Page"
        redirect(URL('start'))
    return dict(message=T("Registration System"), form=form)

@auth.requires_login()
@auth.requires_permission('not allowed', db.auth_user)
def set_up():
    ########################################################
    # No funciona, preguntarle a Mariano o a la Comunidad!
    ########################################################
#    if not SETTED_UP:
#    setting_up()
#    else:
#        redirect(URL('index'))
    db.auth_group.insert(role='root', description='Superadministrador')
    db.auth_group.insert(role='empleado', description='Empleado de la Casa')
    db.auth_group.insert(role='soporte', description='Soporte Técnico')
    db.auth_group.insert(role='directivo', description='Directivo')
    db.auth_group.insert(role='director', description='Director General')
    db.auth_group.insert(role='rector', description='Rector del Colegio')
    db.auth_group.insert(role='secretaria', description='Secretaría')
    db.auth_group.insert(role='secretario', description='Secretario')
    db.auth_group.insert(role='derivaciones', description='Oficina de Derivaciones')
    db.auth_group.insert(role='eoe', description='Equipo de Orientación Escolar')
    db.auth_group.insert(role='administracion', description='Administración')
    db.auth_group.insert(role='administrador', description='Administrador')
    db.auth_group.insert(role='caja', description='Caja')
    db.auth_group.insert(role='padre', description='Padre o Madre')
    db.auth_group.insert(role='candidato', description='Ingresante')
    ## And then the membership on root Group to First User:
    auth.add_membership(1,1)
    ## Later we add permissions:
    auth.add_permission(db.auth_group(role='root').id, 'create', db.auth_user, 0)
    auth.add_permission(db.auth_group(role='root').id, 'read', db.auth_user, 0)
    auth.add_permission(db.auth_group(role='root').id, 'update', db.auth_user, 0)
    auth.add_permission(db.auth_group(role='root').id, 'delete', db.auth_user, 0)

    auth.add_permission(db.auth_group(role="derivaciones").id, 'create new father', db.auth_user, 0)
    auth.add_permission(db.auth_group(role="derivaciones").id, 'view fathers list', db.auth_user, 0)
    return dict(message="SETTED_UP")

def info():
    return locals()

@auth.requires_login()
def start():
    return dict()

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
    ## Deactivating the user group creation on registration
    auth.settings.create_user_groups = None
    ## The line below is commented because is effective on admin/setting_up controller.
    #auth.settings.actions_disabled.append('register')
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

@auth.requires_permission('create new father', db.auth_user)
def new_father():
    form = SQLFORM.factory(db.auth_user.first_name,
                           db.auth_user.middle_name,
                           db.auth_user.last_name,
                           db.auth_user.gender,
                           db.auth_user.email,
                           Field('password', required=True, requires=[IS_MATCH('\d{8}'), CRYPT()], label=T("Document")),
                           db.father,
                           )
    if form.process().accepted:
        new_user_id = db.auth_user.insert(**db.auth_user._filter_fields(form.vars))
        db.auth_membership.insert(user_id=new_user_id,
                                  group_id=db.auth_group(role='padre').id)
        db.father.insert(father_id=new_user_id, **db.father._filter_fields(form.vars))
        db.auth_user[new_user_id]=dict(created_on=request.now)
        response.flash = T("new record inserted")
        redirect(URL('start'))
    elif form.errors:
        response.flash = T("Form has errors")
    return dict(form=form)

def new_personal_data():
    username = auth.user.last_name + ", " + auth.user.first_name + " " + auth.user.middle_name
    form = SQLFORM.factory(db.personal_data.dob,
                           db.personal_data.doc_type,
                           db.personal_data.doc,
                           db.personal_data.nac,
                           db.personal_data.cuil,
                           db.personal_data.mail2,
                           db.personal_data.tel1_type,
                           db.personal_data.tel1,
                           db.personal_data.tel2_type,
                           db.personal_data.tel2,
                           db.address.street,
                           db.address.building,
                           db.address.floor,
                           db.address.door,
                           db.address.apartment,
                           db.address.street1,
                           db.address.street2,
                           db.address.zip_code,
                           db.address.loc,
                           db.address.prov,
                           db.personal_data.obs,
                           db.personal_data.photo,
                           db.personal_data.avatar,
                           db.personal_data.twitter,
                           db.personal_data.facebook,
                          )
    if form.process().accepted:
        data_id = db.personal_data.insert(**db.personal_data._filter_fields(form.vars))
        addr_id = db.address.insert(**db.address._filter_fields(form.vars))
        db.auth_user[auth.user.id]=dict(personal_data_id=data_id, address_id=addr_id)
        response.flash = T("Record inserted")
    return dict(form=form, user=username)

@auth.requires(auth.has_permission('view fathers list', db.auth_user) or auth.has_permission('view users list', db.auth_user))
def fathers_list():
    query = (db.auth_membership.group_id==db.auth_group.id)&(db.auth_membership.user_id==db.auth_user.id)&(db.auth_group.role=='padre')
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
    return dict(grid=grid)

@auth.requires_permission('create', db.date)
def new_date():
    form = SQLFORM(db.date)
    if form.process().accepted:
        #db.date.insert(**db.date._filter_fields(form.vars))
        response.flash = T("Record inserted")
    return dict(form=form)
