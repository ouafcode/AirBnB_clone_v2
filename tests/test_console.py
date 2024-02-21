#!/usr/bin/python3
"""A unit test for the console.
"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clr_stream


class TestHBNBCommand(unittest.TestCase):
    """for test class of the HBNBCommand.
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fst_create(self):
        """Tests with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            const = HBNBCommand()
            const.onecmd('create Place name="CASA"')
            dl_id = cout.getvalue().strip()
            clr_stream(cout)
            self.assertIn('Place.{}'.format(dl_id), storage.all().keys())
            const.onecmd('show Place {}'.format(dl_id))
            self.assertIn("'name': 'CASA'", cout.getvalue().strip())
            clr_stream(cout)
            const.onecmd('create User name="ALI" age=25 height=5.9')
            dl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(dl_id), storage.all().keys())
            clr_stream(cout)
            const.onecmd('show User {}'.format(dl_id))
            self.assertIn("'name': 'ALI'", cout.getvalue().strip())
            self.assertIn("'age': 25", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests of the database storage creation
        """
        with patch('sys.stdout', new=StringIO()) as e:
            const = HBNBCommand()
            # create model with non-null attributes
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                const.onecmd('create User')
            # create User instance
            clear_stream(e)
            const.onecmd('create User email="ali12@gmail.com" password="457"')
            dl_id = e.getvalue().strip()
            dbs = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cur = dbs.cursor()
            cur.execute('SELECT * FROM users WHERE id="{}"'.format(dl_id))
            res = cur.fetchone() 
            self.assertTrue(res is not None)
            self.assertIn('ali12@gmail.com', res)
            self.assertIn('457', res)
            cur.close()
            dbs.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests show command of the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as e:
            const = HBNBCommand()
            # showing a User instance
            obj = User(email="ali12@gmail.com", password="457")
            dbs = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cur = dbs.cursor()
            cur.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            res = cur.fetchone()
            self.assertTrue(res is None)
            const.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                e.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            dbs = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            curs = dbs.cursor()
            curs.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clr_stream(e)
            e.onecmd('show User {}'.format(obj.id))
            result = cur.fetchone()
            self.assertTrue(res is not None)
            self.assertIn('ali12@gmail.com', result)
            self.assertIn('457', result)
            self.assertIn('ali12@gmail.com', e.getvalue())
            self.assertIn('457', e.getvalue())
            cur.close()
            dbs.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Test the count command of database storage.
        """
        with patch('sys.stdout', new=StringIO()) as e:
            const = HBNBCommand()
            dbs = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cur = dbs.cursor()
            cur.execute('SELECT COUNT(*) FROM states;')
            res = cur.fetchone()
            prev_count = int(res[0])
            const.onecmd('create State name="CASA"')
            clr_stream(e)
            e.onecmd('count State')
            cnt = e.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clr_stream(e)
            e.onecmd('count State')
            cur.close()
            dbs.close()
