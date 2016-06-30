from fabric.api import env, run, sudo, local, settings
from fabric.contrib.project import upload_project
from fabric.contrib.files import sed
import os

def production():
	"""Defines production environment"""
        env.user = "root"
        env.nginx_user = "nginx"
        env.hosts = [ 'QPDSite01' ]
        env.port = "2222"
        env.base_dir = "/data/workspace/gwsite/runtime"
        env.app_name = "gizwits_site"
        env.domain_name = "gwsite"
        env.code_path = "/data/workspace/gwsite/src/code"
        env.domain_path = "%(base_dir)s/%(domain_name)s" % { 'base_dir': env.base_dir, 'domain_name': env.domain_name }
        env.current_path = "%(domain_path)s/current" % { 'domain_path': env.domain_path }
        env.releases_path = "%(domain_path)s/releases" % { 'domain_path': env.domain_path }
        env.shared_path = "%(domain_path)s/shared" % { 'domain_path': env.domain_path }
        env.git_clone = "git@gitlab.xtremeprog.com:gizwits/gizwits_site.git"
        env.git_branch = "master"
        env.env_file = "requirements.txt"
        env.virtualenv = "/data/workspace/env/env_gwsite"
        env.settings = "settings_production"
        env.settings_file = "/data/workspace/gwsite/config/settings_production.py"
        env.wsgi_file = "/data/workspace/gwsite/config/wsgi.py"
        env.uwsgi_init_file = "uwsgi-site"


def releases():
    """Lists a release made"""
    env.releases = sorted(run('ls -x %(releases_path)s' % { 'releases_path': env.releases_path }).split())
    if len(env.releases) >= 1:
        env.current_revision = env.releases[-1]
        print("-----" + env.releases[-1])
        env.current_release = "%(releases_path)s/%(current_revision)s" % { 'releases_path': env.releases_path, 'current_revision': env.current_revision }
    if len(env.releases) > 1:
        env.previous_revision = env.releases[-2]
        print("-----" + env.releases[-2])
        env.previous_release = "%(releases_path)s/%(previous_revision)s" % { 'releases_path': env.releases_path, 'previous_revision': env.previous_revision }


def permissions():
    """Makes the release group-writable"""
    sudo("chmod -R g+w %(domain_path)s" % { 'domain_path': env.domain_path })
    sudo("chown -R nginx:nginx %(domain_path)s" % { 'domain_path': env.domain_path })


def setup():
    """Prepares one or more servers for deployment"""
    run("mkdir -p %(domain_path)s/{releases,shared}" % { 'domain_path': env.domain_path })
    run("mkdir -p %(shared_path)s/{system,log,index,install,upload}" % { 'shared_path': env.shared_path })
    run("mkdir -p %(shared_path)s/upload/generated" % { 'shared_path': env.shared_path })
    permissions()


def checkout():
    """Checkout code to the remote servers"""
    import time
    env.current_release = "%(releases_path)s/%(time)s" % { 'releases_path': env.releases_path, 'time': time.strftime("%Y%m%d%I%M%S", time.localtime()) }
    with settings(warn_only=True):
        if local("test -d %(code_path)s" % { 'code_path': env.code_path }).failed:
            local("ssh-agent bash -c 'ssh-add ~/.ssh/gwsite_id_rsa; git clone -q -o deploy --depth 1 -b %(git_branch)s %(git_clone)s %(code_path)s'" % { 'code_path': env.code_path, 'git_branch': env.git_branch, 'git_clone': env.git_clone })
        else:
            local("cd %(code_path)s; ssh-agent bash -c 'ssh-add ~/.ssh/gwsite_id_rsa; git pull'" % { 'code_path': env.code_path })
    local("cp -r %(code_path)s %(current_release)s" % { 'code_path': env.code_path, 'current_release': env.current_release })

    release_settings_file = "%(current_release)s/%(app_name)s/" % { 'current_release': env.current_release, 'app_name': env.app_name } + os.path.split(env.settings_file)[-1]
    local("cp %(settings_file)s %(release_settings_file)s" % { 'settings_file': env.settings_file, 'release_settings_file': release_settings_file})
    sed(release_settings_file, '\{current_release\}', env.current_release)

    local("cp %(wsgi_file)s %(current_release)s/%(app_name)s/" % { 'wsgi_file': env.wsgi_file, 'current_release': env.current_release, 'app_name': env.app_name })
    run("mkdir -p %(current_release)s" % { 'current_release': env.current_release })
    upload_project("%(current_release)s/" % { 'current_release': env.current_release }, "%(releases_path)s" % { 'releases_path': env.releases_path })


def update_code():
    """Copies your project to the remote servers"""
    checkout()
    permissions()


