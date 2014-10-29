from os.path import join, realpath, dirname
from unittest import TestCase

from py_look_for_timeouts.main import check, Checker


SAMPLE_PATH = realpath(join(dirname(__file__), 'samples'))


class TestSimple(TestCase):
    def test_good_file(self):
        errors = check(join(SAMPLE_PATH, 'good.py'))
        self.assertEqual(errors, [])

    def test_bad_urllib_urlopen(self):
        errors = check(join(SAMPLE_PATH, 'bad_script.py'))
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[0].lineno, 3)
        self.assertEqual(errors[0].reason, 'urlopen call without a timeout arg or kwarg')
        self.assertEqual(errors[1].lineno, 4)
        self.assertEqual(errors[1].reason, 'urlopen call with a timeout kwarg of 0')
        self.assertEqual(errors[2].lineno, 6)
        self.assertEqual(errors[2].reason, 'urlopen call with a timeout arg of 0')

    def test_bad_bare_urlopen(self):
        errors = check(join(SAMPLE_PATH, 'bad_script_2.py'))
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[0].lineno, 3)
        self.assertEqual(errors[0].reason, 'urlopen call without a timeout arg or kwarg')
        self.assertEqual(errors[1].lineno, 4)
        self.assertEqual(errors[1].reason, 'urlopen call with a timeout kwarg of 0')
        self.assertEqual(errors[2].lineno, 6)
        self.assertEqual(errors[2].reason, 'urlopen call with a timeout arg of 0')

    def test_bad_httpconnection(self):
        errors = check(join(SAMPLE_PATH, 'bad_httpconnection.py'))
        self.assertEqual(len(errors), 6)
        self.assertEqual(errors[0].reason, 'httplib connection without a timeout arg or kwarg')
        self.assertEqual(errors[2].reason, 'httplib connection with a timeout kwarg of 0')
        self.assertEqual(errors[5].reason, 'httplib connection with a timeout arg of 0')

    def test_bad_twilio_connection(self):
        errors = check(join(SAMPLE_PATH, 'bad_twilio_connection.py'))
        self.assertEqual(len(errors), 6)
        self.assertEqual(errors[0].reason, 'twilio rest connection without a timeout arg or kwarg')
        self.assertEqual(errors[2].reason, 'twilio rest connection with a timeout kwarg of 0')
        self.assertEqual(errors[5].reason, 'twilio rest connection with a timeout arg of 0')

    def test_bad_requests_call(self):
        errors = check(join(SAMPLE_PATH, 'bad_requests.py'))
        self.assertEqual(len(errors), 5)

    def test_hardcoded_timeout(self):
        """Verify that hardcoded timeouts are identified."""
        checker = Checker(allow_hardcoded=False)
        errors = check(join(SAMPLE_PATH, 'bad_hardcoded.py'), checker=checker)
        self.assertEqual(len(errors), 1)
        error = errors[0]
        self.assertEqual(error.lineno, 3)
        self.assertEqual(error.reason, 'urlopen call with an hardcoded timeout arg of 2')
