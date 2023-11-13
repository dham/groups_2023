import numbers
import numpy as np


class Element:
    def __init__(self, group, value):
        group._validate(value)
        self.group = group
        self.value = value

    def __str__(self):
        return f"{self.value}_{self.group}"

    def __repr__(self):
        return f"{type(self).__name__}({self.group!r}, {self.value!r})"

    def __mul__(self, other):
        return type(self)(self.group,
                          self.group.operation(self.value, other.value))


class Group:
    def __init__(self, order):
        self.order = order

    def __str__(self):
        return f"C{self.order}"

    def __repr__(self):
        return f"{type(self).__name__}({self.order!r})"

    def __call__(self, value):
        return Element(self, value)


class CyclicGroup(Group):

    def _validate(self, value):
        if not isinstance(value, numbers.Integral):
            raise TypeError("Cyclic group members must be integers.")
        if not 0 <= value < self.order:
            raise ValueError(
                "Cyclic group of order {self.order} invalid value {value}"
            )

    def operation(self, a, b):
        return (a + b) % self.order


class GeneralLinearGroup(Group):

    def _validate(self, value):
        if not isinstance(value, np.ndarray):
            raise TypeError("Element value must be an array.")
        if not value.shape == (self.order, self.order):
            raise ValueError(
                "Elements of the General Linear group must be square."
            )

    def operation(self, a, b):
        return a @ b
