from unittest import TestCase
from crawler import *

class TestParse_options(TestCase):

    # pass an URL as an argument or use option -u
    def test_parse_no_args(self):
        opts, args = parse_options([])
        self.assertFalse(opts or args)

    def test_parse_urlfile_pass(self):
        opts, args = parse_options(['-u', 'urlfile'])
        self.assertEqual(opts.urlfile, 'urlfile')

    def test_parse_urlfile_fail(self):
        opts, args = parse_options(['-u'])
        self.assertFalse(opts or args)

    def test_parse_urlfile_long_pass(self):
        opts, args = parse_options(['--urlfile', 'urlfile'])
        self.assertEqual(opts.urlfile, 'urlfile')

    def test_parse_urlfile_long_fail(self):
        opts, args = parse_options(['--urlfile'])
        self.assertFalse(opts or args)

    def test_parse_csvfile_pass(self):
        opts, args = parse_options(['-c', 'csvfile', 'http://www.example.com/'])
        self.assertEqual(opts.csvfile, 'csvfile')

    def test_parse_csvfile_fail(self):
        opts, args = parse_options(['-c'])
        self.assertFalse(opts or args)

    def test_parse_csvfile_long_pass(self):
        opts, args = parse_options(['--csvfile', 'csvfile', 'http://www.example.com/'])
        self.assertEqual(opts.csvfile, 'csvfile')

    def test_parse_csvfile_long_fail(self):
        opts, args = parse_options(['--csvfile'])
        self.assertFalse(opts or args)

    def test_parse_dbuser_pass(self):
        opts, args = parse_options(['-U', 'dbuser', 'http://www.example.com/'])
        self.assertEqual(opts.dbuser, 'dbuser')

    def test_parse_dbuser_fail(self):
        opts, args = parse_options(['-U'])
        self.assertFalse(opts or args)

    def test_parse_dbuser_long_pass(self):
        opts, args = parse_options(['--dbuser', 'dbuser', 'http://www.example.com/'])
        self.assertEqual(opts.dbuser, 'dbuser')

    def test_parse_dbuser_long_fail(self):
        opts, args = parse_options(['--dbuser'])
        self.assertFalse(opts or args)

    def test_parse_dbpass_pass(self):
        opts, args = parse_options(['-p', 'dbpass', 'http://www.example.com/'])
        self.assertEqual(opts.dbpass, 'dbpass')

    def test_parse_dbpass_fail(self):
        opts, args = parse_options(['-p'])
        self.assertFalse(opts or args)

    def test_parse_dbpass_long_pass(self):
        opts, args = parse_options(['--dbpass', 'dbpass', 'http://www.example.com/'])
        self.assertEqual(opts.dbpass, 'dbpass')

    def test_parse_dbpass_long_fail(self):
        opts, args = parse_options(['--dbpass'])
        self.assertFalse(opts or args)

    def test_parse_dbhost_pass(self):
        opts, args = parse_options(['-H', 'dbhost', 'http://www.example.com/'])
        self.assertEqual(opts.dbhost, 'dbhost')

    def test_parse_dbhost_fail(self):
        opts, args = parse_options(['-H'])
        self.assertFalse(opts or args)

    def test_parse_dbhost_long_pass(self):
        opts, args = parse_options(['--dbhost', 'dbhost', 'http://www.example.com/'])
        self.assertEqual(opts.dbhost, 'dbhost')

    def test_parse_dbhost_long_fail(self):
        opts, args = parse_options(['--dbhost'])
        self.assertFalse(opts or args)

    def test_parse_dbschema_pass(self):
        opts, args = parse_options(['-s', 'dbschema', 'http://www.example.com/'])
        self.assertEqual(opts.dbschema, 'dbschema')

    def test_parse_dbschema_fail(self):
        opts, args = parse_options(['-s'])
        self.assertFalse(opts or args)

    def test_parse_dbschema_long_pass(self):
        opts, args = parse_options(['--dbschema', 'dbschema', 'http://www.example.com/'])
        self.assertEqual(opts.dbschema, 'dbschema')

    def test_parse_dbschema_long_fail(self):
        opts, args = parse_options(['--dbschema'])
        self.assertFalse(opts or args)

    def test_parse_dbport_pass(self):
        opts, args = parse_options(['-P', 'dbport', 'http://www.example.com/'])
        self.assertEqual(opts.dbport, 'dbport')

    def test_parse_dbport_fail(self):
        opts, args = parse_options(['-P'])
        self.assertFalse(opts or args)

    def test_parse_dbport_long_pass(self):
        opts, args = parse_options(['--dbport', 'dbport', 'http://www.example.com/'])
        self.assertEqual(opts.dbport, 'dbport')

    def test_parse_dbport_long_fail(self):
        opts, args = parse_options(['--dbport'])
        self.assertFalse(opts or args)

    def test_parse_depth_pass(self):
        opts, args = parse_options(['-d', '10', 'http://www.example.com/'])
        self.assertEqual(opts.depth, 10)

    def test_parse_depth_fail(self):
        opts, args = parse_options(['-d'])
        self.assertFalse(opts or args)

    def test_parse_depth_long_pass(self):
        opts, args = parse_options(['--depth', '10', 'http://www.example.com/'])
        self.assertEqual(opts.depth, 10)

    def test_parse_depth_long_fail(self):
        opts, args = parse_options(['--depth'])
        self.assertFalse(opts or args)

    def test_parse_resume_pass(self):
        opts, args = parse_options(['-r'])
        self.assertTrue(opts.resume)

    # option -r cannot be used with an argument
    def test_parse_resume_args_fail(self):
        opts, args = parse_options(['-r', 'http://www.example.com/'])
        self.assertFalse(opts or args)

    # option -r cannot be used with option -u
    def test_parse_resume_urlfile_fail(self):
        opts, args = parse_options(['-r', '-u', 'urlfile'])
        self.assertFalse(opts or args)

    def test_parse_resume_long_pass(self):
        opts, args = parse_options(['--resume'])
        self.assertTrue(opts.resume)

    # option -r cannot be used with an argument
    def test_parse_resume_long_args_fail(self):
        opts, args = parse_options(['--resume', 'http://www.example.com/'])
        self.assertFalse(opts or args)

    # option -r cannot be used with option -u
    def test_parse_resume_long_urlfile_fail(self):
        opts, args = parse_options(['--resume', '-u', 'urlfile'])
        self.assertFalse(opts or args)

    def test_parse_cluster_pass(self):
        opts, args = parse_options(['-j', '5', 'http://www.example.com/'])
        self.assertEqual(opts.cluster_jobs, 5)

    def test_parse_cluster_fail(self):
        opts, args = parse_options(['-j'])
        self.assertFalse(opts or args)

    def test_parse_cluster_long_pass(self):
        opts, args = parse_options(['--cluster-jobs', '5', 'http://www.example.com/'])
        self.assertEqual(opts.cluster_jobs, 5)

    def test_parse_cluster_long_fail(self):
        opts, args = parse_options(['--cluster-jobs'])
        self.assertFalse(opts or args)
