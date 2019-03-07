#!/usr/bin/env python
"""
Idea and code snippets borrowed from http://www.xhtml.net/scripts/Django-CherryPy-server-DjangoCerise
Adapted to run as a management command
switched to standalone
"""

import logging, sys, os, signal, time, errno
import json
from socket import gethostname

import django.contrib.admin
from django.core.management.base import BaseCommand
from django.core.handlers.wsgi import WSGIHandler
from django.conf import settings

from wsgiserver import mediahandler

error_logger = logging.getLogger('spl.django.error')

CPWSGI_HELP = r"""
  Run this project in CherryPy's production quality http webserver.
  Note that it's called wsgiserver but it is actually a complete http server.

    runwsgiserver [options] [cpwsgi settings] [stop]

Optional CherryPy server settings: (setting=value)
  host=HOSTNAME         hostname to listen on
                        Defaults to 127.0.0.1,
                        (set to 0.0.0.0 to bind all ip4 interfaces or :: for
                        all ip6 interfaces)
  port=PORTNUM          port to listen on
                        Defaults to 8000
  server_name=STRING    CherryPy's SERVER_NAME environ entry
                        Defaults to localhost
  daemonize=BOOL        whether to detach from terminal
                        Defaults to False
  pidfile=FILE          write the spawned process-id to this file
  workdir=DIRECTORY     change to this directory when daemonizing
  threads=NUMBER        Number of threads for server to use
  ssl_certificate=FILE  SSL certificate file
  ssl_private_key=FILE  SSL private key file
  server_user=STRING    user to run daemonized process
                        Defaults to www-data
  server_group=STRING   group to daemonized process
                        Defaults to www-data
  adminserve=True|False  Serve the django admin media automatically. Useful
                         in development. Defaults to True so turn to False
                         if  using in production.

Examples:
  Run a "standard" CherryPy wsgi server
    $ manage.py runwsgiserver

  Run a CherryPy server on port 80
    $ manage.py runwsgiserver port=80

  Run a CherryPy server as a daemon and write the spawned PID in a file
    $ manage.py runwsgiserver daemonize=true pidfile=/var/run/django-cpwsgi.pid
  
  Run a CherryPy server using ssl with test certificates located in /tmp
    $ manage.py runwsgiserver ssl_certificate=/tmp/testserver.crt ssl_private_key=/tmp/testserver.key

"""

CPWSGI_OPTIONS = {
'host': '127.0.0.1', # changed from localhost to avoid ip6 problem -clm
'server_name': 'localhost',
'threads': 10, 
'daemonize': False,
'workdir': None,
'pidfile': None,
'server_user': 'www-data',
'server_group': 'www-data',
'ssl_certificate': None,
'ssl_private_key': None,
'autoreload' : False,
'adminserve' : False,  # please serve the admin media too by default
}

class Command(BaseCommand):
    help = "CherryPy Server for project. Requires CherryPy."
    args = "[various KEY=val options, use `runwsgiserver help` for help]"

    def handle(self, *args, **options):
        from django.conf import settings
        from django.utils import translation
        # Activate the current language, because it won't get activated later.
        try:
            translation.activate(settings.LANGUAGE_CODE)
        except AttributeError:
            pass
        runwsgiserver(args)
        
    def usage(self, subcommand):
        return CPWSGI_HELP

def change_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    Src: http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/
    """
    if not os.geteuid() == 0:
        # Do not try to change the gid/uid if not root.
        return
    (uid, gid) = get_uid_gid(uid, gid)
    os.setgid(gid)
    os.setuid(uid)

def get_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    Src: http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/
    """
    import pwd, grp
    uid, default_grp = pwd.getpwnam(uid)[2:4]
    if gid is None:
        gid = default_grp
    else:
        try:
            gid = grp.getgrnam(gid)[2]            
        except KeyError:
            gid = default_grp
    return (uid, gid)
    
    
def poll_process(pid):
    """
    Poll for process with given pid up to 10 times waiting .25 seconds in between each poll. 
    Returns False if the process no longer exists otherwise, True.
    """
    for n in range(10):
        time.sleep(0.25)
        try:
            # poll the process state
            os.kill(pid, 0)
        except OSError, e:
            if e[0] == errno.ESRCH:
                # process has died
                return False
            else:
                raise Exception
    return True

