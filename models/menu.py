# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

#response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
#                  _class="brand",_href="http://www.web2py.com/")
#response.title = request.application.replace('_',' ').title()
#response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
#response.meta.author = 'Your Name <you@example.com>'
#response.meta.description = 'a cool new app'
#response.meta.keywords = 'web2py, python, framework'
#response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## My Own APP Title, subtitle and menu!
#########################################################################
response.logo = A(IMG(_src=URL('static', 'Logo_seacat_mini.png'), 
                      _alt="Logo de SEACAT"), 
                  _class="brand", 
                  _href=URL('default', 'index'))
response.title = 'SEACAT'
response.subtitle = 'v.0.0.1b'

response.meta.author = 'Leandro E. Colombo Viña <colomboleandro@pioix.edu.ar>'
response.meta.description = 'Sistema de Inscripciones para el Colegio Pío IX'
response.meta.keywords = 'Inscripciones, Pío IX, Ingresantes, SEACAT'
response.meta.generator = 'Web2py Web Framework'

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

## Top level Menu:
if auth.is_logged_in():
    response.menu = [
                     [T('Home'), False, URL('default', 'index'), []], ## response.menu[0] to insert always on [3]
                     [T('New'), False, None, []], ## response.menu[1] to insert always on [3]
                     [T('View'), False, None, []], ## response.menu[2] to insert always on [3]
                     [T('Help'), False, URL('default', 'help'), []], ## response.menu[3] to insert always on [3]
    ]

## EXAMPLES:
#response.menu.insert(2, [T('TEST'), False, None, []])
#response.menu[2][3].insert(0, [T('test1'), False, None, []])
#response.menu[2][3].insert(1, [T('test2'), False, None, []])
if auth.has_permission('create new father', db.auth_user):
    if auth.has_membership('derivaciones'):
        response.menu[1][3].insert(0, [T("Parent"), False, URL('new_parent')])
    else:
        response.menu[1][3].insert(0, [T("Parent"), False, URL('secretary', 'new_parent')])

if auth.has_permission('create', db.turn) or auth.has_permission('create', db.date):
    response.menu[1][3].append([T("Date"), False, None, []])

if auth.has_permission('create', db.turn):
    response.menu[1][3][1][3].append([T("Turns"), False, URL('secretary', 'new_turn')])

if auth.has_permission('create', db.date):
    response.menu[1][3][1][3].append(["General", False, URL('default','new_general_dates')])

if auth.has_permission('read', db.auth_user):
    response.menu[2][3].insert(0, [T("Users List"), False, URL(request.application, 'admin', 'users_list')])

if auth.has_permission('read', db.turn):
    response.menu[2][3].insert(0, [T("Turns List"), False, URL(request.application, 'admin', 'turns_list')])

if auth.has_permission('read', db.date):
    response.menu[2][3].append([T("Dates List"), False, URL('admin','dates_list')])

if auth.has_permission('read', db.date):
    response.menu[2][3].append([T("General Dates List"), False, URL('admin','general_dates_list')])

if auth.has_permission('view fathers list', db.auth_user):
    response.menu[2][3].insert(0, [T("Parents List"), False, URL('reception', 'parents_list')])

if auth.has_permission('create', db.auth_user):
    response.menu[1][3].append([T("User"), False, URL(request.application, 'admin', 'new_user')])

if auth.has_membership('root'):
    response.menu.insert(2, [SPAN(T("Admin"), _class='highlighted'), False, None, [
                                                       [T("Database"), False, URL(request.application, 'appadmin', 'index')],
                                                       [T("Upload Image"), False, URL(request.application, 'admin', 'upload_image')],
                                                       [T("Users"), False, URL(request.application, 'admin', 'admin_users')],
                                                       [T("Users Groups"), False, URL(request.application, 'admin', 'admin_user_groups')],
                                                       [T("Users Memberships"), False, URL(request.application, 'admin', 'admin_user_memberships')],
                                                       [T("Users Permissions"), False, URL(request.application, 'admin', 'admin_user_permissions')],
                                                       ]])
if auth.has_permission('create', db.survey):
    response.menu.insert(-1, [T("Surveys"), False, None, [
                                                         [T("New Survey"), False, URL('survey','new_survey')],
                                                         [T("Survey List"), False, URL('survey','survey_list')],
                                                         ]])

