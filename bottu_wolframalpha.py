# -*- coding: utf-8 -*-
from StringIO import StringIO
import urllib
import re
from twisted.python import log
from twisted.web.client import getPage
from wolframalpha import Result


pattern = re.compile(r'^[^\w]*')


def query(env, question):
    def callback(data):
        result = Result(StringIO(data))
        for pod in result.pods:
            if pod.id == 'Result':
                env.msg("%s, the answer seems to be: %s" % (env.user.name, pod.text))
                return
        env.msg("%s, couldn't find an answer, sorry!" % env.user.name)

    def errback(failure):
        log.err(failure)
        env.msg("%s, there was an error looking for an answer, sorry!" % env.user.name)
    query = urllib.urlencode(dict(
        input=question,
        appid=env.plugin.app_id,
    ))
    url = 'http://api.wolframalpha.com/v2/query?' + query
    deferred = getPage(url)
    deferred.addCallback(callback).addErrback(errback)

def message(env, message):
    log.msg("%r %r %r" % (message.lower(), env.app.name.lower(), message.lower().startswith(env.app.name.lower())))
    if message.lower().startswith(env.app.name.lower()):
        rest = pattern.sub('', message[len(env.app.name):])
        query(env, rest)
        env.msg("%s, let me look that up" % env.user.name)

def register(app, conf):
    plugin = app.add_plugin('WolframAlpha')
    plugin.app_id = conf.get('app-id', None)
    if plugin.app_id:
        plugin.bind_event('message', message)
    else:
        log.msg("No app-id specified")
