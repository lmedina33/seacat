# coding: utf8
####################################################################################################
## To setup the new app
####################################################################################################

#SETTED_UP = False

#if not db().select(db.auth_user.ALL):
    #auth.settings.actions_disabled = []
#    redirect(URL('default', 'user', args='register', vars=dict(_next = URL('default', 'set_up'))))

#def setting_up():
#    global SETTED_UP
#    if not SETTED_UP:
        #redirect(URL('default', 'index'))
        ## Deactivating register form from User.
        #auth.settings.actions_disabled.append('register')
        ## After adding the First User
        ## we have to add the Groups:
#        db.auth_group.insert(role='root', description='Superadministrador')
#        db.auth_group.insert(role='empleado', description='Empleado de la Casa')
#        db.auth_group.insert(role='soporte', description='Soporte Técnico')
#        db.auth_group.insert(role='directivo', description='Directivo')
#        db.auth_group.insert(role='director', description='Director General')
#        db.auth_group.insert(role='rector', description='Rector del Colegio')
#        db.auth_group.insert(role='secretaria', description='Secretaría')
#        db.auth_group.insert(role='secretario', description='Secretario')
#        db.auth_group.insert(role='derivaciones', description='Oficina de Derivaciones')
#        db.auth_group.insert(role='eoe', description='Equipo de Orientación Escolar')
#        db.auth_group.insert(role='administracion', description='Administración')
#        db.auth_group.insert(role='administrador', description='Administrador')
#        db.auth_group.insert(role='caja', description='Caja')
#        db.auth_group.insert(role='padre', description='Padre o Madre')
#        db.auth_group.insert(role='candidato', description='Ingresante')
        ## And then the membership on root Group to First User:
#        auth.add_membership(1,1)
        ## Later we add permissions:
#        auth.add_permission(db.auth_group(role='root').id, 'create', db.auth_user, 0)
#        auth.add_permission(db.auth_group(role='root').id, 'view', db.auth_user, 0)
#        auth.add_permission(db.auth_group(role="derivaciones").id, 'create new father', db.auth_user, 0)
#        auth.add_permission(db.auth_group(role="derivaciones").id, 'view fathers list', db.auth_user, 0)
#        SETTED_UP = True
        #response.flash = str(SETTED_UP)
#    else:
#        redirect(URL('default', 'index'))
