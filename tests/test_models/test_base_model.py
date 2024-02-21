#!/usr/bin/python3
"""test Base Model """
from models.base_model import BaseModel, Base
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """test basemodel """

    def __init__(self, *args, **kwargs):
        """test init class"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """the setup method of test class"""
        pass

    def tearDown(self):
        """tearDown method"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """ test init of class """
        self.assertIsInstance(self.value(), BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value(), Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        """test default"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """test kwargs"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """test kwargs value"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """test str """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """testing the to_dict method"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        # Testing dictionary
        self.assertIsInstance(self.value().to_dict(), dict)
        # Testing keys
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        # Testing attribute
        dl = self.value()
        dl.firstname = 'John'
        dl.lastname = 'Aramko'
        self.assertIn('firstname', dl.to_dict())
        self.assertIn('lastname', dl.to_dict())
        self.assertIn('firstname', self.value(firstname='John').to_dict())
        self.assertIn('lastname', self.value(lastname='Aramko').to_dict())
        # Testing attribute
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        # Testing output
        datetime_now = datetime.datetime.today()
        dl = self.value()
        dl.id = '58796'
        dl.created_at = dl.updated_at = datetime_now
        to_dict = {
            'id': '58796',
            '__class__': dl.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(dl.to_dict(), to_dict)
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
                self.value(id='k-n23', age=25).to_dict(),
                {
                    '__class__': dl.__class__.__name__,
                    'id': 'k-n23',
                    'age': 25
                }
            )
            self.assertDictEqual(
                self.value(id='k-n23', age=None).to_dict(),
                {
                    '__class__': dl.__class__.__name__,
                    'id': 'k-n23',
                    'age': None
                }
            )
        # Testing output contradition
        dl_d = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(dl_d.to_dict(), dl_d.__dict__)
        self.assertNotEqual(
            dl_d.to_dict()['__class__'],
            dl_d.__class__
        )
        # Testing with arg
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(45)
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """test kwargs"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """test kwargs"""
        n = {'name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.name, n['name'])

    def test_id(self):
        """test id"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """test created at"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """test updated at"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
