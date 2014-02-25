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
    survey = db(db.survey.is_active==True).select().first()
    sas = db((db.sa.survey==survey.id)&(db.sa.uid==auth.user.id)).select().first()
    if sas:
        if sas.completed:
                change_parent_state(auth.user.id)
                auth.log_event(description="%s - completed parent survey" % (fullname(auth.user.id)))
                redirect(URL('index'))
        else:
            redirect(URL(c='survey', f='take', args=survey.code_take, vars={'caller':request.url}))
    else:
        redirect(URL(c='survey', f='take', args=survey.code_take, vars={'caller':request.url}))

@auth.requires_membership('padre')
def review_data():
    ###################################################
    ####### FALTA VERIFICAR SI HAY O NO SPOUSE!!!!! Y construir los formulario de modificacion y volver a esto.
    ####### Procesar datos casndidate!!!!!
    ###################################################

    ## Obtenemos el regitro del padre que está conectado
    parent = db((db.auth_user.id==auth.user.id)&
                (db.parent.uid==db.auth_user.id)&
                (db.personal_data.uid==db.auth_user.id)&
                (db.address.id==db.personal_data.address_id)).select().first()
    ## Obtenemos el regitro del cónyuge del padre que está conectado
    spouse = db((db.auth_user.id==parent.parent.spouse)&
                (db.parent.uid==parent.parent.spouse)&
                (db.personal_data.uid==parent.parent.spouse)&
                (db.address.id==db.personal_data.address_id)).select().first()
    ## Obtenemos el regitro del hijo del padre que está conectado
    candidate = db((db.auth_user.id==parent.parent.student_id)&
                (db.candidate.uid==parent.parent.student_id)&
                (db.personal_data.uid==parent.parent.student_id)&
                (db.address.id==db.personal_data.address_id)&
                (db.school.id==db.candidate.school)).select().first()

    ## Armamos una lista con los campos comunes, los que vamos a mostrar en la primer tabla. El orden importa!
    common_fields = [db.personal_data.photo, db.auth_user.gender,
                     db.auth_user.last_name, db.auth_user.first_name, db.auth_user.middle_name,
                     db.auth_user.email, db.personal_data.mail2,
                     db.personal_data.doc_type, db.personal_data.doc, db.personal_data.nac,
                     db.personal_data.cuil, db.personal_data.dob, #db.personal_data.age,
                     db.personal_data.tel1_type, db.personal_data.tel1,
                     db.personal_data.tel2_type, db.personal_data.tel2,
                     db.address.street, db.address.building, db.address.floor, db.address.apartment,
                     db.address.door, db.address.street1, db.address.street2, db.address.prov, db.address.zip_code,
                     db.personal_data.facebook, db.personal_data.twitter]
    ## Construimos la tabla Común
    grid = TABLE(COLGROUP(
                          COL(_span="1", _style='web2py_grid')
                          ),
                 THEAD(
                       TR(
                           TH(),
                           TH(T("Parent")),
                           TH(T("Spouse")),
                           TH(T("Candidate")),
                         )
                       ),
                 TBODY(),
                 _class='web2py_grid')

    ## Función para presentar los valores en la tabla
    def __format_data(parent):
        for table in parent:
            for field in parent[table]:
                if parent[table][field] == None:
                    parent[table][field] = ""
                if field == 'gender':
                    if parent[table][field] == 'M':
                        parent[table][field] = T("Male")
                    else:
                        parent[table][field] = T("Female")
                if field == 'email' and 'nomail.com' in parent[table][field]:
                    parent[table][field] = ""
                if isinstance(parent[table][field], datetime.date):
                    parent[table][field] = parent[table][field].strftime(DATE_FORMAT)
                if field == 'cuil':
                    parent[table][field] = parent[table][field][:2]+"-"+parent[table][field][2:-1]+"-"+parent[table][field][-1]
                if field == 'tel1':
                    parent[table][field] = parent[table][field][:-4]+"-"+parent[table][field][4:]
                if field == 'tel2' and parent[table][field] != None:
                    parent[table][field] = parent[table][field][:-4]+"-"+parent[table][field][4:]
                if field == 'doc':
                    parent[table][field] = parent[table][field][:-6]+"."+parent[table][field][-6:-3]+"."+parent[table][field][-3:]
                if field == 'tel1_type' or field == 'tel2_type':
                    for type_tel in TEL_TYPE_SET:
                        if type_tel[0] == parent[table][field]:
                            parent[table][field] = type_tel[1]
                            break
                if field == 'course':
                    for course in COURSE:
                        if course[0] == parent[table][field]:
                            parent[table][field] = course[1]
                            break

    ##  Formateamos los valores de los registros en valores "presentables"
    __format_data(parent)
    __format_data(spouse)
    __format_data(candidate)

    ## Agregamos las filas con los datos que armamos en la lista de campos: common_fields.
    for i,item in enumerate(common_fields):
        if is_odd(i):
            row_class = "odd"
        else:
            row_class = "even"
        grid[2].append(TR(
                          TH(item.label),
                          TD(parent[item]),
                          TD(spouse[item]),
                          TD(candidate[item]),
                          _class=row_class)
                       )
    ## Agregamos los botones de edición en el Table Footer
    grid.append(TFOOT(
                      TR(
                         TD(),
                         TD(TAG.A(T("Edit"), _id="parent", _class="btn", _href=URL('modify', args=['parent']))),
                         TD(TAG.A(T("Edit"), _id="spouse", _class="btn", _href=URL('modify', args=['spouse']))),
                         TD(TAG.A(T("Edit"), _id="candidate", _class="btn", _href=URL('modify', args=['candidate']))),
                        )
                     )
                )

    ## Armamos una lista con los campos exclusivos de los padres. El orden importa!
    parent_fields = [db.parent.work, db.parent.works_in]
    ## Construimos la tabla de Padres
    parent_grid = TABLE(COLGROUP(
                                 COL(_span="1", _style='web2py_grid')
                                ),
                        THEAD(
                              TR(
                                 TH(),
                                 TH(T("Parent")),
                                 TH(T("Spouse"))
                                )
                             ),
                        TBODY(),
                        _class='web2py_grid')
    ## Agregamos las filas con los datos que armamos en la lista de campos: parent_fields.
    for i,item in enumerate(parent_fields):
        if is_odd(i):
            row_class = "odd"
        else:
            row_class = "even"
        parent_grid[2].append(TR(
                                 TH(item.label),
                                 TD(parent[item]),
                                 TD(spouse[item]),
                                 _class=row_class)
                             )
    ## Agregamos los botones de edición en el Table Footer
    parent_grid.append(TFOOT(
                             TR(
                                TD(),
                                TD(TAG.A(T("Edit"), _id="parent_work", _class="btn", _href=URL('modify', args=['parent_work']))),
                                TD(TAG.A(T("Edit"), _id="spouse_work", _class="btn", _href=URL('modify', args=['spouse_work']))),
                               )
                            )
                       )

    ## Acomodamos los títulos de las columnas acorde al sexo del usuario que está conectado:
    if auth.user.gender == 'M':
        grid[1][0][1] = TH(T("Father"))
        parent_grid[1][0][1] = TH(T("Father")+": "+simple_fullname(parent.auth_user.id))
        grid[1][0][2] = TH(T("Mother"))
        parent_grid[1][0][2] = TH(T("Mother")+": "+simple_fullname(spouse.auth_user.id))
    else:
        grid[1][0][1] = TH(T("Mother"))
        parent_grid[1][0][1] = TH(T("Mother")+": "+simple_fullname(parent.auth_user.id))
        grid[1][0][2] = TH(T("Father"))
        parent_grid[1][0][2] = TH(T("Father")+": "+simple_fullname(spouse.auth_user.id))

    ## Armamos una lista con los campos exclusivos de los padres. El orden importa!
    candidate_fields = [db.candidate.course,
                        db.school.name, db.school.number, db.school.district,
                        db.address.street, db.address.building, db.address.floor, db.address.apartment,
                        db.address.door, db.address.street1, db.address.street2, db.address.prov, db.address.zip_code]
    ## Construimos la tabla de la escuela del Candidato
    candidate_grid = TABLE(COLGROUP(
                                    COL(_span="1", _style='web2py_grid')
                                    ),
                           THEAD(
                                 TR(
                                    TH(),
                                    TH(T("Candidate")),
                                   )
                                ),
                           TBODY(),
                           _class='web2py_grid')
    ## Agregamos las filas con los datos que armamos en la lista de campos: candidate_fields.
    for i,item in enumerate(candidate_fields):
        if is_odd(i):
            row_class = "odd"
        else:
            row_class = "even"
        candidate_grid[2].append(TR(
                                    TH(item.label),
                                    TD(candidate[item]),
                                    _class=row_class
                                   )
                                )
    ## Agregamos los botones de edición en el Table Footer
    candidate_grid.append(TFOOT(
                                TR(
                                   TD(),
                                   TD(TAG.A(T("Edit"), _id="edit_candidate_school", _class="btn", _href=URL('modify', args=['candidate_school']))),
                                  )
                               )
                         )
    ## Acomodamos los títulos de las columnas acorde al sexo del candidato:
    if db.auth_user(id=candidate.auth_user.id).gender == "M": ## Si lo pongo como 'candidate.auth_user.gender', eso me devuelve un 'LazyT' no el valor "M" o "F"
        grid[1][0][3] = TH(T("Son"))
        candidate_grid[1][0][1] = TH(T("Son")+": "+simple_fullname(candidate.auth_user.id))
    elif db.auth_user(id=candidate.auth_user.id).gender == "F":
        grid[1][0][3] = TH(T("Daughter"))
        candidate_grid[1][0][1] = TH(T("Daughter")+": "+simple_fullname(candidate.auth_user.id))

    ## Construimos el formulario para verificar los datos
    form = FORM(T("Is the data correct?")+": ",
                INPUT(_name='checked', _type='checkbox', value=False, requires=IS_NOT_EMPTY()),
                SPAN(INPUT(_name='continue', _type='submit', _value=T("Continue"), value=False), _class="right")
               )

    if form.process().accepted:
        change_parent_state(auth.user.id)
        auth.log_event(description="%s - has verified data registered" % (simple_fullname(auth.user.id)))
        redirect(URL('index'))
    return dict(grid=grid, parent_grid=parent_grid, candidate_grid=candidate_grid, form=form)

