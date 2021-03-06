#-*- coding: utf-8 -*-

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
        if auth.has_membership('padre'):
            redirect(URL('parent', 'index'))
        elif auth.has_membership('derivaciones'):
            redirect(URL('reception', 'index'))
        elif auth.has_membership('secretaria'):
            redirect(URL('secretary', 'index'))
        else:
        #usernameid = {'uid': auth.user.id, 'first_name': auth.user.first_name, 'last_name': auth.user.last_name}
        #auth.log_event(description=T("User %(uid)s - %(last_name)s, %(first_name)s - logged in" % usernameid))
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
    logo = db.image(name="Logo Pío IX Nuevo 250x245").file
    closing_date = db.general_date(type=GENERAL_DATE_TYPE[1]).date
    openning_date = db.general_date(type=GENERAL_DATE_TYPE[0]).date
    return dict(logo=logo, closing_date=closing_date, openning_date=openning_date)

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
def new_turn():
    form = SQLFORM(db.date)
    if form.process().accepted:
        #db.date.insert(**db.date._filter_fields(form.vars))
        response.flash = T("Record inserted")
    return dict(form=form)

def validate_gral_dates(form):
    #####################################################
    ## Hay que completar con el resto de los validadores
    #####################################################
    #for date_type in GENERAL_DATE_TYPE:
    if int(form.vars.selected_year) != form.vars[str(GENERAL_DATE_TYPE[0]).replace(' ','_')+'_date'].year:
        form.errors[str(GENERAL_DATE_TYPE[0]).replace(' ','_')+'_date'] = T("The date must equals the year selected")

@auth.requires_permission('create', db.date)
def new_general_dates():
    ## Falta hacer andar el script de la vista, para recargar el formulario con el cambio del año. -- Listo, gracias a Julio César Albornoz <juliocesaralbornoz@gmail.com>
    ## Sino convertimos el formulario a la propuesta de Julio, un primer formulario de búsqueda y
    ## un segundo formulario de modificación.

    #########################################################################################################
    ## Faltaría hacer la validación de la entrada de datos, con jQuery? o armo un validador?
    ## ---  Listo, se valida con la función validate_gral_dates()
    ## Estaría bueno ocultar el campo "selected_year" y trabajar con el valor elegido sin poder modificarlo
    ##    (No se puede agregar el atributo/argumento "hidden" y ahí definimos que selected_year es hidden
    ##     o de alguna manera seleccionar form.element y poner selected_year como tipo hidden).
    ## Preguntarle a Mariano cómo es que funciona el tema de las variables enviadas/aceptadas!!!!!
    ## Falta hacer el auht.log_event!!!!
    #########################################################################################################

    find_form = SQLFORM.factory(db.general_date.year)
    if request.vars != None:
        find_form.vars.year = request.vars.year
    ## Oculta el botón submit
    submit = find_form.element('input',_type='submit')
    submit['_style'] = 'display:none;'
    find_form.attributes['_id'] = 'find_form'
    find_form.element('select').attributes['_id'] = 'filter'

#    if find_form.process(formname='find_form').accepted:
#        response.flash = ""
#        year = find_form.vars.year

    ## Crea el formulario para insertar o modificar los datos
    form = SQLFORM.factory(Field('selected_year', label=T("Selected Year")))
    form.vars.selected_year = request.vars.year

    for date_type in GENERAL_DATE_TYPE:
        fila = TR(LABEL(B(T(date_type))))
        fila += TR(LABEL(T("Date")+":"), INPUT(_name=date_type.replace(' ','_')+'_date', _class="date", requires=IS_EMPTY_OR(IS_DATE(DATE_FORMAT))), _id=date_type.replace(' ','_')+"_date__row")
        fila += TR(LABEL(T("Start Time")+":"), INPUT(_name=date_type.replace(' ','_')+'_start_time', _class="time", requires=IS_EMPTY_OR(IS_TIME())), _id=date_type.replace(' ','_')+"_start_time__row")
        fila += TR(LABEL(T("End Time")+":"), INPUT(_name=date_type.replace(' ','_')+'_end_time', _class="time", requires=IS_EMPTY_OR(IS_TIME())), _id=date_type.replace(' ','_')+"_end_time__row")
        form[0].insert(-1, fila)

    data = db(db.general_date.year==find_form.vars.year).select(
                                                 db.general_date.type,
                                                 db.general_date.date,
                                                 db.general_date.start_time,
                                                 db.general_date.end_time
                                                 )
    for row in data:
        fieldtype = row.type
        fieldtype = fieldtype.replace(' ', '_')
        form.vars[fieldtype+'_date'] = row.date.strftime(DATE_FORMAT)
        #if not row.start_time:
        form.vars[fieldtype+'_start_time'] = row.start_time
        #if not row.end_time:
        form.vars[fieldtype+'_end_time'] = row.end_time

    if form.process(formname='form', onvalidation=validate_gral_dates).accepted:
        for field, value in form.vars.items():
            fieldtype = ""
            date = ""
            start_time = ""
            end_time = ""
            if not value:
                continue
            elif "_date" in field:
                fieldname = field.split("_date")
                fieldtype = fieldname[0].replace('_', ' ')
                date = value
                start_time = form.vars[fieldname[0]+"_start_time"]
                end_time = form.vars[fieldname[0]+"_end_time"]
            elif "_start_time" in field:
                continue
            elif "_end_time" in field:
                continue
            elif "year" in field:
                continue
            else:
                pass
            db.general_date.update_or_insert((db.general_date.type==fieldtype)&(db.general_date.year==form.vars.selected_year),
                                             type=fieldtype,
                                             year=form.vars.selected_year,
                                             date=date,
                                             start_time=start_time,
                                             end_time=end_time)
        response.flash = T("New set of records inserted for year %s" % form.vars.selected_year)
    return dict(find_form=find_form, form=form)

def help():
    return locals()
