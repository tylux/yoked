import os
import unittest
import json

from flask import Flask
#from flask.ext.testing import TestCase

from api import app, db
from api import User, Group, Instance, Shell, Access, Role


class apiTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Shell(self):
        tmpzsh = Shell(name='zsh', path='/usr/bin/zsh')
        db.session.add(tmpzsh)
        db.session.commit()
        tmpbash = Shell(name='bash', path='/bin/bash')
        db.session.add(tmpbash)
        db.session.commit()
        # Check to make sure that worked
        zsh = Shell.query.filter_by(name='zsh').first()
        assert zsh.path == '/usr/bin/zsh'
        bash = Shell.query.filter_by(name='bash').first()
        assert bash.path == '/bin/bash'

    def test_Access(self):
        tmpAdmin = Access(name='admin', description='Grant SuperUser privileges on host')
        db.session.add(tmpAdmin)
        db.session.commit()
        tmpUser = Access(name='user', description='Normal User Access to host')
        db.session.add(tmpUser)
        db.session.commit()
        isadmin = Access.query.filter_by(name='admin').first()
        isuser = Access.query.filter_by(name='user').first()
        assert isadmin.name == 'admin'
        assert isuser.name == 'user'

    def test_Group(self):
        tmpGroup = Group(name='WebServers')
        db.session.add(tmpGroup)
        db.session.commit()
        group = Group.query.filter_by(name='WebServers').first()
        assert group.name == 'WebServers'
        resp = self.app.get('/v1/groups', headers={'Content-Type': "application/json"})
        #groups = {"id": 1, "name": "Webservers", "users": []}
        #validresp = dict({"groups": [groups]})
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()