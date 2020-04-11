import unittest
from homework1304 import Calculate

class TestHomework(unittest.TestCase):
    def setUp(self):
        self.data = Calculate()

    def tearDown(self):
        self.data.result=0
        self.data.base_of_data=[]

    def test_div_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.data.div(1,0)

    def test_subs(self):
        self.data.subst(3,2)
        self.assertEqual(self.data.result, 3-2)

    def test_mult(self):
        self.data.mult(3,2)
        self.assertNotEqual(self.data.result, 2*3)

    def test_is_numbers(self):
        self.data.add(1,2)
        self.assertTrue(type(self.data.result) == int)

    def test_is_right(self):
        self.data.div(5,6)
        self.assertFalse(type(self.data.result)==int)

    def test_mult_is_add(self):
        self.data.add(5,5)
        self.assertIs(self.data.result,self.data.mult(5,2))

    def test_div_not_is_mod(self):
        self.data.div(6,4)
        self.assertIsNot(self.data.result,self.data.mod(6,4))

    def test_is_not_none(self):
        self.data.subst(3*256,2*256)
        self.assertIsNotNone(self.data.result)

    def test_is_none(self):
        self.assertIsNone(self.data.result)

    def test_result_in_base(self):
        self.data.div(10,2)
        self.data.create_base_of_data()
        self.assertIn(self.data.result,self.data.base_of_data)

    def test_is_empty_base(self):
        self.assertNotIn(self.data.result,self.data.base_of_data)

    def test_int(self):
        self.data.mult(10, 2)
        self.assertIsInstance(self.data.result,int)

    def test_not_float(self):
        self.data.mod(10, 2)
        self.assertNotIsInstance(self.data.result,float)

    def test_warns(self):
        with self.assertWarns(Warning):
            self.data.sqrt_of_num(1)


if __name__ == '__main__':
    unittest.main()




