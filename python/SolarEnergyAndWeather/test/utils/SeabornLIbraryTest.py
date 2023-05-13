import unittest

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    def test_something(self):
        df = pd.DataFrame({'team': ['A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B'],
                   'assists': [3, 4, 4, 7, 9, 6, 7, 8, 10, 12],
                   'points': [5, 6, 9, 12, 15, 5, 10, 13, 13, 19]})
        print(df)
        sns.pairplot(data=df, vars=['team', 'assists', 'points'])
        plt.show()


if __name__ == '__main__':
    unittest.main()
