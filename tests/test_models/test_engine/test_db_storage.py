#!/usr/bin/python3
"""module for DBstorage tests"""
import unittest
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'db_storage test not supported')
class TestDBStorage(unittest.TestCase):
    """test dbstorage"""
    def test_new_and_save(self):
        """test  new & save methods"""
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'john',
                           'last_name': 'Aroma',
                           'email': 'john94@gmail.com',
                           'password': 6789})
        curs = db.cursor()
        curs.execute('SELECT COUNT(*) FROM users')
        old_count = curs.fetchall()
        curs.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        curs = db.cursor()
        curs.execute('SELECT COUNT(*) FROM users')
        new_count = curs.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)
        curs.close()
        db.close()

    def test_new(self):
        """ test object added """
        new = User(
            email='john94@gmail.com',
            password='password',
            first_name='John',
            last_name='Aramco'
        )
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        curs = dbc.cursor()
        curs.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = curs.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('john94@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('John', result)
        self.assertIn('Aramco', result)
        curs.close()
        dbc.close()

    def test_delete(self):
        """ test deleted object """
        new = User(
            email='john94@gmail.com',
            password='password',
            first_name='John',
            last_name='Aramco'
        )
        obj_key = 'User.{}'.format(new.id)
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        new.save()
        self.assertTrue(new in storage.all().values())
        curs = dbc.cursor()
        curs.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = curs.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('john94@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('John', result)
        self.assertIn('Aramco', result)
        self.assertIn(obj_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())
        curs.close()
        dbc.close()

    def test_reload(self):
        """ test reload session """
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        curs = dbc.cursor()
        curs.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                'u-n12',
                str(datetime.now()),
                str(datetime.now()),
                'john94@yahoo.com',
                'pass',
                'Aramco',
                'john',
            ]
        )
        self.assertNotIn('User.u-n12', storage.all())
        dbc.commit()
        storage.reload()
        self.assertIn('User.u-n12', storage.all())
        curs.close()
        dbc.close()

    def test_save(self):
        """ test object save """
        new = User(
            email='john94@gmail.com',
            password='password',
            first_name='John',
            last_name='Aramco'
        )
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        curs = dbc.cursor()
        curs.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        curs.execute('SELECT COUNT(*) FROM users;')
        old_cnt = curs.fetchone()[0]
        self.assertTrue(result is None)
        self.assertFalse(new in storage.all().values())
        new.save()
        dbc2 = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor2 = dbc2.cursor()
        cursor2.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor2.fetchone()
        cursor2.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cursor2.fetchone()[0]
        self.assertFalse(result is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new in storage.all().values())
        cursor2.close()
        dbc2.close()
        curs.close()
        dbc.close()
