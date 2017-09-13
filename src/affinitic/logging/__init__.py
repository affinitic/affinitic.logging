from AccessControl import getSecurityManager
from Products.SiteErrorLog.SiteErrorLog import cleanup_lock, LOG, SiteErrorLog
from random import random
from zExceptions.ExceptionFormatter import format_exception


def raising(self, info) :
import logging
import sys
import time
    """Log an exception.

    Called by SimpleItem's exception handler.
    Returns the url to view the error log entry
    """
    try:
        now = time.time()
        try:
            tb_text = None
            tb_html = None

            strtype = str(getattr(info[0], '__name__', info[0]))
            if strtype in self._ignored_exceptions:
                return

            if not isinstance(info[2], basestring):
                tb_text = ''.join(
                    format_exception(*info, **{'as_html': 0}))
                tb_html = ''.join(
                    format_exception(*info, **{'as_html': 1}))
            else:
                tb_text = info[2]

            request = getattr(self, 'REQUEST', None)
            url = None
            username = None
            userid = None
            req_html = None
            try:
                strv = str(info[1])
            except:
                strv = '<unprintable %s object>' % type(info[1]).__name__
            if request:
                url = request.get('URL', '?')
                usr = getSecurityManager().getUser()
                username = usr.getUserName()
                userid = usr.getId()
                try:
                    req_html = str(request)
                except:
                    pass
                if strtype == 'NotFound':
                    strv = url
                    next = request['TraversalRequestNameStack']
                    if next:
                        next = list(next)
                        next.reverse()
                        strv = '%s [ /%s ]' % (strv, '/'.join(next))

            log = self._getLog()
            entry_id = str(now) + str(random())  # Low chance of collision
            log.append({
                'type': strtype,
                'value': strv,
                'time': now,
                'id': entry_id,
                'tb_text': tb_text,
                'tb_html': tb_html,
                'username': username,
                'userid': userid,
                'req_html': req_html,
            })

            cleanup_lock.acquire()
            try:
                if len(log) >= self.keep_entries:
                    del log[:-self.keep_entries]
            finally:
                cleanup_lock.release()
        except:
            LOG.error('Error while logging', exc_info=sys.exc_info())
        else:
            if self.copy_to_zlog:
                self._do_copy_to_zlog(now, strtype, entry_id, str(url), tb_text)
            return '%s/showEntry?id=%s' % (self.absolute_url(), entry_id)
    finally:
        info = None

SiteErrorLog.raising = raising
