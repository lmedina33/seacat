# coding: utf8
## configure email
MAIL_USER="seacat"
MAIL_DOMAIN="pioix.edu.ar"
MAIL_PASSWORD="mbqsjpqla2014"
## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = '%s@%s' % (MAIL_USER, MAIL_DOMAIN)
mail.settings.login = '%s@%s:%s' % (MAIL_USER, MAIL_DOMAIN, MAIL_PASSWORD)
