import unittest
from db import InMemoryDatabase

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryDatabase()

    def test_set_record(self):
        self.db.set_record('a', 10)
        self.assertEqual(self.db.get_record('a'), 10)
    
    def test_get_record(self):
        self.assertIsNone(self.db.get_record('a'))
        self.db.set_record('a', 10)
        self.assertEqual(self.db.get_record('a'), 10)

    def test_first_transaction(self):
        self.db.begin_transaction()
        self.db.set_record('a', 10)
        self.assertEqual(self.db.get_record('a'), 10)
        self.db.begin_transaction()
        self.db.set_record('a', 20)
        self.assertEqual(self.db.get_record('a'), 20)
        self.db.rollback_transaction()
        self.assertEqual(self.db.get_record('a'), 10)
        self.db.rollback_transaction()
        self.assertIsNone(self.db.get_record('a'))

    def test_second_transaction(self):
        self.db.begin_transaction()
        self.db.set_record('a', 30)
        self.db.begin_transaction()
        self.db.set_record('a', 40)
        self.db.commit_transaction()
        self.assertEqual(self.db.get_record('a'), 40)

    def test_third_transaction(self):
        self.db.set_record('a', 50)
        self.db.begin_transaction()
        self.assertEqual(self.db.get_record('a'), 50)
        self.db.set_record('a', 60)
        self.db.begin_transaction()
        self.db.delete_record('a')
        self.assertIsNone(self.db.get_record('a'))
        self.db.rollback_transaction()
        self.assertEqual(self.db.get_record('a'), 60)
        self.db.commit_transaction()
        self.assertEqual(self.db.get_record('a'), 60)

    def test_fourth_transaction(self):
        self.db.set_record('a', 10)
        self.db.begin_transaction()
        self.assertEqual(self.db.get_value_count(10), 1)
        self.db.begin_transaction()
        self.db.delete_record('a')
        self.assertEqual(self.db.get_value_count(10), 0)
        self.db.rollback_transaction()
        self.assertEqual(self.db.get_value_count(10), 1)
        self.db.commit_transaction()

if __name__ == '__main__':
    unittest.main()