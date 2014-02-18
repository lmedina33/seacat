# coding: utf8
@auth.requires_membership('padre')
def index():
    ## Con esta función obtenemos el estado actual del padre para saber a qué página redirigirlo.
    current_state = db.parent(db.parent.uid==auth.user.id).state
    messages = {'Password Change': T("Please change your password."),
                'Parent Data 1': T("Thanks for updating your password!"),
                'Parent Data 2': T("Your personal data has been updated!"),
                'Student Data': T("Your spouse's personal data have been recorded."),
                'School Data': T("Your son's personal data have been recorded."),
                'Survey': T("Your son's school data have been recorded."),
                'Informative Talk': T("Thanks for answering the survey!"),
                'Terms and Conditions':"",
                'Exam Payment':"",
                'First Parent Meeting':"",
                'Priority Test':"",
                'Calification Test':"",
                'Grades Review':"",
                'Test':"",
                'Final Registration':"",
                'Second Parent Meeting':"",
                'Vacancy':"",
                'Admitted':"",
                'Rejected':"" }
    session.flash = messages[current_state]
    redirect(URL(current_state.lower().replace(' ','_')))
    return locals()

def user():
    redirect(URL('default','index'))

@auth.requires_membership('padre')
def password_change():
    ## Automatic Log on event table because auth.change_password form is used.
    form = auth.change_password(onvalidation=validate_password, next=URL('index'))
    return locals()

def validate_password(form):
    if form.vars.new_password == form.vars.old_password:
        form.errors.new_password = T("You must use a password different than the old one!")
    change_parent_state(auth.user.id)

def change_parent_state(uid):
    ## Obtenemos el registro del padre actual.
    parent = db.parent(db.parent.uid==uid)
    ## Incrementamos el estado del padre actual.
    parent.state = PARENT_STATE[PARENT_STATE.index(parent.state)+1]
    ## Actualizamos el registro en la DB.
    parent.update_record()
    if parent.spouse:
        change_spouse_state(parent.spouse)

def change_spouse_state(uid):
    parent = db.parent(db.parent.uid==uid)
    ## Incrementamos el estado del padre actual.
    parent.state = PARENT_STATE[PARENT_STATE.index(parent.state)+1]
    ## Actualizamos el registro en la DB.
    parent.update_record()

@auth.requires_membership('padre')
def parent_data_1():
    name = simple_fullname(auth.user.id)
    form = SQLFORM.factory(db.parent.work,
                           db.parent.works_in,
                           db.personal_data,
                           submit_button=T("Update Data")
                           )
    personal_data = db.personal_data(db.personal_data.uid==auth.user.id)
    parent_data = db.parent(db.parent.uid==auth.user.id)

    for field in db.personal_data.fields:
        form.vars[field] = personal_data[field]
        if isinstance(personal_data[field], datetime.date):
            form.vars[field] = personal_data[field].strftime(DATE_FORMAT)

    form.vars.work = parent_data.work
    form.vars.works_in = parent_data.works_in

    if form.process().accepted:
        db(db.parent.uid==auth.user.id).update(**db.parent._filter_fields(form.vars))
        db(db.personal_data.uid==auth.user.id).update(**db.personal_data._filter_fields(form.vars))
        change_parent_state(auth.user.id)
        auth.log_event(description="Parent %s updated data" % (fullname(auth.user.id)))
        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def parent_data_2():
    form = SQLFORM.factory(db.auth_user.first_name,
                           db.auth_user.middle_name,
                           db.auth_user.last_name,
                           db.auth_user.gender,
                           db.parent.is_alive,
                           db.personal_data.doc_type,
                           db.personal_data.doc,
                           db.personal_data.nac,
                           db.personal_data.cuil,
                           db.personal_data.dob,
                           db.auth_user.email,
                           db.personal_data.mail2,
                           db.personal_data.tel1_type,
                           db.personal_data.tel1,
                           db.personal_data.tel2_type,
                           db.personal_data.tel2,
                           db.parent.work,
                           db.parent.works_in,
                           db.personal_data.photo,
                           db.personal_data.avatar,
                           db.personal_data.twitter,
                           db.personal_data.facebook,
                           db.personal_data.obs,
                           Field("enabled", 'boolean', default=True, label=T("Enable User?"), comment=T("If you enable the user he will be capable of using the system and make modifications like you do. He will be notified by email. Any modifications made in registration process (by him or you) will be notified by email to both of us.")),
                           submit_button=T("Insert Data")
                           )

    if auth.user.gender == GENDER_LIST[1][0]:
        form.vars.gender = GENDER_LIST[0][0]
        form.add_button(T("Skip Father"), URL('skip_parent_data_2'))
    else:
        form.vars.gender = GENDER_LIST[1][0]
        form.add_button(T("Skip Mother"), URL('skip_parent_data_2'))


    if form.process().accepted:
        parent = db.parent(db.parent.uid==auth.user.id)
        new_parent_id = db.auth_user.insert(password=str(CRYPT()(form.vars.doc)[0]),
                                            **db.auth_user._filter_fields(form.vars))
        db.personal_data.insert(uid=new_parent_id,
                                **db.personal_data._filter_fields(form.vars)
                                )
        db.parent.insert(uid=new_parent_id,
                         children_in_school=parent.children_in_school,
                         children_name=parent.children_name,
                         student_network=parent.student_network,
                         student_school=parent.student_school,
                         spouse=auth.user.id,
                         state=parent.state,
                         created_on=request.now,
                         **db.parent._filter_fields(form.vars)
                         )
        db.auth_membership.insert(user_id=new_parent_id,
                          group_id=db.auth_group(role='padre').id)
        parent.spouse = new_parent_id
        parent.update_record()
        auth.log_event(description="%s - created new user: %s" % (fullname(auth.user.id), fullname(new_parent_id)))
        if not form.vars.enabled:
            db(db.auth_user.id==new_parent_id).update(registration_key="disabled")
            auth.log_event(description="%s - disabled user: %s" % (fullname(auth.user.id), fullname(new_parent_id)))
        else:
            send_welcome_mail(form, new_parent_id)
        change_parent_state(auth.user.id)
        redirect(URL('index'))
    return locals()

def skip_parent_data_2():
    change_parent_state(auth.user.id)
    auth.log_event(description="Parent %s skipped spouse data" % (fullname(auth.user.id)))
    redirect(URL('index'))

@auth.requires_membership('padre')
def student_data():
    age = db.personal_data(uid=auth.user.id).dob
    return locals()
