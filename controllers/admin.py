# coding: utf8
# intente algo como
def index(): return dict(message="hello from admin.py")

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

@auth.requires_permission('create new user', db.auth_user)
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
        redirect(URL('start'))
    elif form.errors:
        response.flash = T("Form has errors")
    return dict(form=form)

@auth.requires_membership('root')
def upload_image():
    grid = SQLFORM.smartgrid(db.images)
    return locals()

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
