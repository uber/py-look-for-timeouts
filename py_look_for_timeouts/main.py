#!/usr/bin/env python

import argparse
import ast

from . import __version__


class IllegalLine(object):
    def __init__(self, reason, node, filename):
        self.reason = reason
        self.lineno = node.lineno
        self.filename = filename
        self.node = node

    def __str__(self):
        return "%s:%d\t%s" % (self.filename, self.lineno, self.reason)

    def __repr__(self):
        return "IllegalLine<%s, %s:%s>" % (
            self.reason,
            self.filename,
            self.lineno
        )


def _intify(something):
    if isinstance(something, ast.Num):
        return something.n
    else:
        # we aren't going to evaluate anything else, so, uh
        # assume it was okay
        return None


def _stringify(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return '%s.%s' % (_stringify(node.value), node.attr)
    elif isinstance(node, ast.Subscript):
        return '%s[%s]' % (_stringify(node.value), _stringify(node.slice))
    elif isinstance(node, ast.Index):
        return _stringify(node.value)
    elif isinstance(node, ast.Call):
        return '%s(%s, %s)' % (
            _stringify(node.func),
            _stringify(node.args),
            _stringify(node.keywords)
        )
    elif isinstance(node, list):
        return '[%s]' % (', '.join(_stringify(n) for n in node))
    elif isinstance(node, ast.Str):
        return node.s
    else:
        return ast.dump(node)


class Visitor(ast.NodeVisitor):
    def __init__(self, filename, checker, *args, **kwargs):
        self.filename = filename
        self.checker = checker
        self.errors = []
        super(Visitor, self).__init__(*args, **kwargs)

    @staticmethod
    def _is_urlopen_call(function_name):
        if '.' in function_name:
            if function_name in ('urllib.urlopen', 'urllib2.urlopen'):
                return True
        else:
            if function_name == 'urlopen':
                return True
        return False

    @staticmethod
    def _is_httplib_call(function_name):
        if '.' in function_name:
            if function_name in (
                'httplib.HTTPConnection',
                'httplib.HTTPSConnection'
            ):
                return True
        else:
            if function_name in ('HTTPConnection', 'HTTPSConnection'):
                return True
        return False

    @staticmethod
    def _is_twilio_call(function_name):
        if '.' in function_name:
            if function_name.endswith('rest.TwilioRestClient'):
                return True
        elif function_name == 'TwilioRestClient':
            return True
        return False

    @staticmethod
    def _is_requests_call(function_name):
        if function_name in (
            'requests.get',
            'requests.post',
            'requests.put',
            'requests.head',
            'requests.request',
        ):
            return True
        return False

    def _check_timeout_call(self, node, arg_offset, kwarg_name, desc):
        # Grab the timeout node inside the function call
        timeout = None
        is_kwarg = False
        if arg_offset is not None and len(node.args) > arg_offset:
            timeout = node.args[arg_offset]
        elif node.keywords:
            keywords = [k for k in node.keywords if k.arg == kwarg_name]
            if keywords:
                is_kwarg = True
                timeout = keywords[0].value
        errors = self.checker(timeout, desc, node, self.filename, is_kwarg)
        if errors:
            self.errors.extend(errors)

    def visit_Call(self, node):
        function_name = _stringify(node.func)
        if self._is_urlopen_call(function_name):
            self._check_timeout_call(
                node,
                arg_offset=2,
                kwarg_name='timeout',
                desc='urlopen call'
            )
        elif self._is_httplib_call(function_name):
            self._check_timeout_call(
                node,
                arg_offset=5,
                kwarg_name='timeout',
                desc='httplib connection'
            )
        elif self._is_twilio_call(function_name):
            self._check_timeout_call(
                node,
                arg_offset=5,
                kwarg_name='timeout',
                desc='twilio rest connection'
            )
        elif self._is_requests_call(function_name):
            self._check_timeout_call(
                node,
                arg_offset=None,
                kwarg_name='timeout',
                desc='requests call'
            )


class Checker(object):

    def __init__(self, allow_hardcoded=True):
        self.allow_hardcoded = allow_hardcoded

    def __call__(self, timeout_node, desc, node, filename, is_kwarg):
        """Return a list of IllegalLine on misconfigured timeout.

        :param timeout_node:
        :param desc:
        :param node:
        :param str filename:
        """
        msg = None
        if not timeout_node:
            msg = '%s without a timeout arg or kwarg' % desc
            return [IllegalLine(msg, node, filename)]

        value = _intify(timeout_node)
        if value == 0:
            msg = '%s with a timeout %sarg of 0' % (
                desc, 'kw' if is_kwarg else '')
        elif isinstance(value, int) and not self.allow_hardcoded:
            msg = '%s with an hardcoded timeout arg of %d' % (desc, value)

        if msg:
            return [IllegalLine(msg, node, filename)]


def check(filename, checker=None):
    """Check a file for missing/misconfigure timeouts."""
    if not checker:
        checker = Checker()

    v = Visitor(filename, checker=checker)
    with open(filename, 'r') as fobj:
        try:
            parsed = ast.parse(fobj.read(), filename)
            v.visit(parsed)
        except Exception:  # noqa
            raise  # noqa
    return v.errors


def main():
    parser = argparse.ArgumentParser(
        description='Look for python source files missing timeouts',
        epilog=('Exit status is 0 if all files are okay, 1 if any files '
                'have an error. Errors are printed to stdout')
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + __version__
    )
    parser.add_argument(
        '--no-hardcoded',
        action='store_true',
        help="Do not allow hardcoded constant"
    )
    parser.add_argument('files', nargs='+', help='Files to check')
    args = parser.parse_args()

    errors = []
    checker = Checker(allow_hardcoded=not args.no_hardcoded)
    for fname in args.files:
        these_errors = check(fname, checker=checker)
        if these_errors:
            print '\n'.join(str(e) for e in these_errors)
            errors.extend(these_errors)
    if errors:
        print '%d total errors' % len(errors)
        return 1
    else:
        return 0


if __name__ == '__main__':
    main()