def stop_server(pidfile):
    """
    Stop process whose pid was written to supplied pidfile. 
    First try SIGTERM and if it fails, SIGKILL. If process is still running, an exception is raised.
    """
    if os.path.exists(pidfile):
        pid = int(open(pidfile).read())
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError: #process does not exist
            os.remove(pidfile)
            return
        if poll_process(pid):
            #process didn't exit cleanly, make one last effort to kill it
            os.kill(pid, signal.SIGKILL)
            #if still_alive(pid):
            if poll_process(pid):
                raise OSError, "Process %s did not stop."
        os.remove(pidfile)

class LoggingWSGIHandler(WSGIHandler):
    def handle_uncaught_exception(self, request, resolver, exc_info, *args, **kwargs):
        """
        Processing for any otherwise uncaught exceptions (those that will
        generate HTTP 500 responses). Can be overridden by subclasses who want
        customised 500 handling.

        Be *very* careful when overriding this because the error could be
        caused by anything, so assuming something like the database is always
        available would be an error.
        """

        # We delegate all behavior to our super class. We only use this override
        # to add our own logging.
        error_logger.error('Internal Server Error: %s', request.path,
            exc_info=exc_info,
            extra={
                'status_code': 500,
                'request': request
            }
        )
        
        return super(LoggingWSGIHandler, self).handle_uncaught_exception(request, resolver, exc_info, *args, **kwargs)            


def start_server_servestatic(*args, **options):
    """
    Start CherryPy server AND serve default static files

    Want SSL support?
    a. The new (3.1 or 3.2) way: Just set server.ssl_adapter to an SSLAdapter 
       instance.

    b. The old way (deprecated way) is to set these attributes:

       server.ssl_certificate = <filename>
       server.ssl_private_key = <filename>

       But this is the only way from the management command line
       in the future I may need to adapt this to use a server.ssl_adapter
    """
    
    options['mount'] = '/' + settings.MOUNT
    splunkdj_port = settings.DJANGO_PORT
    options['port'] = int(options.get('port', splunkdj_port))

    print 'starting server with options: %s' % json.dumps(options, sort_keys=True, indent=2)
    
    if options['daemonize'] and options['server_user'] and options['server_group']:
        #ensure the that the daemon runs as specified user
        change_uid_gid(options['server_user'], options['server_group'])
    
    from wsgiserver.server import CherryPyWSGIServer, WSGIPathInfoDispatcher

    app = LoggingWSGIHandler()
    
    if options['adminserve']: # serve the admin media too
        # AdminMediaHandler is middleware for local use
        import django.core.servers.basehttp
        app = django.core.servers.basehttp.AdminMediaHandler(app)
    # another way to serve the admin media three application
    path = { 
        options['mount']: app,
        settings.STATIC_URL: mediahandler.MediaHandler(settings.STATIC_ROOT),
    }
    dispatcher =  WSGIPathInfoDispatcher(path)
        
    server = CherryPyWSGIServer(
        (options['host'], int(options['port'])),
        dispatcher,
        int(options['threads']), 
        options['server_name']
    )
    if options['ssl_certificate'] and options['ssl_private_key']:
        server.ssl_certificate = options['ssl_certificate']
        server.ssl_private_key = options['ssl_private_key']  
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

def runwsgiserver(argset=[], **kwargs):
    # Get the options
    options = CPWSGI_OPTIONS.copy()
    options.update(kwargs)
    for x in argset:
        if "=" in x:
            k, v = x.split('=', 1)
        else:
            k, v = x, True
        if v=='False' or v=='false':
            v = False
            # print "found false", v
        options[k.lower()] = v
        
    if "help" in options:
        print CPWSGI_HELP
        return
        
    if "stop" in options:
        stop_server(options['pidfile'])
        return True
    
    if options['daemonize']:
        if not options['pidfile']:
            options['pidfile'] = '/var/run/cpwsgi_%s.pid' % options['port']
        stop_server(options['pidfile'])     
       
        from django.utils.daemonize import become_daemon
        if options['workdir']:
            become_daemon(our_home_dir=options['workdir'])
        else:
            become_daemon()

        fp = open(options['pidfile'], 'w')
        fp.write("%d\n" % os.getpid())
        fp.close()
    if options['autoreload']:
        from django.utils import autoreload
    
    # Start the webserver
    if options['autoreload']:
        autoreload.main(start_server_servestatic, (), options)
    else:
        start_server_servestatic(options)

if __name__ == '__main__':
    runwsgiserver(sys.argv[1:])
