# coding: utf-8
# intente algo como
@auth.requires_membership('secretaria')
def index():
    return dict(message="hello from secretary.py")

def user():
    redirect(URL('default','index'))

@auth.requires(auth.has_permission('create', db.date) or auth.has_permission('create', db.turn))
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
        fila = TR(LABEL(B(date_type)))
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

@auth.requires_permission('create new father', db.auth_user)
def new_parent():
    form = SQLFORM.factory(db.auth_user.first_name,
                           db.auth_user.middle_name,
                           db.auth_user.last_name,
                           db.auth_user.gender,
                           db.auth_user.email,
                           Field('send_mail', 'boolean', default=False, label=T("Send email?")),
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
    #if form.process().accepted:
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
