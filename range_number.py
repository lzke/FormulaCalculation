#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/21 21:53
# @Author  : KE
# @File    : range_number.py

from decimal import Decimal


def decimal_range(x, y, jump):
    while x <= y:
        yield Decimal(x)
        x += Decimal(jump)


class RangeNumber(object):
    def __init__(self, param_value):
        self.num_min = Decimal(str(param_value["range"][0]))
        self.num_max = Decimal(str(param_value["range"][1]))

        self.num_graduate = Decimal("0.000001")
        if "graduate" in param_value:
            self.num_graduate = Decimal(str(param_value["graduate"]))

        self.num_range = decimal_range(self.num_min, self.num_max, self.num_graduate)

    def range(self):
        return self.num_range