def modify():
    parent = db((db.auth_user.id==auth.user.id)&
                (db.parent.uid==db.auth_user.id)&
                (db.personal_data.uid==db.auth_user.id)&
                (db.address.id==db.personal_data.address_id)).select().first()
    spouse = db((db.auth_user.id==parent.parent.spouse)&
                (db.parent.uid==parent.parent.spouse)&
                (db.personal_data.uid==parent.parent.spouse)&
                (db.address.id==db.personal_data.address_id)).select().first()
    candidate = db((db.auth_user.id==parent.parent.student_id)&
                (db.candidate.uid==parent.parent.student_id)&
                (db.personal_data.uid==parent.parent.student_id)&
                (db.address.id==db.personal_data.address_id)&
                (db.school.id==db.candidate.school)).select().first()

    if request.args[0] == 'parent' or request.args[0] == 'parent_work':
        subject = parent
    if request.args[0] == 'spouse' or request.args[0] == 'spouse_work':
        subject = spouse
    if request.args[0] == 'candidate' or request.args[0] == 'candidate_school':
        subject = candidate

    form = []
    if request.args[0] == 'parent' or request.args[0] == 'spouse' or request.args[0] == 'candidate':
        form = SQLFORM.factory(db.auth_user.gender,
                               db.auth_user.last_name, db.auth_user.first_name, db.auth_user.middle_name, db.auth_user.email,
                               db.personal_data.mail2, db.personal_data.doc_type, db.personal_data.doc, db.personal_data.nac,
                               db.personal_data.cuil, db.personal_data.dob, #db.personal_data.age,
                               db.personal_data.tel1_type, db.personal_data.tel1, db.personal_data.tel2_type, db.personal_data.tel2,
                               db.address.street, db.address.building, db.address.floor, db.address.apartment, db.address.door,
                               db.address.street1, db.address.street2, db.address.prov, db.address.zip_code,
                               db.personal_data.photo, db.personal_data.facebook, db.personal_data.twitter,
                               submit_button=T("Update Data")
                               )
    elif request.args[0] == 'parent_work' or request.args[0] == 'spouse_work':
        form = SQLFORM.factory(db.parent.work,
                               db.parent.works_in,
                               submit_button=T("Update Data")
                               )
    elif request.args[0] == 'candidate_school':
        form = SQLFORM.factory(db.candidate.course, db.school.name, db.school.number, db.school.district,
                               db.address.street, db.address.building, db.address.floor, db.address.apartment,
                               db.address.door, db.address.street1, db.address.street2, db.address.prov, db.address.zip_code,
                               submit_button=T("Update Data")
                               )

    for table in subject:
        for field in subject[table]:
                form.vars[field] = subject[table][field]
                if isinstance(subject[table][field], datetime.date):
                    form.vars[field] = subject[table][field].strftime(DATE_FORMAT)

    if form.process(dbio=False).accepted:
        test = ""
        if request.args[0] == 'parent' or request.args[0] == 'spouse' or request.args[0] == 'candidate':
            """
            subject.auth_user.gender = form.vars.gender
            subject.auth_user.last_name = form.vars.last_name
            subject.auth_user.first_name = form.vars.first_name
            subject.auth_user.middle_name = form.vars.middle_name
            subject.auth_user.email = form.vars.email
            subject.personal_data.mail2 = form.vars.mail2
            subject.personal_data.doc_type = form.vars.doc_type
            subject.personal_data.doc = form.vars.doc
            subject.personal_data.nac = form.vars.nac
            subject.personal_data.cuil = form.vars.cuil
            subject.personal_data.dob = form.vars.dob
            subject.personal_data.tel1_type = form.vars.tel1_type
            subjec.personal_data.tel1 = form.vars.tel1
            subject.personal_data.tel2_type = form.vars.tel2_type
            subject.personal_data.tel2 = form.vars.tel2
            subject.address.street = form.vars.street
            subject.address.building = form.vars.building
            subject.address.floor = form.vars.florr
            subject.address.apartment = form.vars.apartment
            subject.address.door = form.vars.door
            subject.address.street1 = form.vars.street1
            subject.address.street2 = form.vars.street2
            subject.address.prov = form.vars.prov
            subject.address.zip_code = form.vars.zip_code
            subject.personal_data.photo = form.vars.photo
            subject.personal_data.facebook = form.vars.facebook
            subject.personal_data.twitter = form.vars.twitter

            subject.auth_user.update_record()
            subject.address.update_record()
            subject.personal_data.update_record()
            """

            subject.auth_user.update_record(**db.auth_user._filter_fields(form.vars))
            subject.personal_data.update_record(**db.personal_data._filter_fields(form.vars))
            subject.address.update_record(**db.address._filter_fields(form.vars))

        elif request.args[0] == 'parent_work' or request.args[0] == 'spouse_work':
            """
            subject.parent.work = form.vars.work
            subject.parent.works_in = form.vars.works_in

            subject.parent.update_record()
            """
            subject.parent.update_record(**db.parent._filter_fields(form.vars))
            #db(db.parent.uid==subject.auth_user.id).update(**db.parent._filter_fields(form.vars))
        elif request.args[0] == 'candidate_school':
            """
            subject.candidate.course = form.vars.course
            subject.school.name = form.vars.name
            subject.school.number = form.vars.number
            subject.school.district = form.vars.district
            subject.address.street = form.vars.street
            subject.address.building = form.vars.building
            subject.address.floor = form.vars.floor
            subject.address.apartment = form.vars.apartment
            subject.address.door = form.vars.door
            subject.address.street1 = form.vars.street1
            subject.address.street2 = form.vars.street2
            subject.address.prov = form.vars.prov
            subject.address.zip_code = form.vars.zip_code

            subject.candidate.update_record()
            subject.school.update_record()
            subject.address.update_record()
            """
            #subject.candidate.update_record(**db.candidate._filter_fields(form.vars)) ## NO ANDUVO
            subject.candidate.update_record(course=form.vars.course)
            subject.school.update_record(**db.school._filter_fields(form.vars))
            #db(db.candidate.uid==subject.auth_user.id).update(**db.candidate._filter_fields(form.vars))
            #db((db.school.id==db.candidate.school)&(db.candidate.uid==subject.auth_user.id)).update(**db.school._filter_fields(form.vars))
            #db((db.address.id==db.school.address_id)&(db.school.id==subject.candidate.school)).update(**db.address._filter_fields(form.vars))
        session.flash = T("Records Updated!")
        redirect(URL('index'))
    return locals()

#@auth.requires_membership('padre')
def informative_talk():
    form = SQLFORM.factory(Field('date', requires=IS_IN_DB(db(db.date.type=="informative talk"), 'date.id', '%(date)s %(start_time)s'), label=T("Date"))
                           )
    ## FALTA HACER EL ONVALIDATION PARA QUE CUENTE LOS CUPOS!
    if form.process().accepted:
        db.turn.insert(uid=auth.user.id,
                       date=form.vars.date)
        #change_parent_state(auth.user.id)
        auth.log_event(description="%s - choose informative talk on %s at %s" % (simple_fullname(auth.user.id),
                                                                                 db(db.date.id==form.vars.date).select().first().date,
                       db(db.date.id==form.vars.date).select().first().start_time))
    return locals()
