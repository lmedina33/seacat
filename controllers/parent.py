# coding: utf-8
#72:
#######################################################################
#80:
###############################################################################
#100:
###################################################################################################
"""
Sería prudente hacer la consulta de 'parent', 'spouse' y 'candidate' de manera global en el controlador?
"""
"""
Sería mejor tener una función para los datos y que reciba por argumento a quién tiene que modificar?
(algo parecido a lo que hice en review_data y modify)
"""

@auth.requires_membership('padre')
def index():
    """
    This function redirects the page according to parent state.
    """
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
    return dict()

def user():
    """
    This allows user functions on this controller.
    """
    redirect(URL('default','index'))

@cache.action()
def download():
    ### Aún no sé si es necesario!!!!
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@auth.requires_membership('padre')
def password_change():
    """
    This uses the 'password_change' form from 'Auth'.

    This event is logged automatically on event table because
    auth.change_password form is used.
    """
    def __validate_password(form):
        """
        This checks if old password is being changed for a different one.
        """
        if form.vars.new_password == form.vars.old_password:
            form.errors.new_password = T("You must use a password different than the old one!")
        __change_parents_state(auth.user.id)

    form = auth.change_password(onvalidation=__validate_password, next=URL('index'))
    test=""
    return dict(form=form)

def __change_parents_state(uid):
    """
    Advances the current parents state to the next state according to PARENT_STATE.

    If the parent has spouse, then the spouse state is advanced too.

    ## Se podría mejorar haciendo que reciba un 2º argumento que sea el estado al que queremos que vaya.
    """
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
    ## Si el padre tiene cónyuge y está con el mismo estado, aumentamos.
    if parent.spouse and spouse.state == state:
        __change_parent_state(parent.spouse)

def __change_parent_state(uid):
    """
    Advances only the parent state of the UID provided.
    """
    spouse = db.parent(db.parent.uid==uid)
    ## Incrementamos el estado del padre actual.
    spouse.state = PARENT_STATE[PARENT_STATE.index(spouse.state)+1]
    ## Actualizamos el registro en la DB.
    spouse.update_record()

@auth.requires_membership('padre')
def parent_data():
    """
    This function updates the parent data.

    ## Por ahí habría que pensar en una implementación de una función que reciba como argumento
    ## a quién debe ingresar los datos y después muestre el formulario según eso. 
    ## Como hice en 'modify'.
    """
    form = SQLFORM.factory(db.parent.work,
                           db.parent.works_in,
                           db.personal_data,
                           submit_button=T("Update Data")
                           )
    personal_data = db.personal_data(db.personal_data.uid==auth.user.id)
    parent_data = db.parent(db.parent.uid==auth.user.id)

    ## Pre-popule form with data.
    for field in db.personal_data.fields:
        form.vars[field] = personal_data[field]
        if isinstance(personal_data[field], datetime.date):
            form.vars[field] = personal_data[field].strftime(DATE_FORMAT)
    form.vars.work = parent_data.work
    form.vars.works_in = parent_data.works_in

    if parent_data.state != PARENT_STATE[1]:
        response.flash = ""

    if form.process().accepted:
        ## Update parent data.
        db(db.parent.uid==auth.user.id).update(**db.parent._filter_fields(form.vars))
        db(db.personal_data.uid==auth.user.id).update(**db.personal_data._filter_fields(form.vars))

        if parent_data.spouse:
            ## If the parent was inserted and activated by his/her spouse, first must change his/her
            ## password, then updates his/her personal data. The spouse and candidate data has been
            ## already completed by his/her spouse. So that's why he/she must advances two states.
            #__change_parent_state(auth.user.id)
            #__change_parent_state(auth.user.id)
            spouse_state = db.parent(db.parent.uid==parent_data.spouse).state
            db(db.parent.uid==auth.user.id).update(state=spouse_state)
            auth.log_event(description="%s - advanced to spouse state \"%s\"" % (fullname(auth.user.id), spouse_state))
            session.flash=T("Your are here because your spouse completed some data before.")
        else:
            ## If the parent doesn't have spouse, means that he/she is the first one doing the
            ## registration.
            __change_parents_state(auth.user.id)

        auth.log_event(description="%s - updated personal data" % (fullname(auth.user.id)))

        redirect(URL('index'))
    return dict(form=form, name=simple_fullname(auth.user.id))

@auth.requires_membership('padre')
def spouse_data():
    """
    Insert or Skip spouse's personal data.
    """
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
                           Field("enabled", 'boolean', default=True, label=T("Enable User?"),
                                 comment=T("If you enable the user he will be capable of using the system and make modifications like you do. \
                                 He will be notified by email. Any modifications made in registration process (by him or you) will be notified\
                                 by email to both of us.")),
                           Field('email', 'string', length=128, requires=IS_EMPTY_OR(IS_EMAIL()), label=T("Email")),
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
                           submit_button=T("Insert Data")
                           )

    ## Gender form personalization
    if auth.user.gender == GENDER_LIST[1][0]:
        form.vars.gender = GENDER_LIST[0][0]
		#form.add_button(T("Skip Mother"), URL('_skip_spouse_data'))
        button = A(T("Skip Mother"), _href=URL('_skip_spouse_data'), _class='btn')
    else:
        form.vars.gender = GENDER_LIST[1][0]
        #form.add_button(T("Skip Father"), URL('_skip_spouse_data'))
        button = A(T("Skip Father"), _href=URL('_skip_spouse_data'), _class='btn')

    ## AL PEDO??????
    if db.parent(db.parent.uid==auth.user.id).state != PARENT_STATE[2]:
        response.flash = ""

    if form.process().accepted:
        if not form.vars.enabled:
            form.vars.email = 'spouse_'+str(auth.user.id)+'@nomail.com'
        ## We get the current parent record.
        parent = db.parent(db.parent.uid==auth.user.id)

        ## new_parent_id would be the spouse's logged parent.
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

        ## Updated parent spouse with the new_parent_id
        parent.spouse = new_parent_id
        parent.update_record()

        auth.log_event(description="%s - created new parent: %s" % (fullname(auth.user.id), fullname(new_parent_id)))

        __change_parents_state(auth.user.id)

        ## Enable/Disable spouse's user.
        if not form.vars.enabled:
            db(db.auth_user.id==new_parent_id).update(registration_key="disabled")
            auth.log_event(description="%s - disabled parent: %s" % (fullname(auth.user.id), fullname(new_parent_id)))
        else:
            send_welcome_mail(form, new_parent_id)
            db(db.parent.uid==new_parent_id).update(state=PARENT_STATE[0])

        redirect(URL('index'))
    return locals()

