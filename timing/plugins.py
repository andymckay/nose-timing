from functools import wraps
from inspect import ismodule
import inspect
import json
import logging
import os
import time

NOSE = False
try:
    from nose.plugins.base import Plugin
    NOSE = True
except ImportError:
    class Plugin:
        pass

log = logging.getLogger(__name__)


class NoseTiming(Plugin):
    name = 'timing'

    def options(self, parser, env=os.environ):
        super(NoseTiming, self).options(parser, env=env)

        parser.add_option('--output-directory',
                          action='store',
                          default='.',
                          dest='destination',
                          help=('Where to write JSON files'))


    def configure(self, options, conf):
        super(NoseTiming, self).configure(options, conf)
        if not self.enabled:
            return

        self.destination = options.destination

        self._timed_tests = {}
        self._timed_setup_start = {}
        self._timed_setup_elapsed = {}

    @staticmethod
    def name_for_obj(i):
        if ismodule(i):
            return i.__name__
        else:
            return "%s.%s" % (i.__module__, i.__name__)

    def report(self, stream):
        out = [(self._timed_setup_elapsed, 'setup.json'),
               (self._timed_tests, 'tests.json')]

        for data, filename in out:
            dest = os.path.join(os.path.abspath(self.destination), filename)
            stream.writeln('Writing to %s' % dest)
            json.dump(data, open(dest, 'w'))

    def record_elapsed_decorator(self, f, ctx, key_name):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time.time()

            try:
                return f(*args, **kwargs)
            finally:
                ctx[key_name] = time.time() - start_time

        return wrapped

    def startContext(self, context):
        ctx_name = self.name_for_obj(context)
        self._timed_setup_elapsed[ctx_name] = ctx = {'total': 0, 'setUp': 0,
                                                     'tearDown': 0,
                                                     'file': self.file(context)}

        if hasattr(context, 'setUp'):
            for k in ('setUp', 'tearDown'):
                old_f = getattr(context, k)
                new_f = self.record_elapsed_decorator(old_f, ctx, k)
                setattr(context, k, new_f)

        self._timed_setup_start[context] = time.time()

    def stopContext(self, context):
        end_time = time.time()

        elapsed = end_time - self._timed_setup_start.pop(context)
        ctx_name = self.name_for_obj(context)
        self._timed_setup_elapsed[ctx_name]['total'] = elapsed

    def _timeTaken(self):
        if hasattr(self, '_timer'):
            taken = time.time() - self._timer
        else:
            # test died before it ran (probably error in setup())
            # or success/failure added before test started probably
            # due to custom TestResult munging
            taken = 0.0
        return taken

    def file(self, context):
        try:
            return {'name': os.path.abspath(inspect.getsourcefile(context)),
                    'line': inspect.getsourcelines(context)[-1]}
        except (TypeError, IOError):
            return {}

    def startTest(self, test):
        self._timer = time.time()

    def _register_time(self, test):
        self._timed_tests[test.id()] = {'total': self._timeTaken(),
                                        'file': self.file(test.context)}

    def addError(self, test, err, capt=None):
        self._register_time(test)

    def addFailure(self, test, err, capt=None, tb_info=None):
        self._register_time(test)

    def addSuccess(self, test, capt=None):
        self._register_time(test)

