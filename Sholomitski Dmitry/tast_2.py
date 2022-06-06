import task
from unittest import TestCase, main
from unittest.mock import call, patch

class Test_mock_global_task(TestCase):

        @patch('builtins.print')
        @patch('task.get_input')
        def test_main(self, mock_input, mock_print):
            mock_input.side_effect = ['r', '10', '', '20', '0', '-5', '6', 'q']

            task.main()
            self.assertEqual(mock_print.mock_calls, [
                call('Incorrect input: There should be integer argument'),
                call((10, [3, 7])),
                call('Incorrect input: There should  be at least 1 argument'),
                call((20, [3, 17])),
                call('Incorrect input: Input integer should be more than 3, you gave 0'),
                call('Incorrect input: Input integer should be more than 3, you gave -5'),
                call((6, [3, 3])),
                call('Thank you for using my script. Bye')])

if __name__ == '__main__':
    main()