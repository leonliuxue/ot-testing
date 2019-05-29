import unittest


class TestIsEven(unittest.TestCase):
  def test_should_all_be_even(self):
    for n in (0, 4, -2, 11):
      with self.subTest(n=n):
        self.assertTrue(n%2==0)


if __name__ == '__main__':
  unittest.main()
