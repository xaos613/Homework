from unittest import TestCase, main
from unittest.mock import patch

import mock

import task


class Test_Goldbach(TestCase):

    def test_is_even(self):
        self.assertEqual(task.chckerfunc(4), 4)
        self.assertEqual(task.chckerfunc(8), 8)
        with self.assertRaises(task.EmptyException):
            task.chckerfunc(None)
        with self.assertRaises(task.TypeException):
            task.chckerfunc('r')
        with self.assertRaises(task.TypeException):
            task.chckerfunc((10, 20))
        with self.assertRaises(task.ValueException):
            task.chckerfunc('3')
        with self.assertRaises(task.ValueException):
            task.chckerfunc(0)
        with self.assertRaises(task.ValueException):
            task.chckerfunc(3)
        with self.assertRaises(task.ValueException):
            task.chckerfunc(-3)

    def test_goldbach(self):
        with self.assertRaises(task.ValueException):
            task.goldbach(2)
        self.assertEqual(task.goldbach(20), (20, [3, 17]))
        self.assertEqual(task.goldbach(4), (4, [2, 2]))

    def test_get_primes(self):
        self.assertEqual(task.get_primes(4), [2, 3])
        self.assertEqual(task.get_primes(20), [2, 3, 5, 7, 11, 13, 17, 19])

    def test_CustomException(self):
        self.assertEqual(str(task.CustomException('Custom message')), 'Custom message')
        self.assertEqual(str(task.CustomException()), '')

    def test_input(self):
        with mock.patch('builtins.input', return_value="6"):
            assert task.get_input() == '6'
        with mock.patch('builtins.input', return_value="t"):
            assert task.get_input() == 't'
        with mock.patch('builtins.input', return_value="q"):
            self.assertRaises(SystemExit)
        with mock.patch('builtins.input', return_value=""):
            self.assertRaises(task.EmptyException)
        with mock.patch('builtins.input', return_value="bbb"):
            self.assertRaises(task.TypeException)

    @patch('task.chckerfunc')
    @patch('task.get_primes')
    def test_find_goldbach_mock(self, mock_primes, mock_chckerfunc):
        mock_chckerfunc.return_value = 50
        mock_primes.return_value = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        self.assertEqual(task.goldbach(50), (50, [3, 47]))
        mock_chckerfunc.return_value = 50
        mock_primes.return_value = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
        self.assertEqual(task.goldbach(50), (50, [7, 43]))
        mock_chckerfunc.return_value = False
        mock_primes.return_value = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]





if __name__ == '__main__':
    main()
