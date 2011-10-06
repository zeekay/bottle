''' Test module for the Bottle class and its methods MINUS the WSGI part. See
    test_wsgi for WSGI compatibility tests.
'''

import unittest
from bottle import Bottle, default_app

# Minimal route callback
def cb(): return 'OK'

class TestRouteGroups(unittest.TestCase):
    ''' The Bottle.group() context manager. '''

    def test_default_path_and_method(self):
        app = Bottle()
        with app.group(path='/test', method='ANY'):
            app.route(callback=cb)
        self.assertEqual(app.routes[-1].rule, '/test')
        self.assertEqual(app.routes[-1].method, 'ANY')
        app.route(callback=cb)
        self.assertEqual(app.routes[-1].rule, '/cb')
        self.assertEqual(app.routes[-1].method, 'GET')

    def test_default_config(self):
        app = Bottle()
        with app.group(foo='bar'):
            app.route('/foo', callback=cb)
        self.assertEqual(app.routes[-1].rule, '/foo')
        self.assertEqual(app.routes[-1].config.foo, 'bar')
        app.route('/bar', callback=cb)
        self.assertEqual(app.routes[-1].rule, '/bar')
        self.assertTrue('foo' not in app.routes[-1].config)

    def test_nesting(self):
        app = Bottle()
        with app.group(a=1, b=1):
            with app.group(b=2, c=2):
                app.route('/foo', callback=cb)
        self.assertEqual(app.routes[-1].config.a, 1)
        self.assertEqual(app.routes[-1].config.b, 2)
        self.assertEqual(app.routes[-1].config.c, 2)

    def test_default_app(self):
        app = Bottle()
        self.assertNotEqual(app, default_app())
        with app.group():
            self.assertEqual(app, default_app())
        self.assertNotEqual(app, default_app())


   
if __name__ == '__main__': #pragma: no cover
    unittest.main()

