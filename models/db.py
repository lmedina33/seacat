# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL(DBURI, check_reserved=[DB_ENGINE])

#if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    #db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
    ## To connect to a PostgreSQL DB: postgres://username:password@server/database
    ## DBURI contains the string to configure de DB it's stored in 0.py
#    db = DAL(DBURI, check_reserved=[DB_ENGINE])
#else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
#    db = DAL('google:datastore')
    ## store sessions and tickets there
#   session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

db.define_table(auth.settings.table_user_name,
                Field('first_name', 'string', length=64, required=True, requires=IS_NOT_EMPTY(), label=T("First Name")),
                Field('middle_name', 'string', length=64, label=T("Middle Name")),
                Field('last_name', 'string', length=128, required=True, requires=IS_NOT_EMPTY(), label=T("Last Name")),
                Field('email', 'string', length=128, required=True, unique=True, requires=IS_EMAIL(), label=T("Email")),
                Field('password', 'password', length=512, readable=False, requires=CRYPT(), label=T('Password')),
                Field('gender', 'string', length=1, default=GENDER_LIST[1][0], requires=IS_IN_SET(GENDER_LIST), label=T("Gender")),
                Field('last_login', 'datetime', label=T("Last Login"), writable=False, readable=True),
                Field('obs', 'text', label=T("Observations")),
                Field('registration_key', 'string', length=512, writable=False, readable=False, default='', label=T("Registration Key")),
                Field('reset_password_key', 'string', length=512, writable=False, readable=False, default='', label=T("Reset Password Key")),
                Field('registration_id', 'string', length=512, writable=False, readable=False, default='', label=T("Registration ID")),
                auth.signature,
                format='%(last_name)s'+", "+'%(first_name)s'+" "+'%(middle_name)s'
                )

auth.settings.table_user = db[auth.settings.table_user_name]
## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=True, migrate=True)

## Defining new table for Images:
db.define_table('image',
                Field('name', 'string', length=128, label=T("Name")),
                Field('file', 'upload', label=T("File"), required=True),
                auth.signature
                )

## Defining new table for address:
db.define_table('address',
                Field('street', 'string', length=128, label=T("Street")),
                Field('building', 'string', length=5, label=T("Building")),
                Field('floor', 'string', length=3, label=T("Floor")),
                Field('door', 'string', length=3, label=T("Door")),
                Field('apartment', 'string', length=3, label=T("Apartment")),
                Field('street1', 'string', length=128, label=T("Street 1")),
                Field('street2', 'string', length=128, label=T("Street 2")),
                Field('zip_code', 'string', length=10, label=T("ZIP Code")),
                Field('loc', 'string', length=64, default=PROVINCES_LIST[2], label=T("Locality")),
                Field('prov', 'string', length=64, requires=IS_IN_SET(PROVINCES_LIST), default=PROVINCES_LIST[2], label=T("Province")),
                Field('obs', 'text', label=T("Observations")),
                auth.signature,
                format='%(street)s'+" "+'%(building)s'+" "+'%(floor)s'+" "+'%(door)s'+" "+'%(apartment)s'
                )
db.address.zip_code.comment=SPAN(T("If you doesn't know your zip code, you can check it on: "), A("Correo Argentino", _target='_blank', _href='http://www.correoargentino.com.ar/formularios/cpa'))

