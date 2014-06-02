# coding: utf-8
def index():
    redirect(URL('default', 'index'))

@auth.requires_membership('root')
def admin_users():
    grid = SQLFORM.smartgrid(db.auth_user,
                             fields=[db.auth_user.id,
                                     db.auth_user.gender,
                                     db.auth_user.first_name,
                                     db.auth_user.middle_name,
                                     db.auth_user.last_name,
                                     db.auth_user.email,
                                     db.auth_user.obs,
                                     db.auth_user.last_login,
                                     db.auth_user.created_on],
                             maxtextlengths={'auth_user.email': 50},
                             showbuttontext=False,
                             orderby='auth_user.last_name',
                             paginate=50,
                             links_in_grid=False,
                             exportclasses=dict(csv=True, csv_with_hidden_cols=False, json=False, tsv=False, tsv_with_hidden_cols=False, xml=True)
                             )
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

@auth.requires_permission('create', db.auth_user)
def new_user():
    form = SQLFORM.factory(db.auth_user.first_name,
                           db.auth_user.middle_name,
                           db.auth_user.last_name,
                           db.auth_user.gender,
                           db.auth_user.email,
                           db.auth_user.password,
                           Field('password_check', required=True, requires=[IS_EQUAL_TO(request.vars.password)], widget=SQLFORM.widgets.password.widget, label=T("Password Verification")),
                           Field('role', required=True, requires=IS_IN_DB(db, 'auth_group.role', '%(description)s'), notnull=True, label=T("Role")),
                           db.auth_user.obs
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
        redirect(URL('default','start'))
    elif form.errors:
        response.flash = T("Form has errors")
    return dict(form=form)

@auth.requires_membership('root')
def upload_image():
    grid = SQLFORM.smartgrid(db.image)
    return locals()

@auth.requires_permission('read', db.auth_user)
def users_list():
    form = SQLFORM.factory(Field('role', requires=IS_EMPTY_OR(IS_IN_DB(db, 'auth_group.role', '%(description)s', zero=T("All"))),
                                 label=T("Filter")),
                           submit_button=T("Find"))
    query =  (db.auth_membership.group_id==db.auth_group.id)&(db.auth_membership.user_id==db.auth_user.id)
    if form.process().accepted:
        if form.vars.role != None:
            query &= (db.auth_group.role==request.vars.role)
        response.flash = ""
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

@auth.requires_permission('read', db.turn)
def dates_list():
    form = SQLFORM.factory(Field('type', requires=IS_EMPTY_OR(IS_IN_DB(db, 'date.type', zero=T("All"), distinct=True)), label=T("Filter")), submit_button=T("Find"))

    query = db.date

    if form.process().accepted:
        if form.vars.type != None:
            query = db.date.type==request.vars.type
            response.flash = T("Showing data for %s", request.vars.type)
        else:
            response.flash = T("Showing data for all dates")

    grid = SQLFORM.grid(query,
                        create=False,
                        deletable=False,
                        details=False,
                        editable=False,
                        searchable=False,
                        csv=False,
                        paginate=50
                        )

    return dict(form=form, grid=grid)

@auth.requires_permission('read', db.date)
def general_dates_list():
    form = SQLFORM.factory(Field('year', requires=IS_EMPTY_OR(IS_IN_DB(db, 'general_date.year', zero=T("All"), distinct=True)), label=T("Filter")), submit_button=T("Find"))

    query = db.general_date

    if form.process().accepted:
        if form.vars.year != None:
            query = db.general_date.year==request.vars.year
            response.flash = T("Showing data for year %s", request.vars.year)
        else:
            response.flash = T("Showing data for all years")

    grid = SQLFORM.grid(query,
                             #fields=[db.general_date.id,
                             #        db.general_date.type],
                             maxtextlengths={'general_date.type': 50},
                             showbuttontext=False,
                             orderby=db.general_date.type,
                             #groupby=db.general_date.year, ## Cuando le pongo el groupby me tira error y no sé por qué.
                             paginate=50,
                             links_in_grid=False,
                             create=False,
                             deletable=False,
                             details=False,
                             editable=False,
                             searchable=False,
                             csv=False,
                             )
    return dict(form=form, grid=grid)

@auth.requires_permission('read', db.turn)
def turns_list():
    form = SQLFORM.factory(Field('turn', requires=IS_IN_DB(db((db.date.type=="informative talk")),
                                                           'date.id', '%(date)s @ %(start_time)s | %(participants)s / %(max_participants)s'),
                                 label=T("Turn Filter")),
                           submit_button=T("Find"))
    query = (db.turn.date==db.date.id)&(db.auth_user.id==db.turn.uid)
    turn = ""
    if form.process().accepted:
        if form.vars.turn != None:
            query &= (db.turn.date==request.vars.turn)
            turn = db(db.date.id==request.vars.turn).select().first()
            turn = turn.date.strftime(DATE_FORMAT)+" @ "+turn.start_time.strftime(TIME_FORMAT)
        response.flash = ""
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
    return dict(form=form, grid=grid, turn=turn)
