# coding: utf8

## Removing "remember me" feature at login form
auth.settings.remember_me_form = False

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.settings.create_user_groups = False

auth.settings.login_url = URL('user',args='login')
auth.settings.logged_url = URL('user',args='profile')
auth.settings.download_url = URL('download')
auth.settings.login_next = URL('index')
auth.settings.logout_next = URL('index')
auth.settings.profile_next = URL('index')
auth.settings.register_next = URL('user',args='login')
auth.settings.retrieve_username_next = URL('index')
auth.settings.retrieve_password_next = URL('index')
auth.settings.change_password_next = URL('index')
auth.settings.request_reset_password_next = URL('user', args='login')
auth.settings.reset_password_next = URL('user', args='login')
auth.settings.verify_email_next = URL('user', args='login')
auth.settings.on_failed_authentication = URL('user', args='login')


if not db().select(db.auth_user.ALL):
    auth.settings.actions_disabled = []
else:
    auth.settings.actions_disabled = ['register']
