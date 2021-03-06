# coding: utf-8

import kanimysql
import yaml
import pytest

yaml_data = '''
adapter: mysql
database: test
username: root
password: p@ssw0rd
host: 127.0.0.1
port: 3306
charset: utf8
'''
db_settings = yaml.load(yaml_data)
conn = kanimysql.KaniMySQL(db=db_settings['database'], host=db_settings['host'], user=db_settings['username'],
                           passwd=db_settings['password'], charset=db_settings['charset'], port=db_settings['port'])

TestResult = conn.get_table_class('test_results')

test = TestResult()
test.name = 'Slim Shady'
test.student_id = 2345
test.birth_date = '2018-01-02T13:38:00'
conn.insert(test)

tests = conn.select(TestResult)
for test in tests:
    assert conn.update(test) == -1, 'Checking unmodified value is not executed'

import random
for test in tests:
    test.test_result = random.randint(0, 100)
    assert conn.update(test, columns=['test_result']) == 1, 'modified value is not recorded.'
    assert conn.update(test) == 0, 'Update query was not properly executed.'
    assert conn.update(test) == -1, 'Checking unmodified value returns -1'

tests = conn.select(TestResult)
print(tests)
tests = conn.select(TestResult, where={'name': 'Slim Shady'})
print(tests)
tests = conn.select(TestResult, where={'id': {'$>=': 0}})
print(tests)

# Error will raise if the columns name does'nt exist.
with pytest.raises(KeyError):
    test.bad_column_name = 'test'

conn.delete(table=TestResult)
