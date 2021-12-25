#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/21 10:39
# @Author  : KE
# @File    : range_getter.py

import csv
import decimal
import io
import itertools
import time
from decimal import Decimal, localcontext

import yaml

from range_number import RangeNumber


def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents.strip()


def write_to_csv(header, content):
    file_name = "%s.csv" % str(int(time.time()))
    with open(file_name, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, header)
        writer.writeheader()
        writer.writerows(content)


def get_range():
    with open("config.yaml", encoding="utf-8") as f:
        conf = yaml.safe_load(f)

    formula = conf.get("formula", "")
    end_graduate = Decimal(str(conf.get("end", "0.000001")))
    end_exponent = end_graduate.as_tuple().exponent

    local_parameters = locals()
    range_numbers = dict()
    for param_name in conf["parameter"]:
        param_value = conf["parameter"][param_name]
        if isinstance(param_value, dict):
            range_numbers[param_name] = RangeNumber(param_value)
        else:
            local_parameters[param_name] = Decimal(str(param_value))

    result = list()
    for param_values in itertools.product(*[rn.range() for rn in range_numbers.values()]):
        for idx, param_name in enumerate(range_numbers.keys()):
            local_parameters[param_name] = param_values[idx]

        with localcontext() as ctx:
            ctx.clear_flags()
            end = Decimal(print_to_string(eval(formula)))
            end_exp = end.as_tuple().exponent
            if not ctx.flags[decimal.Inexact] and end_exp >= end_exponent:
                res = {"end": end}
                for param_name in range_numbers.keys():
                    res[param_name] = local_parameters[param_name]
                    print(param_name, res[param_name], " ", end="")
                print("end:", end)
                result.append(res)

    header = list(range_numbers.keys())
    header.append("end")
    write_to_csv(header, result)


if __name__ == '__main__':
    time_start = time.time()
    get_range()
    time_end = time.time()
    print("\ntime cost", time_end - time_start, "s")