def _skip_spouse_data():
    """
    Skips the spouse's data form, advances the current parent state and logs the event.
    """
    __change_parents_state(auth.user.id)
    auth.log_event(description="Parent %s skipped spouse data" % (fullname(auth.user.id)))
    redirect(URL('index'))

@auth.requires_membership('padre')
def candidate_data():
    """
    Inserts new candidate data.
    """
    form = SQLFORM.factory(db.auth_user.first_name,
                           db.auth_user.middle_name,
                           db.auth_user.last_name,
                           db.auth_user.gender,
                           Field('has_email', 'boolean', default=False, label=T("Has email?"), 
                                 comment=T("If you want your children gets notified, check this and fill below with a valid email address")),
                           ## We use a new field for email because the parent maybe doesn't provide a mail.
                           ## If that the case, the mail would be 'parent_#id@nomail.com'.
                           Field('email', 'string', length=128, requires=IS_EMPTY_OR(IS_EMAIL()), label=T("Email")),
                           #db.auth_user.email,
                           db.personal_data.doc_type,
                           db.personal_data.doc,
                           db.personal_data.nac,
                           db.personal_data.cuil,
                           db.personal_data.dob,
                           db.personal_data.tel1_type,
                           db.personal_data.tel1,
                           db.personal_data.tel2_type,
                           db.personal_data.tel2,
                           db.personal_data.photo,
                           db.personal_data.avatar,
                           db.personal_data.twitter,
                           db.personal_data.facebook,
                           db.personal_data.obs,
                           db.candidate.course,
                           db.candidate.key,
                           submit_button=T("Insert Data")
                           )

    form.vars.tel1_type = db.personal_data(db.personal_data.uid==auth.user.id).tel1_type
    form.vars.tel1 = db.personal_data(db.personal_data.uid==auth.user.id).tel1

    if form.process().accepted:
        if not form.vars.has_email:
            form.vars.email = 'parent_'+str(auth.user.id)+'@nomail.com'

        ## Insert the new candidate.
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

        ## Associate parent with new candidate.
        parent = db.parent(uid=auth.user.id)
        parent.student_id=new_user_id
        parent.update_record()

        ## Associate spouse with new candidate.
        if parent.spouse:
            spouse = db.parent(spouse=auth.user.id)
            spouse.student_id=new_user_id
            spouse.update_record()
        auth.log_event(description="%s - created new candidate: %s" % (fullname(auth.user.id), fullname(new_user_id)))

        ## Enable/Disable candidate user.
        if not form.vars.has_email:
            db(db.auth_user.id==new_user_id).update(registration_key="disabled")
            auth.log_event(description="%s - disabled candidate: %s" % (fullname(auth.user.id), fullname(new_user_id)))
        else:
            send_welcome_mail(form, new_user_id)

        __change_parents_state(auth.user.id)
        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def school_data():
    """
    Associates an school record with a candidate record.
    """
    ## We get the candidate UID associated with the logged parent.
    query = ((auth.user.id == db.parent.uid)
             &(db.parent.student_id == db.candidate.uid)
             &(db.auth_user.id == db.candidate.uid)
             )
    form = SQLFORM.factory(Field('school_id', 'string', length=128,
                                 requires=IS_IN_DB(db, 'school.id', '(%(number)s) %(name)s',
                                                               zero=T("Select one from list or \"Add new school\"")),
                                 label=T("School Name")),
                           Field('candidate_id', requires=IS_IN_DB(db(query), 'auth_user.id',
                                                                   '%(first_name)s %(middle_name)s %(last_name)s',
                                                                   zero=None),
                                 label=T("Sun/Daughter")),
                           submit_button=T("Insert Data")
                           )
    form.add_button(T('Add new school'), URL('add_new_school'))

    if form.process().accepted:
        ## We get the school record.
        school = db.school(db.school.id == form.vars.school_id)
        ## We get the candidate record.
        candidate = db.candidate(db.candidate.uid == form.vars.candidate_id)

        ## Update candidate school.
        candidate.school = school.id
        candidate.update_record()

        __change_parents_state(auth.user.id)

        auth.log_event(description="%s - link candidate %s with school %s" % (fullname(auth.user.id), fullname(candidate.uid), school.number))

        redirect(URL(index))
    return locals()

@auth.requires_membership('padre')
def add_new_school():
    """
    Inserts a new school.
    """
    form = SQLFORM.factory(db.school.name,
                           db.school.number,
                           db.school.district,
                           db.address.street,
                           db.address.building,
                           db.address.loc,
                           db.address.prov,
                           db.address.zip_code,
                           submit_button=T("Insert Data")
                          )
    form.add_button(T("Back"), URL("school_data"))

    if form.process().accepted:
        ## Inserts the new address
        new_address_id = db.address.insert(**db.address._filter_fields(form.vars))
        ## Inserts the new school
        new_school_id = db.school.insert(address_id=new_address_id,
                                         **db.school._filter_fields(form.vars)
                                         )

        auth.log_event(description="%s - created new school: %s" % (fullname(auth.user.id), form.vars.name+"("+form.vars.number+")"))

        redirect(URL(school_data))
    return locals()