## Defining new table for personal data
db.define_table('personal_data',
                Field('uid', 'reference auth_user', writable=False, readable=False, requires=IS_IN_DB(db, 'auth_user.id'), label=T("User ID")),
                Field('doc_type', 'string', length=10, requires=IS_IN_SET(DOC_TYPE_SET), default=DOC_TYPE_SET[0], label=T("Document Type")),
                Field('doc', 'string', length=8, requires=IS_MATCH('^\d{7,8}$'), label=T("Document"), comment=T("Insert only numbers.")+" i.e.: 12654897"),
                Field('nac', 'string', length=32, default="Argentina", label=T("Nacionality")),
                Field('cuil', 'string', length=11, requires=IS_MATCH('\d{11}'), label="CUIL", comment=T("Insert only numbers")+" i.e.: 20126548971"),
                Field('dob', 'date', requires=IS_DATE(format=(DATE_FORMAT)), label=T("Day of Birth"), comment=T("Use the format dd-mm-aaaa")+" i.e.: 30-08-1978"),
                Field('mail2', 'string', length=128, requires=IS_EMPTY_OR(IS_EMAIL()), label=T("Alternative email"), comment=T("Another contact mail (optional)")),
                Field('tel1_type', 'string', length=32, requires=IS_IN_SET(TEL_TYPE_SET), default=TEL_TYPE_SET[0], label=T("Principal Phone Type"), comment=T("If you choose Cell Phone, do not use (15)")),
                Field('tel1', length=8, requires=IS_MATCH('^\d{6,10}$'), label=T("Principal Phone Number"), comment=T("Insert only numbers, without area code and dashes.")+" i.e.: 49811337"),
                Field('tel2_type', 'string', length=32, requires=IS_EMPTY_OR(IS_IN_SET(TEL_TYPE_SET)), default=TEL_TYPE_SET[0], label=T("Alternative Phone Type"), comment=T("If you choose Cell Phone, do not use (15)")+" "+T("(optional)")),
                Field('tel2', length=8, requires=IS_EMPTY_OR(IS_MATCH('^\d{6,10}$')), label=T("Alternative Phone Number"), comment=T("Insert only numbers, without area code and dashes.")+" i.e.: 49811985"),
                Field('photo', 'upload', uploadfolder=os.path.join(request.folder, 'uploads'), requires=IS_EMPTY_OR(IS_IMAGE(extensions=VALID_IMG_EXTENSION_SET, maxsize=MAX_PHOTO_SIZE)), label=T("Photo"), comment=T("Your picture (optional)")),
                Field('avatar', 'upload', requires=IS_EMPTY_OR(IS_IMAGE(extensions=VALID_IMG_EXTENSION_SET, maxsize=MAX_AVATAR_SIZE)), label=T("Avatar"), comment=T("An image for your profile (optional)")),
                Field('twitter', 'string', length=128, requires=IS_EMPTY_OR(IS_URL()), label=T("Twitter Profile"), comment=T("For social networking (optional)")),
                Field('facebook', 'string', length=128, requires=IS_EMPTY_OR(IS_URL()), label=T("Facebook Profile"), comment=T("For social networking (optional)")),
                Field('obs', 'text', label=T("Observations"), comment=T("Anything you wanna add to your profile that you consider important (optional)")),
                Field('address_id', 'reference address', writable=False, readable=False, requires=IS_IN_DB(db, 'address.id'), label=T("Address ID")),
                auth.signature,
                #Field.Virtual('age', lambda row: diff_in_years(row.dob)),
                format='%(doc)s'
                )
db.personal_data.age = Field.Virtual('age', lambda row: diff_in_years(row.personal_data.dob)) ### REVISAR CUENTA DE LOS AÑOS, NO CALCULA!

db.define_table('school',
                Field('name', 'string', length=50, requires=IS_NOT_EMPTY(), label=T("School Name")),
                Field('number', 'string', requires=IS_MATCH('^A-\d{2,4}$', error_message=T("The format must be A-#, like A-1024")), length=10, label=T("Number"), comment=T("School code.")+" i.e.: A-66"),
                Field('district', 'string', length=6, requires=IS_NOT_EMPTY(), label=T("District")),
                Field('address_id', 'reference address', writable=False, readable=False, requires=IS_IN_DB(db, 'address.id'), label=T("Address ID")),
                Field('verified', 'boolean', default=False, label=T("Verified")),
                auth.signature,
                format="("+'%(number)s'+") "+'%(name)s'
                )

