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

    def test_get_categories(self):
        print('---Category全件読み込み---')
        categories = Category.query.all()
        categoryCount = len(categories)
        self.assertTrue(categoryCount)

    def test_get_categories_dict(self):
        print('---Category全件読込→Dict---')
        categories = Category.query.all()
        sch = CategorySchema(many=True).dump(categories)
        self.assertEqual(sch[0]['categoryName'], '食料品')

    def test_get_category_byId(self):
        print('---Category一件読み込み---')
        category = Category.query.filter(Category.id == 1).first()
        self.assertTrue(category)
        self.assertEqual(category.categoryName, '食料品')

        print('---Category一件読み込み失敗---')
        categories = Category.query.filter(Category.id == 9999).all()
        self.assertFalse(categories)
        self.assertEqual(len(categories), 0)

    def test_update_category(self):
        print('---Category一件更新---')
        category = Category.query.filter(Category.id == 2).first()
        category.categoryName = 'カテゴリー変更'
        db.session.commit()
        category = Category.query.filter(Category.id == 2).first()
        self.assertEqual(category.categoryName, "カテゴリー変更")

    def test_create_category(self):
        print('---Category新規作成---')
        categories = [
            Category(categoryName='衣類'),
            Category(categoryName='工具'),
        ]
        db.session.add_all(categories)
        db.session.commit()
        self.assertGreaterEqual(len(Category.query.all()), 2)

    def test_delete_category(self):
        print('---Category一件削除---')
        category = Category(categoryName='消耗品')
        db.session.add(category)
        db.session.commit()
        newId = category.id
        category = Category.query.filter(Category.id == newId).delete()
        db.session.commit()

        category = Category.query.filter(Category.id == newId).all()
        self.assertEqual(len(category), 0)


if __name__ == '__main__':
    unittest.main()