@auth.requires_membership('padre')
def parent_address_data():
    """
    Updates parent address data.
    """
    form = SQLFORM(db.address,
                   submit_button=T("Insert Data"))

    if form.process().accepted:
        #new_address_id = form.vars.id
        ## Update the parent address data.
        db(db.personal_data.uid==auth.user.id).update(address_id=form.vars.id)

        __change_parents_state(auth.user.id)

        auth.log_event(description="%s - stored own address (%s)" % (fullname(auth.user.id), form.vars.id))

        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def spouse_address_data():
    """
    Inserts new spouse's address data.
    """
    parent = db((db.auth_user.id==auth.user.id)
                &(db.personal_data.uid==db.auth_user.id)
                &(db.parent.uid==db.auth_user.id)
                ).select().first()

    if parent.parent.spouse:
        form = SQLFORM(db.address,
                       submit_button=T("Insert Data")
                       )

        button1 = A(T("We live together"), _href=URL('_spouses_lives_together'), _class='btn')
        button2 = A(T("Skip Address"), _href=URL('_skip_spouse_address'), _class='btn')

        if form.process().accepted:
            #new_address_id = form.vars.id
            ## Get parent record.
            parent = db.parent(db.parent.uid==auth.user.id)
            ## Update parent address record.
            db((db.personal_data.uid==parent.spouse)).update(address_id=form.vars.id)

            __change_parents_state(auth.user.id)

            auth.log_event(description="%s - stored spouse address (%s)" % (fullname(auth.user.id), form.vars.id))

            redirect(URL('index'))
    else:
        __change_parents_state(auth.user.id)
        auth.log_event(description="%s - spouse omitted, spouse address omitted too" % (fullname(auth.user.id)))
        redirect(URL('index'))
    return locals()

def _spouses_lives_together():
    """
    Sets spouse's address data to matches parent address data.
    """
    ## Get logged parent address_id.
    address_id = db.personal_data(db.personal_data.uid==auth.user.id).address_id
    ## Get logged parent spouse_id.
    spouse_id = db.parent(db.parent.uid==auth.user.id).spouse
    ## Update spouse address_id with parent address_id.
    db(db.personal_data.uid==spouse_id).update(address_id=address_id)

    __change_parents_state(auth.user.id)
    auth.log_event(description="%s - lives with spouse" % (fullname(auth.user.id)))
    redirect(URL('index'))

def _skip_spouse_address():
    """
    Leaves spouse's address data on blank and logs the event.
    """
    __change_parents_state(auth.user.id)
    auth.log_event(description="%s - skip spouse address" % (fullname(auth.user.id)))
    redirect(URL('index'))

@auth.requires_membership('padre')
def candidate_address_data():
    """
    Associates candidate's address data with parent address data or a new address.
    """
    ## Get parent record.
    parent = db((db.auth_user.id==auth.user.id)
                &(db.personal_data.uid==db.auth_user.id)
                &(db.parent.uid==db.auth_user.id)
                ).select().first()
    ## Get candidate record.
    candidate = db((db.auth_user.id==parent.parent.student_id)
                   &(db.personal_data.uid==db.auth_user.id)
                   ).select().first()
    spouse = None

    ## Default LIVES_WITH list, includes Parent and "Doesn't live with parents" options
    LIVES_WITH = ((parent.auth_user.id, simple_fullname(parent.auth_user.id)),
                  ("0", T("Doesn't live with parents")))

    ## If the spouse is registered on the system
    if parent.parent.spouse:
        ## Get spouse record.
        spouse = db((db.auth_user.id==parent.parent.spouse)
                    &(db.personal_data.uid==db.auth_user.id)
                    &(db.parent.uid==db.auth_user.id)
                    ).select().first()
        ## If parents lives in different addresses, the candidate may live with father or mother.
        if parent.personal_data.address_id != spouse.personal_data.address_id and spouse.personal_data.address_id != None: 
            LIVES_WITH = ((parent.auth_user.id, simple_fullname(parent.auth_user.id)),
                          (spouse.auth_user.id, simple_fullname(spouse.auth_user.id)),
                          ("0", T("Doesn't live with parents")))

    form = SQLFORM.factory(Field("lives_with", requires=IS_IN_SET(LIVES_WITH, zero=None), label=T("Lives with")),
                           db.address,
                           submit_button=T("Insert Data")
                           )

    if form.process().accepted:
        ## For log
        addr_id = None

        ## We store the address according to selection.
        if form.vars.lives_with == str(parent.auth_user.id):
            candidate.personal_data.address_id=parent.personal_data.address_id
            candidate.personal_data.update_record()
            addr_id = parent.personal_data.address_id
        elif spouse and form.vars.lives_with == str(spouse.auth_user.id):
            candidate.personal_data.address_id=spouse.personal_data.address_id
            candidate.personal_data.update_record()
            addr_id = spouse.personal_data.address_id
        elif form.vars.lives_with == "0":
            new_address_id = db.address.insert(**db.address._filter_fields(form.vars))
            db(db.personal_data.uid==candidate.auth_user.id).update(address_id=new_address_id)
            addr_id = new_address_id

        __change_parents_state(auth.user.id)

        auth.log_event(description="%s - candidate %s in address (%s)" % (simple_fullname(auth.user.id), simple_fullname(candidate.auth_user.id), addr_id))

        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def survey():
    ## Get the active survey.
    survey = db(db.survey.is_active==True).select().first()

    ## Get survey answers.
    sas = db((db.sa.survey==survey.id)
             &(db.sa.uid==auth.user.id)
             ).select().first()

    if sas:
        if sas.completed:
                __change_parents_state(auth.user.id)
                auth.log_event(description="%s - completed parent survey" % (fullname(auth.user.id)))
                redirect(URL('index'))
        else:
            redirect(URL(c='survey', f='take', args=survey.code_take, vars={'caller':request.url}))
    else:
        redirect(URL(c='survey', f='take', args=survey.code_take, vars={'caller':request.url}))

