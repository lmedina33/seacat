# coding: utf-8
@auth.requires_membership('derivaciones')
def index():
    return dict()

def user():
    redirect(URL('default','index'))

@auth.requires_permission('create new father', db.auth_user)
def new_parent():
    form = SQLFORM.factory(db.auth_user.first_name,
                           db.auth_user.middle_name,
                           db.auth_user.last_name,
                           db.auth_user.gender,
                           db.auth_user.email,
                           Field('send_mail', 'boolean', default=True, label=T("Send email?")),
                           db.personal_data.doc,
                           db.parent.children_in_school,
                           db.parent.children_name,
                           db.parent.children_registration_year,
                           db.parent.children_course,
                           db.parent.student_network,
                           db.parent.student_school,
                           Field('date', requires=IS_IN_DB(db((db.date.type=="informative talk")
                                                              #&(db.date.max_participants>db.date.participants) ## No me deja comparar con el Virtual Field
                                                              ), 'date.id', '%(date)s @ %(start_time)s | %(participants)s / %(max_participants)s'), label=T("Informative Talk")),
                           submit_button=T("Create New Parent")
                           )
    def __validate_booking(form):
        date = db(db.date.id==form.vars.date).select().first()
        if date.participants == date.max_participants:
            form.errors.date= T("This date is full, please choose another one")
    if form.process(onvalidation=__validate_booking).accepted:
        new_user_id = db.auth_user.insert(password=str(CRYPT()(form.vars.doc)[0]),
                                          **db.auth_user._filter_fields(form.vars))
        db.auth_membership.insert(user_id=new_user_id,
                                  group_id=db.auth_group(role='padre').id)
        db.parent.insert(uid=new_user_id,
                         is_alive=True,
                         state=PARENT_STATE[0],
                         **db.parent._filter_fields(form.vars)
                         )
        db.personal_data.insert(uid=new_user_id,
                                doc=form.vars.doc
                                )
        db.auth_user[new_user_id]=dict(created_on=request.now)
        auth.log_event(description="New Parent Created: %s" % (fullname(new_user_id)))
        db.turn.insert(uid=new_user_id,
                       date=form.vars.date)
        auth.log_event(description="%s - choose informative talk on %s at %s" % (simple_fullname(new_user_id),
                                                                                 db(db.date.id==form.vars.date).select().first().date,
                                                                                 db(db.date.id==form.vars.date).select().first().start_time))
        message = T("New record inserted")
        if form.vars.send_mail:
            send_welcome_mail(form, new_user_id)
            message += " & "+T("Email sent")
        session.flash = message
        redirect(URL('index'))
    elif form.errors:
        response.flash = T("Form has errors")
    return locals()

@auth.requires(auth.has_permission('view fathers list', db.auth_user) or auth.has_permission('view users list', db.auth_user))
def parents_list():
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
    return locals()
