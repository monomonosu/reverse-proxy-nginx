import unittest
import sys,os

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))
from app import db, app
from models import *
from seeder import seeder


class BasicTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # print('-----setUp-----')
        pass

    # テスト後にシーダーを流しなおす
    @classmethod
    def tearDownClass(cls):
        print("---tearDown---")
        seeder()

    def test_get_units(self):
        print('---Unit全件読み込み---')
        units = Unit.query.all()
        unitCount = len(units)
        self.assertTrue(unitCount)

    def test_get_units_dict(self):
        print('---Unit全件読込→Dict---')
        units = Unit.query.all()
        sch = UnitSchema(many=True).dump(units)
        self.assertEqual(sch[0]['unitName'], '個')

    def test_get_unit_byId(self):
        print('---Unit一件読み込み---')
        unit = Unit.query.filter(Unit.id == 1).first()
        self.assertTrue(unit)
        self.assertEqual(unit.unitName, '個')

        print('---Unit一件読み込み失敗---')
        units = Unit.query.filter(Unit.id == 9999).all()
        self.assertFalse(units)
        self.assertEqual(len(units), 0)

    def test_update_unit(self):
        print('---Unit一件更新---')
        unit = Unit.query.filter(Unit.id == 2).first()
        unit.unitName = '丁'
        db.session.commit()
        unit = Unit.query.filter(Unit.id == 2).first()
        self.assertEqual(unit.unitName, "丁")

    def test_create_unit(self):
        print('---Unit新規作成---')
        units = [
            Unit(unitName='式'),
            Unit(unitName='枚'),
        ]
        db.session.add_all(units)
        db.session.commit()
        self.assertGreaterEqual(len(Unit.query.all()), 2)

    def test_delete_unit(self):
        print('---Unit一件削除---')
        unit = Unit(unitName='点')
        db.session.add(unit)
        db.session.commit()
        newId = unit.id
        unit = Unit.query.filter(Unit.id == newId).delete()
        db.session.commit()

        unit = Unit.query.filter(Unit.id == newId).all()
        self.assertEqual(len(unit), 0)


if __name__ == '__main__':
    unittest.main()