###################################################################################################
@auth.requires_membership('padre')
def review_data():
    ## Obtenemos el regitro del padre que está conectado
    parent = db((db.auth_user.id==auth.user.id)&
                (db.parent.uid==db.auth_user.id)&
                (db.personal_data.uid==db.auth_user.id)&
                (db.address.id==db.personal_data.address_id)
                ).select().first()
    ## Obtenemos el regitro del cónyuge del padre que está conectado
    if parent.parent.spouse and db.personal_data(db.personal_data.uid==parent.parent.spouse).address_id:
        spouse = db((db.auth_user.id==parent.parent.spouse)&
                    (db.parent.uid==parent.parent.spouse)&
                    (db.personal_data.uid==parent.parent.spouse)&
                    (db.address.id==db.personal_data.address_id)
                    ).select().first()
    else:
        spouse = db((db.auth_user.id==parent.parent.spouse)&
                    (db.parent.uid==parent.parent.spouse)&
                    (db.personal_data.uid==parent.parent.spouse)
                    ).select().first()
    ## Obtenemos el regitro del hijo del padre que está conectado
    candidate = db((db.auth_user.id==parent.parent.student_id)&
                (db.candidate.uid==parent.parent.student_id)&
                (db.personal_data.uid==parent.parent.student_id)&
                (db.address.id==db.personal_data.address_id)&
                (db.school.id==db.candidate.school)
                ).select().first()

    ## Armamos una lista con los campos comunes, los que vamos a mostrar en la primer tabla. El orden importa!
    common_fields = [#db.personal_data.photo,
                     db.auth_user.gender,
                     db.auth_user.last_name, db.auth_user.first_name, db.auth_user.middle_name,
                     db.auth_user.email, db.personal_data.mail2,
                     db.personal_data.doc_type, db.personal_data.doc, db.personal_data.nac,
                     db.personal_data.cuil, db.personal_data.dob, #db.personal_data.age,
                     db.personal_data.tel1_type, db.personal_data.tel1,
                     db.personal_data.tel2_type, db.personal_data.tel2,
                     db.address.street, db.address.building, db.address.floor, db.address.apartment,
                     #db.address.door,
                     db.address.street1, db.address.street2,
                     db.address.prov, db.address.loc, db.address.zip_code,
                     db.personal_data.facebook, db.personal_data.twitter]
    ## Construimos la tabla Común
    grid = TABLE(COLGROUP(
                          COL(_span="1", _style='web2py_grid')
                          ),
                 THEAD(
                       TR(
                           TH(_id="header"),
                           TH(T("Parent"), _id="parent_header"),
                           TH(T("Spouse"), _id="spouse_header"),
                           TH(T("Candidate"), _id="candidate_header"),
                           _id="header__row"
                         )
                       ),
                 TBODY(),
                 _class='web2py_grid',
                 _id="personal_data__table"
                 )

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
					if parent[table][field] == "":
						parent[table][field]
					else:
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
    if spouse:
        __format_data(spouse)
    __format_data(candidate)

    ## Agregamos las filas con los datos que armamos en la lista de campos: common_fields.
    for i,item in enumerate(common_fields):
        if is_odd(i):
            row_class = "odd"
        else:
            row_class = "even"
        if spouse:
            if 'address' in str(item) and 'address' not in spouse:
                grid[2].append(TR(
                                  TH(item.label, _id=str(item)+"__label"),
                                  TD(parent[item], _id=str(item)+"__parent"),
                                  TD("no data", _id=str(item)+"__spouse"),
                                  TD(candidate[item], _id=str(item)+"__candidate"),
                                  _class=row_class,
                                  _id=str(item)+"__row"
                                 )
                              )
            else:
                grid[2].append(TR(
                                  TH(item.label, _id=str(item)+"__label"),
                                  TD(parent[item], _id=str(item)+"__parent"),
                                  TD(spouse[item], _id=str(item)+"__spouse"),
                                  TD(candidate[item], _id=str(item)+"__candidate"),
                                  _class=row_class,
                                  _id=str(item)+"__row"
                                 )
                              )
        else:
            grid[2].append(TR(
                              TH(item.label, _id=str(item)+"__label"),
                              TD(parent[item], _id=str(item)+"__parent"),
                              TD("", _id=str(item)+"__spouse"),
                              TD(candidate[item], _id=str(item)+"__candidate"),
                              _class=row_class,
                              _id=str(item)+"__row"
                             )
                          )
    ## Agregamos los botones de edición en el Table Footer
    grid.append(TFOOT(
                      TR(
                         TD(),
                         TD(TAG.A(T("Edit"), _id="parent__btn", _class="btn", _href=URL('modify', args=['parent']))),
                         TD(TAG.A(T("Edit"), _id="spouse__btn", _class="btn", _href=URL('modify', args=['spouse']))),
                         TD(TAG.A(T("Edit"), _id="candidate__btn", _class="btn", _href=URL('modify', args=['candidate']))),
                         _id="footer__row"
                        )
                     )
                )
    ## Muestra de fotos
    """
    ###############################
    ## LA FOTO NO FUNCIONA!!!!!!!!!!!!!!!!!!!!!
    ###############################

    grid[2][0][1]= TD(IMG(_src=URL('download', args=[parent.personal_data.photo]), _alt=simple_fullname(parent.auth_user.id)+" Photo"), _id='personal_data.photo__parent')
    if spouse:
        grid[2][0][2] = TD(IMG(_src=URL('download', args=spouse.personal_data.photo), _alt=simple_fullname(spouse.auth_user.id)+" Photo"), _id='personal_data.photo__spouse')
    grid[2][0][3] = TD(IMG(_src=URL('download', args=candidate.personal_data.photo), _alt=simple_fullname(candidate.auth_user.id)+" Photo"), _id='personal_data.photo__candidate')
    """
    ## Armamos una lista con los campos exclusivos de los padres. El orden importa!
    parent_fields = [db.parent.work, db.parent.works_in]
    ## Construimos la tabla de Padres
    parent_grid = TABLE(COLGROUP(
                                 COL(_span="1", _style='web2py_grid')
                                ),
                        THEAD(
                              TR(
                                 TH(_id="header"),
                                 TH(T("Parent"), _id="parent_header"),
                                 TH(T("Spouse"), _id="spouse_header"),
                                 _id="header__row"
                                )
                             ),
                        TBODY(),
                        _class='web2py_grid',
                        _id="parents__table"
                        )

    ## Agregamos las filas con los datos que armamos en la lista de campos: parent_fields.
    for i,item in enumerate(parent_fields):
        if is_odd(i):
            row_class = "odd"
        else:
            row_class = "even"
        if spouse:
            parent_grid[2].append(TR(
                                     TH(item.label, _id=str(item)+"__label"),
                                     TD(parent[item], _id=str(item)+"__parent"),
                                     TD(spouse[item], _id=str(item)+"__spouse"),
                                     _class=row_class,
                                     _id=str(item)+"__row"
                                    )
                                 )
        else:
            parent_grid[2].append(TR(
                                     TH(item.label, _id=str(item)+"__label"),
                                     TD(parent[item], _id=str(item)+"__parent"),
                                     TD("", _id=str(item)+"__spouse"),
                                     _class=row_class,
                                     _id=str(item)+"__row"
                                    )
                                 )
    ## Agregamos los botones de edición en el Table Footer
    parent_grid.append(TFOOT(
                             TR(
                                TD(),
                                TD(TAG.A(T("Edit"), _id="parent_work__btn", _class="btn", _href=URL('modify', args=['parent_work']))),
                                TD(TAG.A(T("Edit"), _id="spouse_work__btn", _class="btn", _href=URL('modify', args=['spouse_work']))),
                                _id="footer__row"
                               )
                            )
                       )

    ## Acomodamos los títulos de las columnas acorde al sexo del usuario que está conectado:
    if auth.user.gender == 'M':
        grid[1][0][1] = TH(T("Father"), _id="parent_header")
        grid[1][0][2] = TH(T("Mother"), _id="spouse_header")
        parent_grid[1][0][1] = TH(T("Father")+": "+simple_fullname(parent.auth_user.id), _id="parent_header")
        if spouse:
            parent_grid[1][0][2] = TH(T("Mother")+": "+simple_fullname(spouse.auth_user.id), _id="spouse_header")
        else:
            parent_grid[1][0][2] = TH(T("Mother"), _id="spouse_header")
    else:
        grid[1][0][1] = TH(T("Mother"), _id="parent_header")
        grid[1][0][2] = TH(T("Father"), _id="spouse_header")
        parent_grid[1][0][1] = TH(T("Mother")+": "+simple_fullname(parent.auth_user.id), _id="parent_header")
        if spouse:
            parent_grid[1][0][2] = TH(T("Father")+": "+simple_fullname(spouse.auth_user.id), _id="spouse_header")
        else:
            parent_grid[1][0][2] = TH(T("Mother"), _id="spouse_header")

    ## Armamos una lista con los campos exclusivos de los padres. El orden importa!
    candidate_fields = [db.candidate.course,
                        db.school.name, db.school.number, db.school.district,
                        db.address.street, db.address.building, db.address.floor, db.address.apartment,
                        #db.address.door,
						db.address.street1, db.address.street2,
                        db.address.prov, db.address.loc, db.address.zip_code]
    ## Construimos la tabla de la escuela del Candidato
    candidate_grid = TABLE(COLGROUP(
                                    COL(_span="1", _style='web2py_grid')
                                    ),
                           THEAD(
                                 TR(
                                    TH(_id="header"),
                                    TH(T("Candidate"), _id="candidate_header"),
                                    _id="header__row"
                                   )
                                ),
                           TBODY(),
                           _class='web2py_grid',
                           _id="candidate__table",
                           )
    ## Agregamos las filas con los datos que armamos en la lista de campos: candidate_fields.
    for i,item in enumerate(candidate_fields):
        school_address = db.address((db.school.id==candidate.candidate.school)&(db.school.address_id==db.address.id)).address

        if is_odd(i):
            row_class = "odd"
        else:
            row_class = "even"
        if 'address' in str(item):
            candidate_grid[2].append(TR(
                                        TH(item.label, _id=str(item)+"__label"),
                                        TD(school_address[item], _id=str(item)+"__candidate"),
                                        _class=row_class,
                                        _id=str(item)+"__row"
                                       )
                                    )
        else:
            candidate_grid[2].append(TR(
                                        TH(item.label, _id=str(item)+"__label"),
                                        TD(candidate[item], _id=str(item)+"__candidate"),
                                        _class=row_class,
                                        _id=str(item)+"__row"
                                       )
                                    )
    ## Agregamos los botones de edición en el Table Footer
    candidate_grid.append(TFOOT(
                                TR(
                                   TD(),
                                   TD(TAG.A(T("Edit"), _id="edit_candidate_school__btn", _class="btn", _href=URL('modify', args=['candidate_school']))),
                                   _id="footer__row"
                                  )
                               )
                         )
    ## Acomodamos los títulos de las columnas acorde al sexo del candidato:
    if db.auth_user(id=candidate.auth_user.id).gender == "M": ## Si lo pongo como 'candidate.auth_user.gender', eso me devuelve un 'LazyT' no el valor "M" o "F"
        grid[1][0][3] = TH(T("Son"), _id="candidate_header")
        candidate_grid[1][0][1] = TH(T("Son")+": "+simple_fullname(candidate.auth_user.id), _id="candidate_header")
    elif db.auth_user(id=candidate.auth_user.id).gender == "F":
        grid[1][0][3] = TH(T("Daughter"), _id="candidate_header")
        candidate_grid[1][0][1] = TH(T("Daughter")+": "+simple_fullname(candidate.auth_user.id), _id="candidate_header")

    ## Construimos el formulario para verificar los datos
    form = FORM(T("Is the data correct?")+": ",
                INPUT(_name='checked', _type='checkbox', value=False, requires=IS_NOT_EMPTY()),
                SPAN(INPUT(_name='continue', _type='submit', _value=T("Continue"), value=False), _class="right")
               )

    if form.process().accepted:
        __change_parents_state(auth.user.id)
        auth.log_event(description="%s - has verified data registered" % (simple_fullname(auth.user.id)))
        redirect(URL('index'))
    return dict(grid=grid, parent_grid=parent_grid, candidate_grid=candidate_grid, form=form)

