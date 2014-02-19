# coding: utf8
@auth.requires_membership('padre')
def index():
    ## Con esta función obtenemos el estado actual del padre para saber a qué página redirigirlo.
    current_state = db.parent(db.parent.uid==auth.user.id).state
    messages = {'Password Change': T("Please change your password."),
                'Parent Data': T("Thanks for updating your password!"),
                'Spouse Data': T("Your personal data has been updated!"),
                'Candidate Data': T("Your spouse's personal data have been recorded."),
                'School Data': T("Your son's personal data have been recorded."),
                'Parent Address Data': T("Your son's school data have been recorded."),
                'Spouse Address Data': T("Your address data have been recorded."),
                'Candidate Address Data': T("Your spouse's address data have been recorded."),
                'Survey': T("Your son's address data have been recorded."),
                'Review Data': T("Thanks for answering the survey!"),
                'Informative Talk': "",
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
    state = parent.state
    ## Si tiene cónyuge obtenemos el registro.
    if parent.spouse:
        spouse = db.parent(db.parent.uid==parent.spouse)
    ## Incrementamos el estado del padre actual.
    parent.state = PARENT_STATE[PARENT_STATE.index(state)+1]
    ## Actualizamos el registro en la DB.
    parent.update_record()
    if parent.spouse and spouse.state == state:
        change_spouse_state(parent.spouse)

def change_spouse_state(uid):
    parent = db.parent(db.parent.uid==uid)
    ## Incrementamos el estado del padre actual.
    parent.state = PARENT_STATE[PARENT_STATE.index(parent.state)+1]
    ## Actualizamos el registro en la DB.
    parent.update_record()

@auth.requires_membership('padre')
def parent_data():
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

    if parent_data.state != PARENT_STATE[1]:
        response.flash = ""

    if form.process().accepted:
        db(db.parent.uid==auth.user.id).update(**db.parent._filter_fields(form.vars))
        db(db.personal_data.uid==auth.user.id).update(**db.personal_data._filter_fields(form.vars))
        if parent_data.spouse:
            change_spouse_state(auth.user.id)
            change_spouse_state(auth.user.id)
        else:
            change_parent_state(auth.user.id)
        auth.log_event(description="Parent %s updated data" % (fullname(auth.user.id)))
        if parent_data.spouse:
            db(db.parent.id==auth.user.id).update(state=db.parent(uid=parent_data.spouse).state)
        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def spouse_data():
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

    if db.parent(db.parent.uid==auth.user.id).state != PARENT_STATE[2]:
        response.flash = ""

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
                         children_course=parent.children_course,
                         children_registration_year=parent.children_registration_year,
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
        auth.log_event(description="%s - created new parent: %s" % (fullname(auth.user.id), fullname(new_parent_id)))
        change_parent_state(auth.user.id)
        if not form.vars.enabled:
            db(db.auth_user.id==new_parent_id).update(registration_key="disabled")
            auth.log_event(description="%s - disabled parent: %s" % (fullname(auth.user.id), fullname(new_parent_id)))
        else:
            send_welcome_mail(form, new_parent_id)
            db(db.parent.uid==new_parent_id).update(state=PARENT_STATE[0])
        redirect(URL('index'))
    return locals()

def skip_parent_data_2():
    change_parent_state(auth.user.id)
    auth.log_event(description="Parent %s skipped spouse data" % (fullname(auth.user.id)))
    redirect(URL('index'))

@auth.requires_membership('padre')
def candidate_data():
    form = SQLFORM.factory(db.auth_user.first_name,
                           db.auth_user.middle_name,
                           db.auth_user.last_name,
                           Field('has_email', 'boolean', default=False, label=T("Has email?"), comment=T("If you want your children gets notified, check this and fill below with a valid email address")),
                           Field('email', 'string', length=128, requires=IS_EMPTY_OR(IS_EMAIL()), label=T("Email")),
                           #db.auth_user.email,
                           db.personal_data.doc_type,
                           db.personal_data.doc,
                           db.personal_data.nac,
                           db.personal_data.cuil,
                           db.personal_data.dob,
                           db.personal_data.photo,
                           db.personal_data.avatar,
                           db.personal_data.twitter,
                           db.personal_data.facebook,
                           db.personal_data.obs,
                           db.candidate.course,
                           db.candidate.key,
                           submit_button=T("Insert Data")
                           )

    if form.process().accepted:
        if not form.vars.has_email:
            form.vars.email = 'parent_'+str(auth.user.id)+'@nomail.com'
        new_user_id = db.auth_user.insert(password=str(CRYPT()(form.vars.doc)[0]),
                                            **db.auth_user._filter_fields(form.vars))
        db.personal_data.insert(uid=new_user_id,
                                **db.personal_data._filter_fields(form.vars)
                                )
        db.candidate.insert(uid=new_user_id,
                            cod=computeMD5(simple_fullname(new_user_id)),
                            **db.candidate._filter_fields(form.vars)
                            )
        db.auth_membership.insert(user_id=new_user_id,
                                  group_id=db.auth_group(role='candidato').id)
        parent = db.parent(uid=auth.user.id)
        parent.student_id=new_user_id
        parent.update_record()
        if parent.spouse:
            spouse = db.parent(spouse=auth.user.id)
            spouse.student_id=new_user_id
            spouse.update_record()
        auth.log_event(description="%s - created new candidate: %s" % (fullname(auth.user.id), fullname(new_user_id)))
        if not form.vars.has_email:
            db(db.auth_user.id==new_user_id).update(registration_key="disabled")
            auth.log_event(description="%s - disabled candidate: %s" % (fullname(auth.user.id), fullname(new_user_id)))
        else:
            send_welcome_mail(form, new_user_id)
        change_parent_state(auth.user.id)
        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def school_data():
    query = (auth.user.id == db.parent.uid) & (db.parent.student_id == db.candidate.uid) & (db.auth_user.id == db.candidate.uid)
    form = SQLFORM.factory(Field('school_id', 'string', length=50, requires=IS_EMPTY_OR(IS_IN_DB(db, 'school.id', '(%(number)s) %(name)s', zero=T("Select one from list or \"Add new school\""))), label=T("School Name")),
                           Field('candidate_id', requires=IS_IN_DB(db(query), 'auth_user.id', '%(first_name)s %(middle_name)s %(last_name)s', zero=None), label=T("Sun/Daughter")),
                           submit_button=T("Insert Data")
                                    )
    form.add_button('Add new school', URL('add_new_school'))
    if form.process().accepted:
        school = db.school(db.school.id == form.vars.school_id)
        candidate = db.candidate(db.candidate.uid == form.vars.candidate_id)
        candidate.school = school.id
        candidate.update_record()
        change_parent_state(auth.user.id)
        auth.log_event(description="%s - link candidate %s with school %s" % (fullname(auth.user.id), fullname(candidate.uid), school.number))
        redirect(URL(index))
    return locals()

@auth.requires_membership('padre')
def add_new_school():
    form = SQLFORM.factory(db.school.name,
                           db.school.number,
                           db.school.district,
                           db.address.street,
                           db.address.building,
                           db.address.loc,
                           db.address.prov,
                           submit_button=T("Insert Data")
                          )
    if form.process().accepted:
        new_address_id = db.address.insert(**db.address._filter_fields(form.vars))
        new_school_id = db.school.insert(address_id=new_address_id,
                                         **db.school._filter_fields(form.vars)
                                         )
        auth.log_event(description="%s - created new school: %s" % (fullname(auth.user.id), form.vars.name+"("+form.vars.number+")"))
        redirect(URL(school_data))
    return locals()

@auth.requires_membership('padre')
def parent_address_data():
    form = SQLFORM(db.address,
                   submit_button=T("Insert Data"))
    if form.process().accepted:
        new_address_id = form.vars.id
        db(db.personal_data.uid==auth.user.id).update(address_id=new_address_id)
        change_parent_state(auth.user.id)
        auth.log_event(description="%s - stored own address (%s)" % (fullname(auth.user.id), new_address_id))
        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def spouse_address_data():
    form = SQLFORM(db.address,
                   submit_button=T("Insert Data")
                   )
    form.add_button(T("My spouse lives with me"), URL('spouses_lives_together'))

    if auth.user.gender == GENDER_LIST[1][0]:
        form.add_button(T("Skip Father Address"), URL('skip_spouse_address'))
    else:
        form.add_button(T("Skip Mother Address"), URL('skip_spouse_address'))

    if form.process().accepted:
        new_address_id = form.vars.id
        parent = db.parent(db.parent.uid==auth.user.id)
        db((db.personal_data.uid==parent.spouse)).update(address_id=new_address_id)
        change_parent_state(auth.user.id)
        auth.log_event(description="%s - stored spouse address (%s)" % (fullname(auth.user.id), new_address_id))
        redirect(URL('index'))
    return locals()

def spouses_lives_together():
    address_id = db.personal_data(db.personal_data.uid==auth.user.id).address_id
    spouse_id = db.parent(db.parent.uid==auth.user.id).spouse
    db(db.personal_data.uid==spouse_id).update(address_id=address_id)
    change_parent_state(auth.user.id)
    auth.log_event(description="%s - lives with spouse" % (fullname(auth.user.id)))
    redirect(URL('index'))

def skip_spouse_address():
    change_parent_state(auth.user.id)
    auth.log_event(description="%s - skip spouse address" % (fullname(auth.user.id)))
    redirect(URL('index'))

@auth.requires_membership('padre')
def candidate_address_data():
    parent = db((db.auth_user.id==auth.user.id)&(db.personal_data.uid==db.auth_user.id)&(db.parent.uid==db.auth_user.id)).select().first()
    candidate = db((db.auth_user.id==parent.parent.student_id)&(db.personal_data.uid==db.auth_user.id)).select().first()
    spouse = None
    LIVES_WITH = ((parent.auth_user.id, simple_fullname(parent.auth_user.id)),
                  ("0", T("Doesn't live with parents")))
    if parent.parent.spouse:
        spouse = db((db.auth_user.id==parent.parent.spouse)&(db.personal_data.uid==db.auth_user.id)&(db.parent.uid==db.auth_user.id)).select().first()
        LIVES_WITH = ((parent.auth_user.id, simple_fullname(parent.auth_user.id)),
                      (spouse.auth_user.id, simple_fullname(spouse.auth_user.id)),
                      ("0", T("Doesn't live with parents")))

    form = SQLFORM.factory(Field("lives_with", requires=IS_IN_SET(LIVES_WITH, zero=None)),
                           db.address,
                           submit_button=T("Insert Data")
                           )
    if form.process().accepted:
        addr_id = None
        if form.vars.lives_with == str(parent.auth_user.id):
            #db(db.personal_data.uid==candidate.auth_user.id).update(address_id=parent.personal_data.id)
            candidate.personal_data.address_id=parent.personal_data.address_id
            candidate.personal_data.update_record()
            addr_id = parent.personal_data.address_id
        elif spouse and form.vars.lives_with == str(spouse.auth_user.id):
            #db(db.personal_data.uid==candidate.auth_user.id).update(address_id=spouse.personal_data.id)
            candidate.personal_data.address_id=spouse.personal_data.address_id
            candidate.personal_data.update_record()
            addr_id = spouse.personal_data.address_id
        elif form.vars.lives_with == "0":
            new_address_id = db.address.insert(**db.address._filter_fields(form.vars))
            db(db.personal_data.uid==candidate.auth_user.id).update(address_id=new_address_id)
            addr_id = new_address_id
        change_parent_state(auth.user.id)
        auth.log_event(description="%s - candidate %s in address (%s)" % (simple_fullname(auth.user.id), simple_fullname(candidate.auth_user.id), addr_id))
        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def survey():
    form = "ENCUESTA"
    age = db(db.personal_data.uid==auth.user.id).select().first().age
    return locals()
