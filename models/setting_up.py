# coding: utf8
####################################################################################################
## To setup the new app
##
## Be sure that databases directory is empty and seacat.sup contains a 0.
####################################################################################################

with open(os.path.join(request.folder, 'private', 'seacat.sup'), 'r') as setup_file:
    SETTED_UP = bool(int(setup_file.readline().strip()))
setup_file.close()

if not SETTED_UP:
    print "Setting up for the first time..."
    print "Reading values from seacat_conf.py"
    import seacat_conf
    print "Adding new SuperUser..."
    root_uid = db.auth_user.insert(first_name=seacat_conf.first_name,
                                   middle_name=seacat_conf.middle_name,
                                   last_name=seacat_conf.last_name,
                                   email=seacat_conf.email,
                                   password=str(CRYPT()(seacat_conf.password)[0]),
                                   gender=seacat_conf.gender,
                                   )
    print "Adding new Roles..."
    root_gid = db.auth_group.insert(role='root', description='Superadministrador')
    db.auth_group.insert(role='empleado', description='Empleado de la Casa')
    db.auth_group.insert(role='soporte', description='Soporte Técnico')
    db.auth_group.insert(role='directivo', description='Directivo')
    db.auth_group.insert(role='director', description='Director General')
    db.auth_group.insert(role='rector', description='Rector del Colegio')
    db.auth_group.insert(role='secretaria', description='Secretaría')
    db.auth_group.insert(role='secretario', description='Secretario')
    db.auth_group.insert(role='derivaciones', description='Oficina de Derivaciones')
    db.auth_group.insert(role='eoe', description='Equipo de Orientación Escolar')
    db.auth_group.insert(role='administracion', description='Administración')
    db.auth_group.insert(role='administrador', description='Administrador')
    db.auth_group.insert(role='caja', description='Caja')
    db.auth_group.insert(role='padre', description='Padre o Madre')
    db.auth_group.insert(role='candidato', description='Ingresante')

    ## And then the membership on root Group to First User:
    print "Adding Root to Superadministrator group..."
    auth.add_membership(root_gid, root_uid)

    ## Later we add permissions:
    print "Adding permissions..."
    print "... setting all permissions (CRUD) to all tables for root"
    actions = ['create', 'read', 'update', 'delete']
    count = 0
    for action in actions:
        for table in db.tables:
            auth.add_permission(db.auth_group(role='root').id, action, table, 0)
            count = count + 1
    auth.add_permission(db.auth_group(role="root").id, 'create new father', db.auth_user, 0)
    count = count + 1
    auth.add_permission(db.auth_group(role="root").id, 'view fathers list', db.auth_user, 0)
    count = count + 1
    print "\t\t %d permission added for root" % count

    groups = ['directivo', 'director', 'rector', 'secretario', 'secretaria', 'derivaciones']
    for group in groups:
        print "... setting 'create new father' permission to group %s" % group
        auth.add_permission(db.auth_group(role=group).id, 'create new father', db.auth_user, 0)
        print "... setting 'view fathers list' permission to group %s" % group
        auth.add_permission(db.auth_group(role=group).id, 'view fathers list', db.auth_user, 0)

    for action in actions:
        groups = ['rector', 'secretario']
        for group in groups:
            print "... setting %s on auth_user table to group %s" % (action, group)
            auth.add_permission(db.auth_group(role=group).id, action, db.auth_user, 0)
            print "... setting %s on date table to group %s" % (action, group)
            auth.add_permission(db.auth_group(role=group).id, action, db.date, 0)

    for action in actions:
        groups = ['rector', 'secretario', 'secretaria', 'derivaciones', 'eoe']
        for group in groups:
            print "... setting %s on turn table to group %s" % (action, group)
            auth.add_permission(db.auth_group(role=group).id, action, db.turn, 0)

    print "Saving configuration status"
    with open(os.path.join(request.folder, 'private', 'seacat.sup'), 'w') as setup_file:
        SETTED_UP = 1
        setup_file.write(str(SETTED_UP))
        setup_file.close()
    print "First setup is done! GOOD JOB!! ;-)"
