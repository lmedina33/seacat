# coding: utf8
# intente algo como
@auth.requires_membership('secretaria')
def index():
    return dict(message="hello from secretary.py")

def user():
    redirect(URL('default','index'))

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