DEVELOPMENT_MENU = False

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (SPAN('web2py', _class='highlighted'), False, 'http://web2py.com', [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, URL('admin', 'default', 'design/%s' % app), [
        (T('Controller'), False,
         URL(
         'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
        (T('View'), False,
         URL(
         'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
        (T('Layout'), False,
         URL(
         'admin', 'default', 'edit/%s/views/layout.html' % app)),
        (T('Stylesheet'), False,
         URL(
         'admin', 'default', 'edit/%s/static/css/web2py.css' % app)),
        (T('DB Model'), False,
         URL(
         'admin', 'default', 'edit/%s/models/db.py' % app)),
        (T('Menu Model'), False,
         URL(
         'admin', 'default', 'edit/%s/models/menu.py' % app)),
        (T('Database'), False, URL(app, 'appadmin', 'index')),
        (T('Errors'), False, URL(
         'admin', 'default', 'errors/' + app)),
        (T('About'), False, URL(
         'admin', 'default', 'about/' + app)),
        ]),
            ('web2py.com', False, 'http://www.web2py.com', [
             (T('Download'), False,
              'http://www.web2py.com/examples/default/download'),
             (T('Support'), False,
              'http://www.web2py.com/examples/default/support'),
             (T('Demo'), False, 'http://web2py.com/demo_admin'),
             (T('Quick Examples'), False,
              'http://web2py.com/examples/default/examples'),
             (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
             (T('Videos'), False,
              'http://www.web2py.com/examples/default/videos/'),
             (T('Free Applications'),
              False, 'http://web2py.com/appliances'),
             (T('Plugins'), False, 'http://web2py.com/plugins'),
             (T('Layouts'), False, 'http://web2py.com/layouts'),
             (T('Recipes'), False, 'http://web2pyslices.com/'),
             (T('Semantic'), False, 'http://web2py.com/semantic'),
             ]),
            (T('Documentation'), False, 'http://www.web2py.com/book', [
             (T('Preface'), False,
              'http://www.web2py.com/book/default/chapter/00'),
             (T('Introduction'), False,
              'http://www.web2py.com/book/default/chapter/01'),
             (T('Python'), False,
              'http://www.web2py.com/book/default/chapter/02'),
             (T('Overview'), False,
              'http://www.web2py.com/book/default/chapter/03'),
             (T('The Core'), False,
              'http://www.web2py.com/book/default/chapter/04'),
             (T('The Views'), False,
              'http://www.web2py.com/book/default/chapter/05'),
             (T('Database'), False,
              'http://www.web2py.com/book/default/chapter/06'),
             (T('Forms and Validators'), False,
              'http://www.web2py.com/book/default/chapter/07'),
             (T('Email and SMS'), False,
              'http://www.web2py.com/book/default/chapter/08'),
             (T('Access Control'), False,
              'http://www.web2py.com/book/default/chapter/09'),
             (T('Services'), False,
              'http://www.web2py.com/book/default/chapter/10'),
             (T('Ajax Recipes'), False,
              'http://www.web2py.com/book/default/chapter/11'),
             (T('Components and Plugins'), False,
              'http://www.web2py.com/book/default/chapter/12'),
             (T('Deployment Recipes'), False,
              'http://www.web2py.com/book/default/chapter/13'),
             (T('Other Recipes'), False,
              'http://www.web2py.com/book/default/chapter/14'),
             (T('Buy this book'), False,
              'http://stores.lulu.com/web2py'),
             ]),
            (T('Community'), False, None, [
             (T('Groups'), False,
              'http://www.web2py.com/examples/default/usergroups'),
                        (T('Twitter'), False, 'http://twitter.com/web2py'),
                        (T('Live Chat'), False,
                         'http://webchat.freenode.net/?channels=web2py'),
                        ]),
                (T('Plugins'), False, None, [
                        ('plugin_wiki', False,
                         'http://web2py.com/examples/default/download'),
                        (T('Other Plugins'), False,
                         'http://web2py.com/plugins'),
                        (T('Layout Plugins'),
                         False, 'http://web2py.com/layouts'),
                        ])
                ]
         )]

if DEVELOPMENT_MENU: _()

#if "auth" in locals(): auth.wikimenu()
