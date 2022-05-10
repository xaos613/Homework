'''
Implement a class Money to represent value and currency. You need to implement methods to use all basic
arithmetics expressions (comparison, division, multiplication, addition and subtraction).
Tip: use class attribute exchange rate which is dictionary and stores information about exchange rates
to your default currency:
'''


class Money:
    exchange_rate = {
        "EUR": 0.93,
        "BYN": 2.1
    }

    def __init__(self, value, currency="USD"):
        self.value = value
        self.currency = currency.upper()

    def __repr__(self):
        return f'{round(self.value, 2)} {self.currency}'

    def __str__(self):
        return f'{round(self.value, 2)} {self.currency}'

    def _exchange(self, value, currency):
        if currency == 'USD':
            return value
        else:
            return round(value / self.exchange_rate[currency], 2)

    def _back_exchange(self, value, currency):
        if currency == 'USD':
            return value
        else:
            return round(value * self.exchange_rate[currency], 2)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.value + other, self.currency)
        elif isinstance(other, Money):
            result_in_USD = self._exchange(self.value, self.currency) + self._exchange(other.value, other.currency)
            return Money(self._back_exchange(result_in_USD, self.currency), self.currency)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Money(self.value - other, self.currency)
        elif isinstance(other, Money):
            result_in_USD = self._exchange(self.value, self.currency) - self._exchange(other.value, other.currency)
            return Money(self._back_exchange(result_in_USD, self.currency), self.currency)

    __rsub__ = __sub__



    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Money(round(self.value * other, 2), self.currency)

    __rmul__ = __mul__


x = Money(10, "BYN")
y = Money(11)  # define your own default value, e.g. “USD”
z = Money(12.34, "EUR")
# print(y + x)
# print(x - 3.11)  # result in “EUR”
# print(z)
# print(3.11 * x)
# print(y * 0.8)
#
#
# print(z + 3.11 * x + y * 0.8) # result in “EUR”


lst = [Money(10,"BYN"), Money(11), Money(12.01, "EUR")]

s = sum(lst)
print(s) #result in “BYN”