def modify():
    """
    #####################################################
    ## No pude pasar los parent, spouse y candidate, cuando los pasaba como vars, me los pasaba como str.
    #####################################################
    """
    parent = db((db.auth_user.id==auth.user.id)&
                (db.parent.uid==db.auth_user.id)&
                (db.personal_data.uid==db.auth_user.id)&
                (db.address.id==db.personal_data.address_id)
                ).select().first()
    ## Obtenemos el regitro del cónyuge del padre que está conectado
    if parent.parent.spouse and db.personal_data(db.personal_data.uid==parent.parent.spouse).address_id:
        spouse = db((db.auth_user.id==parent.parent.spouse)&
                    (db.parent.uid==parent.parent.spouse)&
                    (db.personal_data.uid==parent.parent.spouse)&
                    (db.address.id==db.personal_data.address_id)
                    ).select().first()
    else:
        spouse = db((db.auth_user.id==parent.parent.spouse)&
                    (db.parent.uid==parent.parent.spouse)&
                    (db.personal_data.uid==parent.parent.spouse)
                    ).select().first()
    candidate = db((db.auth_user.id==parent.parent.student_id)&
                (db.candidate.uid==parent.parent.student_id)&
                (db.personal_data.uid==parent.parent.student_id)&
                (db.address.id==db.personal_data.address_id)&
                (db.school.id==db.candidate.school)
                ).select().first()

    if request.args[0] == 'parent' or request.args[0] == 'parent_work':
        subject = parent
    if request.args[0] == 'spouse' or request.args[0] == 'spouse_work':
        if spouse:
            subject = spouse
        else:
            ## Simplemente para que subject no sea None y no me tire error. ;-)
            subject = parent
    if request.args[0] == 'candidate' or request.args[0] == 'candidate_school':
        subject = candidate

    ## Para poner el dropdown de opciones de donde vive el candidato
    LIVES_WITH = ((auth.user.id, simple_fullname(auth.user.id)),
                  ("0", T("Doesn't live with parents")))
    if parent.parent.spouse:
        if parent.personal_data.address_id != spouse.personal_data.address_id:
            LIVES_WITH = ((auth.user.id, simple_fullname(auth.user.id)),
                          (parent.parent.spouse, simple_fullname(parent.parent.spouse)),
                          ("0", T("Doesn't live with parents")))
        else:
            LIVES_WITH = ((auth.user.id, simple_fullname(auth.user.id)+"& "+simple_fullname(spouse.auth_user.id)),
                          ("0", T("Doesn't live with parents")))

    ## Construimos el formulario de modificación de datos personales.
    if request.args[0] == 'parent' or request.args[0] == 'spouse' or request.args[0] == 'candidate':
        form = SQLFORM.factory(db.auth_user.gender,
                               db.auth_user.last_name, db.auth_user.first_name, db.auth_user.middle_name, db.auth_user.email,
                               db.personal_data.mail2, db.personal_data.doc_type, db.personal_data.doc, db.personal_data.nac,
                               db.personal_data.cuil, db.personal_data.dob, #db.personal_data.age,
                               db.personal_data.tel1_type, db.personal_data.tel1, db.personal_data.tel2_type, db.personal_data.tel2,
                               Field("lives_with", requires=IS_EMPTY_OR(IS_IN_SET(LIVES_WITH, zero=None))),
                               db.address.street, db.address.building, db.address.floor, db.address.apartment, #db.address.door,
                               db.address.street1, db.address.street2, db.address.prov, db.address.loc, db.address.zip_code,
                               db.personal_data.photo, db.personal_data.facebook, db.personal_data.twitter,
                               submit_button=T("Update Data")
                               )
    ## Modificamos el formulario de datos personales que hicimos recién según el perfil a modificar.
    if request.args[0] == 'parent':
        ## Si no es el candidato, sacamos la opción de "vive con"...
        form[0].__delitem__(15)
    if request.args[0] == 'spouse':
        ## Si no es el candidato, sacamos la opción de "vive con"...
        form[0].__delitem__(15)
        ## Si es el cónyuge, agregamos la opción de "tiene email"
        form[0].insert(4, TR(TD(LABEL(T("Has email?"), _for="no_table_has_email", _id="no_table_has_email__label"),_class="w2p_fl"),
                             TD(INPUT(_type='checkbox', _name='has_email', _id="no_table_has_email"), _class="w2p_fw"),
                             TD(T("Check this option if your spouse has email. This will enable your spouse's user."),_class="w2p_fc"),
                             _id="no_table_has_email__row"))
        """
        Agregar función para insertar campos en los SQLFORM.factory
        """
        ## Si es el cónyuge, agregamos la opción de "vive conmigo"
        form[0].insert(16, TR(TD(LABEL(T("My spouse lives with me"), _for="no_table_same_address", _id="no_table_same_address__label"),_class="w2p_fl"),
                             TD(INPUT(_type='checkbox', _name='same_address', _id="no_table_same_address"), _class="w2p_fw"),
                             TD(T("Check this option if you live together"),_class="w2p_fc"),
                             _id="no_table_same_address__row"))
    if request.args[0] == 'candidate':
        ## Si es el candidato, agregamos la opción de "has_email"
        form[0].insert(4, TR(TD(LABEL(T("Has email?"), _for="no_table_has_email", _id="no_table_has_email__label"),_class="w2p_fl"),
                             TD(INPUT(_type='checkbox', _name='has_email', _id="no_table_has_email"), _class="w2p_fw"),
                             TD(T("Check this option if your son/daughter has email. This will enable your son/daugther's user."),_class="w2p_fc"),
                             _id="no_table_has_email__row"))

    ## Construimos el formulario de modificación de datos personales de los padres (trabajo)
    if request.args[0] == 'parent_work' or request.args[0] == 'spouse_work':
        form = SQLFORM.factory(db.parent.work,
                               db.parent.works_in,
                               submit_button=T("Update Data")
                               )
    """
    ########
    ## Me gustaría agregar la posibilidad de que school_id me liste todas las escuelas en la DB, pero cuando ocurre el evento 'onchange' tengo que cargar los campos del formulario y no sé como.
    ########
    """
    ## Construimos el formulario de modificación de datos personales del candidato (escuela y carrera)
    if request.args[0] == 'candidate_school':
        form = SQLFORM.factory(db.candidate.course,
                               Field('school_id', 'string', length=128,
                                     requires=IS_EMPTY_OR(IS_IN_DB(db(db.school.id==subject.candidate.school), 'school.id', '(%(number)s) %(name)s', zero=T("Add new school"))),
									 default=subject.candidate.school,
                                     label=T("Select School"), comment=T("Change the actual school selected or create a new one.")),
                               db.school.name, db.school.number, db.school.district,
                               db.address.street, db.address.building, db.address.floor, db.address.apartment,
                               #db.address.door,
							   db.address.street1, db.address.street2,
                               db.address.prov, db.address.loc, db.address.zip_code,
                               submit_button=T("Update Data")
                               )

    ## Agregamos el botón para volver a la página anterior.
    form.add_button(T("Go Back"), URL('review_data'))

    ## Completamos el formulario con los valores del registro.
    for table in subject:
        for field in subject[table]:
                form.vars[field] = subject[table][field]
                if isinstance(subject[table][field], datetime.date):
                    form.vars[field] = subject[table][field].strftime(DATE_FORMAT)
    ## Modificamos la presentación del formulario según los valores del registro.
    if '@nomail.com' in subject.auth_user.email:
        form.vars.has_email = False
    else:
        form.vars.has_email = True
    if request.args[0] == 'spouse' and spouse:
        if parent.personal_data.address_id == spouse.personal_data.address_id:
            form.vars.same_address = True
        else:
            form.vars.same_address = False
    if request.args[0] == 'candidate':
        if parent.personal_data.address_id == candidate.personal_data.address_id:
            form.vars.lives_with = parent.auth_user.id
        elif spouse.personal_data.address_id == candidate.personal_data.address_id:
            form.vars.lives_with = spouse.auth_user.id
        else:
            form.vars.lives_with = "0"

    ## Solo para que valide, porque con 'parent' o 'spouse' me tira error en "lives_with"
    ## se ve que como lo uso en el constructor y después lo elimino, queda en el validador
    if form.vars.lives_with == None:
        form.vars.lives_with = "0"

    if not spouse:
        for field in form.vars:
            form.vars[field] = ""
        if auth.user.gender == "M":
            form.vars.gender = 'F'
        else:
            form.vars.gender = 'M'
        form.vars.email = 'spouse_'+str(auth.user.id)+'@nomail.com'
        form.vars.prov = parent.address.prov

    if request.args[0] == 'candidate_school':
        school_address = db.address((db.school.id==candidate.candidate.school)&(db.school.address_id==db.address.id)).address
        form.vars.street = school_address.street
        form.vars.building = school_address.building
        form.vars.floor = school_address.floor
        form.vars.apartment = school_address.apartment
        #form.vars.door = school_address.door
        form.vars.street1 = school_address.street1
        form.vars.street2 = school_address.street2
        form.vars.prov = school_address.prov
        form.vars.loc = school_address.loc
        form.vars.zip_code = school_address.zip_code

    if form.process(dbio=False).accepted:
        """
        ###########
        ### El form.vars contiene valores de uid y password que yo nunca agregué ¿?
        ###########
        """
        if not spouse:
            new_uid = db.auth_user.insert(password=str(CRYPT()(form.vars.doc)[0]),
                                          last_name=form.vars.last_name,
                                          first_name=form.vars.first_name,
                                          middle_name=form.vars.middle_name,
                                          email=form.vars.email,
                                          gender=form.vars.gender,
                                          created_by=auth.user.id,
                                          created_on=request.now,
                                          modified_on=request.now,
                                          modified_by=auth.user.id
                                          )
            subject.parent.update_record(spouse = new_uid)
            new_personal_data = db.personal_data.insert(uid=new_uid,
                                                        mail2=form.vars.mail2,
                                                        doc_type=form.vars.doc_type,
                                                        doc=form.vars.doc,
                                                        nac=form.vars.nac,
                                                        cuil=form.vars.cuil,
                                                        dob=form.vars.dob,
                                                        tel1_type=form.vars.tel1_type,
                                                        tel1=form.vars.tel1,
                                                        tel2_type=form.vars.tel2_type,
                                                        tel2=form.vars.tel2,
                                                        photo=form.vars.photo,
                                                        facebook=form.vars.facebook,
                                                        twitter=form.vars.twitter,
                                                        )
            db.parent.insert(uid=new_uid,
                             children_in_school=parent.parent.children_in_school,
                             student_network=parent.parent.student_network,
                             work="",
                             works_in="",
                             spouse=auth.user.id,
                             student_id=parent.parent.student_id,
                             children_registration_year=parent.parent.children_registration_year,
                             student_school=parent.parent.student_school,
                             children_name=parent.parent.children_name,
                             state=parent.parent.state,
                             children_course=parent.parent.children_course)
            auth.log_event("%s - created spouse %s" % (simple_fullname(auth.user.id), new_uid))
            if form.vars.same_address:
                db(db.personal_data.id==new_personal_data).select().first().update_record(address_id = parent.personal_data.address_id)
                auth.log_event("%s - lives with spouse" % (simple_fullname(auth.user.id), new_uid))
            else:
                address_id = db.address.insert(**db.address._filter_fields(form.vars))
                db(db.personal_data.id==new_personal_data).update_record(address_id = address_id)
                auth.log_event("%s - new spouse's (%s) address %s" % (simple_fullname(auth.user.id), new_uid, address_id))
        else:
            if request.args[0] == 'parent' or request.args[0] == 'spouse' or request.args[0] == 'candidate':
                subject.auth_user.update_record(**db.auth_user._filter_fields(form.vars))
                subject.personal_data.update_record(**db.personal_data._filter_fields(form.vars))
                auth.log_event("%s - modified %s data" % (simple_fullname(auth.user.id), request.args[0]))
                if request.args[0] == 'candidate':
                    if form.vars.lives_with == str(parent.auth_user.id):
                        subject.personal_data.update_record(address_id = parent.personal_data.address_id)
                        auth.log_event("%s - candidate lives with parent" % (simple_fullname(auth.user.id)))
                    elif form.vars.lives_with == str(spouse.auth_user.id):
                        subject.personal_data.update_record(address_id = spouse.personal_data.address_id)
                        auth.log_event("%s - candidate lives with spouse" % (simple_fullname(auth.user.id)))
                    else:
                        address_id = db.address.update_or_insert(**db.address._filter_fields(form.vars))
                        subject.personal_data.update_record(address_id = address_id)
                        auth.log_event("%s - new candidate's address (%s)" % (simple_fullname(auth.user.id), address_id))
                    if form.vars.has_email:
                        subject.auth_user.update_record(registration_key="")
                        auth.log_event("%s - candidate's mail enabled" % (simple_fullname(auth.user.id)))
                        ## Mandar mail de bienvenida al usuario candidato.
                        auth.log_event("%s - sent mail to candidate" % (simple_fullname(auth.user.id)))
                if request.args[0] == 'spouse':
                    if form.vars.same_address:
                        subject.personal_data.update_record(address_id = parent.personal_data.address_id)
                        auth.log_event("%s - modified spouse address, lives together" % (simple_fullname(auth.user.id)))
                    else:
                        address_id = db.address.update_or_insert(**db.address._filter_fields(form.vars))
                        subject.personal_data.update_record(address_id = address_id)
                        auth.log_event("%s - modified spouse address, new address (%s)" % (simple_fullname(auth.user.id), address_id))
            elif request.args[0] == 'parent_work' or request.args[0] == 'spouse_work':
                subject.parent.update_record(**db.parent._filter_fields(form.vars))
                auth.log_event("%s - modified %s" % (simple_fullname(auth.user.id), request.args[0].replace("_", " ")))
            elif request.args[0] == 'candidate_school':
                subject.candidate.update_record(course=form.vars.course)
                auth.log_event("%s - modified candidate course" % (simple_fullname(auth.user.id)))
                if form.vars.school_id == None:
                    new_address = db.address.insert(**db.address._filter_fields(form.vars))
                    new_school = db.school.insert(address_id=new_address,
                                                  name=form.vars.name,
                                                  number=form.vars.number,
                                                  district=form.vars.district,
                                                  verified=False,
                                                  )
                    subject.candidate.update_record(school=new_school)
                    auth.log_event("%s - new candidate school %s" % (simple_fullname(auth.user.id), new_school))
                else:
                    subject.school.update_record(**db.school._filter_fields(form.vars))
                    school_address.update_record(**db.address._filter_fields(form.vars))
                    auth.log_event("%s - modified candidate school" % (simple_fullname(auth.user.id)))
        session.flash = T("Records Updated!")
        redirect(URL('index'))
    return locals()