db.define_table('candidate',
                Field('uid', 'reference auth_user', writable=False, readable=False, requires=IS_IN_DB(select_user_from_group('candidato'), 'auth_user.id'), label=T("Candidate ID")),
                Field('cod', 'string', length=32, label=T("Candidate Code")),
                Field('school', 'reference school', label=T("School")),
                Field('course', 'string', length=16, requires=IS_IN_SET(COURSE), label=T("Course")),
                Field('admitted', 'boolean', default=False, label=T("Admitted")),
                Field('key', 'integer', requires=IS_INT_IN_RANGE(0,99999999), label=T("Form Number")),
                auth.signature,
                format='%(db.auth_user.last_name)s'+', '+'%(db.auth_user.first_name)s'+' '+'%(db.auth_user.middle_name)s'
                )

## Defining new table for Parents.
db.define_table('parent',
                Field('uid', 'reference auth_user', writable=False, readable=False, requires=IS_IN_DB(select_user_from_group('padre'), 'auth_user.id'), label=T("Father ID")),
                Field('children_in_school', 'boolean', label=T("Do you have children in our school?")),
                Field('children_name', 'string', length=128, label=T("Children name")),
                Field('children_course', 'string', length=16, requires=IS_EMPTY_OR(IS_IN_SET(COURSE)), label=T("Children course")),
                Field('children_registration_year', length=4, requires=IS_EMPTY_OR(IS_MATCH('^\d{4}$', error_message=T("Please insert year in the format YYYY")+" i.e.: 2008")), label=T("Children Registration Year")),
                Field('student_network', 'boolean', label=T("Does your son goes to a school in our network?")),
                Field('student_school', 'string', length=32, requires=IS_EMPTY_OR(IS_IN_SET(SCHOOL_NETWORK_LIST)), label=T("Choose your school")),
                Field('is_alive', 'boolean', required=True, default=True, label=T("Is Alive?")),
                Field('work', 'string', length=100, label=T("Work"), comment=T("Teacher, Sailsman, Engineer, etc...")),
                Field('works_in', 'string', length=100, label=T("Works in"), comment=T("Where you work")),
                Field('spouse', 'reference auth_user', label=T("Spouse")),
                Field('state', 'string', length=32, requires=IS_IN_SET(PARENT_STATE), label=T("State")),
                Field('student_id', 'reference auth_user', label=T("Student")),
                auth.signature,
                format='%(db.auth_user.last_name)s'+', '+'%(db.auth_user.first_name)s'+' '+'%(db.auth_user.middle_name)s'
               )

db.define_table('date',
                Field('type', 'string', length=16, requires=IS_IN_SET(DATE_TYPE), label=T("Date Type")),
                Field('date', 'date', required=True, requires=IS_DATE(DATE_FORMAT), label=T("Date")),
                Field('start_time', 'time', requires=IS_EMPTY_OR(IS_TIME()), label=T("Start Time")),
                Field('end_time', 'time', requires=IS_EMPTY_OR(IS_TIME()), label=T("End Time")),
                Field('description', 'string', length=128, label=T("Description")),
                Field('participants', 'integer', length=2, label=T("Participants")),
                auth.signature
                )

db.define_table('general_date',
                Field('type', 'string', length=64, requires=IS_IN_SET(GENERAL_DATE_TYPE), label=T("Date Type")),
                Field('year', 'integer', length=4, required=True, requires=IS_IN_SET(['2013', '2014', '2015', '2016', '2017', '2018']), label=T("Year")),
                Field('date', 'date', requires=IS_DATE(DATE_FORMAT), label=T("Date")),
                Field('start_time', 'time', requires=IS_EMPTY_OR(IS_TIME()), label=T("Start Time")),
                Field('end_time', 'time', requires=IS_EMPTY_OR(IS_TIME()), label=T("End Time")),
                auth.signature
                )

db.define_table('turn',
                Field('uid', 'reference auth_user', writable=False, readable=False, requires=IS_IN_DB(select_user_from_group('padre'), 'auth_user.id'), label=T("Father ID")),
                Field('date', 'reference date', requires=IS_IN_DB(db, 'date.id'), label=T("Date ID"))
                )

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
