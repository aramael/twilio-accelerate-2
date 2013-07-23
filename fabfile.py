from fabric.api import *


# === Environments ===
def development():
    env.env = 'development'
    env.settings = 'settings.local'


def staging():
    env.env = 'staging'
    env.settings = 'settings.staging'
    env.remote = 'staging'
    env.heroku_app = 'staging'


def production():
    env.env = 'production'
    env.settings = 'settings.production'
    env.remote = 'production'
    env.heroku_app = 'production'


# Default Environment
development()


# === Deployment ===
def deploy():
    local('git push origin --all')
    local('git push {remote}'.format(**env))
    local('heroku open --remote {heroku_app}'.format(**env))


def open():
    if env.env == 'development':
        local('/usr/bin/open \'http://127.0.0.1:8000/\'')
        local('python manage.py runserver')
    else:
        local('heroku open --remote {heroku_app}'.format(**env))

# === DB ===
def resetdb():
    if env.env == 'development':
        local('python manage.py syncdb --settings={settings}'.format(**env))
        local('python manage.py migrate --settings={settings}'.format(**env))
    else:

        if raw_input('\nDo you really want to RESET DATABASE of {heroku_app}? YES or [NO]: '.format(**env)) == 'YES':
            local('heroku run python manage.py syncdb --noinput --settings={settings} --remote {heroku_app}'.format(
                **env))
            local('heroku run python manage.py migrate --settings={settings} --remote {heroku_app}'.format(**env))
        else:
            print '\nRESET DATABASE aborted'


def schemamigration(app_names):
    local('python manage.py schemamigration {} --auto --settings={settings}'.format(app_names, **env))


def migrate():
    if env.env == 'development':
        local('python manage.py migrate --settings={settings}'.format(**env))
    else:

        if raw_input('\nDo you really want to MIGRATE DATABASE of {heroku_app}? YES or [NO]: '.format(**env)) == 'YES':
            local('heroku run python manage.py migrate --settings={settings} --remote {heroku_app}'.format(**env))
        else:
            print '\nMIGRATE DATABASE aborted'


def updatedb(app_names):
    schemamigration(app_names)
    migrate()


# === Heroku ===
def ps():
    local('heroku ps --remote {heroku_app}'.format(**env))


def restart():
    if raw_input('\nDo you really want to RESTART (web/worker) {heroku_app}? YES or [NO]: '.format(**env)) == 'YES':
        local('heroku ps:restart web --remote {heroku_app}'.format(**env))
    else:
        print '\nRESTART aborted'


def tail():
    local('heroku logs --tail --remote {heroku_app}'.format(**env))


def shell():
    if env.env == 'development':
        local('python manage.py shell --settings={settings}'.format(**env))
    else:
        local('heroku run bash --remote {heroku_app}'.format(**env))


def config():
    local('heroku config --remote {heroku_app}'.format(**env))


def set(key=None, value=None):
    if key and value:
        local('heroku config:add {}={} --remote {heroku_app}'.format(key, value, **env))
    else:
        print '\nErr!'