@auth.requires_membership('padre')
def informative_talk():
    query = db.date.type=="informative talk"
    fields = [db.date.date,
              db.date.start_time,
              db.date.end_time,
              db.date.participants,
              db.date.max_participants,
              db.date.description,
              ]
    grid = SQLFORM.grid(query,
                        fields,
                        maxtextlengths={
                                        'date.description': 250,
                                        },
                        create=False,
                        deletable=False,
                        details=False,
                        editable=False,
                        searchable=False,
                        csv=False,
                        paginate=50
                        )
    form = SQLFORM.factory(Field('date', requires=IS_IN_DB(db((db.date.type=="informative talk")
                                                              #&(db.date.max_participants>db.date.participants) ## No me deja comparar con el Virtual Field
                                                              ), 'date.id', '%(date)s at %(start_time)s | %(participants)s of %(max_participants)s'), label=T("Date")),
                           submit_button=T("Choose Date")
                           )

    def __validate_booking(form):
        date = db(db.date.id==form.vars.date).select().first()
        if date.participants == date.max_participants:
            form.errors.date= T("This date is full, please choose another one")

    if form.process(onvalidation=__validate_booking).accepted:
        db.turn.insert(uid=auth.user.id,
                       date=form.vars.date)
        __change_parents_state(auth.user.id)
        auth.log_event(description="%s - choose informative talk on %s at %s" % (simple_fullname(auth.user.id),
                                                                                 db(db.date.id==form.vars.date).select().first().date,
                                                                                 db(db.date.id==form.vars.date).select().first().start_time))
        redirect(URL('index'))
    return dict(grid=grid, form=form)


@auth.requires_membership('padre')
def terms_and_conditions():
    form = SQLFORM.factory(Field('accept', 'boolean', requires=IS_NOT_EMPTY(), label=T("I accept the terms and conditions")),
                           submit_button=T("Accept"))
    if form.process().accepted:
        parent = db(db.parent.uid==auth.user.id).select().first().update_record(accepted_terms=request.now)
        if parent.spouse:
            db((db.parent.spouse==auth.user.id)).select().first().update_record(accepted_terms=request.now)
        __change_parents_state(auth.user.id)
        auth.log_event(description="%s - accepted Terms&Conditions (%s)" % (simple_fullname(auth.user.id), request.now))
        redirect(URL('index'))
    return dict(form=form)

@auth.requires_membership('padre')
def exam_payment():
    return locals()