def symlink():
    """Updates the symlink to the most recently deployed version"""
    if not env.has_key('current_release'):
        releases()
    run("ln -nfs %(current_release)s %(current_path)s" % { 'current_release': env.current_release, 'current_path': env.current_path })
    run("ln -nfs %(shared_path)s/log %(current_release)s/log" % { 'shared_path': env.shared_path, 'current_release': env.current_release })
    run("ln -nfs %(shared_path)s/upload %(current_release)s/upload" % { 'shared_path': env.shared_path, 'current_release': env.current_release })


def collectstatic():
    """Collect static files"""
    if not env.has_key('current_release'):
        releases()
    run("source %(virtualenv)s/bin/activate; cd %(current_release)s/; python manage.py collectstatic --noinput --settings=%(app_name)s.%(settings)s" % { 'virtualenv': env.virtualenv, 'current_release': env.current_release, 'app_name': env.app_name, 'settings': env.settings })
    run("mkdir -p %(current_release)s/_static/CACHE/; chown -R %(nginx_user)s.%(nginx_user)s %(current_release)s/_static/CACHE/" % { 'current_release': env.current_release, 'nginx_user': env.nginx_user })
    run("source %(virtualenv)s/bin/activate; cd %(current_release)s/; python manage.py compress --force --settings=%(app_name)s.%(settings)s" % { 'virtualenv': env.virtualenv, 'current_release': env.current_release, 'app_name': env.app_name, 'settings': env.settings })
    run("mkdir %(current_release)s/static/" % { 'current_release': env.current_release })
    run('if [ ! -d "%(current_path)s/_static" ]; then cp -r %(current_path)s/static %(current_path)s/_static;fi' % { 'current_path': env.current_path })
    run("cp -r %(current_path)s/_static/* %(current_release)s/_static/* %(current_release)s/static 2>/dev/null || :" % { 'current_release': env.current_release, 'current_path': env.current_path })


def migrate():
    """Run the migration task"""
    if not env.has_key('current_release'):
        releases()
    run("source %(virtualenv)s/bin/activate; cd %(current_release)s/; python manage.py migrate --settings=%(app_name)s.%(settings)s" % { 'virtualenv': env.virtualenv, 'current_release': env.current_release, 'app_name': env.app_name, 'settings': env.settings })


def syncdb():
    """Run syncdb"""
    if not env.has_key('current_release'):
        releases()
    run("source %(virtualenv)s/bin/activate; cd %(current_release)s/; python manage.py syncdb --settings=%(app_name)s.%(settings)s" % { 'virtualenv': env.virtualenv, 'current_release': env.current_release, 'app_name': env.app_name, 'settings': env.settings })


def migrations():
    """Deploy and run pending migrations"""
    update_code()
    syncdb()
    migrate()
    collectstatic()
    symlink()
    reload()


def rollback_code():
    """Rolls back to the previously deployed version"""
    releases()
    if len(env.releases) >= 2:
        env.current_release = env.releases[-1]
        env.previous_revision = env.releases[-2]
        env.current_release = "%(releases_path)s/%(current_revision)s" % { 'releases_path': env.releases_path, 'current_revision': env.current_revision }
        env.previous_release = "%(releases_path)s/%(previous_revision)s" % { 'releases_path': env.releases_path, 'previous_revision': env.previous_revision }
        run("rm %(current_path)s; ln -s %(previous_release)s %(current_path)s && rm -rf %(current_release)s" % { 'current_release': env.current_release, 'previous_release': env.previous_release, 'current_path': env.current_path })


def rollback():
    """Rolls back to a previous version and restarts"""
    rollback_code()
    reload()


def cleanup():
    """Clean up old releases"""
    if not env.has_key('releases'):
        releases()
    if len(env.releases) > 3:
        directories = env.releases
        directories.reverse()
        del directories[:3]
        env.directories = ' '.join([ "%(releases_path)s/%(release)s" % { 'releases_path': env.releases_path, 'release': release } for release in directories ])
        run("rm -rf %(directories)s" % { 'directories': env.directories })


def deploy():
    """Deploys your project. This calls both 'update' and 'restart'"""
    update_code()
    collectstatic()
    symlink()
    reload()


def start():
    """Start the application servers"""
    sudo("/etc/init.d/nginx start")
    sudo("/etc/init.d/%(uwsgi_init_file)s start" % { 'uwsgi_init_file': env.uwsgi_init_file })


def restart():
    """Restarts your application"""
    sudo("/etc/init.d/%(uwsgi_init_file)s restart" % { 'uwsgi_init_file': env.uwsgi_init_file })


def reload():
    """reload your application"""
    sudo("/etc/init.d/%(uwsgi_init_file)s reload" % { 'uwsgi_init_file': env.uwsgi_init_file })


def stop():
    """Stop the application servers"""
    sudo("/etc/init.d/%(uwsgi_init_file)s stop" % { 'uwsgi_init_file': env.uwsgi_init_file })
