#!/usr/bin/python3

import sys
import csv
from collections import namedtuple

TaxQuickTable = namedtuple(
    'TaxQuickTable', ['start_point', 'tax_rate', 'quick_subtractor']
)

TAXQUICKITEM = [
    TaxQuickTable(80000, 0.45, 13505),
    TaxQuickTable(55000, 0.35, 5505),
    TaxQuickTable(35000, 0.30, 2755),
    TaxQuickTable(9000, 0.25, 1005),
    TaxQuickTable(4500, 0.2, 555),
    TaxQuickTable(1500, 0.1, 105),
    TaxQuickTable(0, 0.03, 0)
]


class Config(object):
    def __init__(self, _configfile):
        self._config = self.read_config()

    def read_config(self):
        config = {}
        with open(configfile) as f:
            for line in f.readlines():
                key, value = line.strip().split(' = ')
                try:
                    config[key] = float(value)
                except:
                    print("Parameter Error")
                    exit()
        return config

    def get_config(self, key):
        try:
            return self._config[key]
        except:
            print("Config Error")
            exit()

    @property
    def social_high_baseline(self):
        return self.get_config("JiShuH")

    @property
    def social_low_baseline(self):
        return self.get_config("JiShuL")

    @property
    def social_total_rate(self):
        return sum([
            self.get_config("YangLao"),
            self.get_config("YiLiao"),
            self.get_config("ShiYe"),
            self.get_config("GongShang"),
            self.get_config("ShengYu"),
            self.get_config("GongJiJin")
        ])


class UserData(object):
    def __init__(self, _userdatafile):
        self._userdata = self.read_userdata()

    def read_userdata(self):
        userdata = []
        with open(userdatafile) as f:
            for line in f.readlines():
                key_employee_id, value_salary = line.strip().split(',')
                try:
                    employee_salary = int(value_salary)
                except:
                    print("Parameter Error")
                    exit()
                userdata.append((key_employee_id, employee_salary))
        return userdata

    def __iter__(self):
        return iter(self._userdata)


class Calculator(object):
    def __init__(self, _userdata):
        self._userdata = _userdata

    @staticmethod
    def social_fund(_salary):
        if _salary < config.social_low_baseline:
            return config.social_low_baseline * config.social_total_rate
        if _salary > config.social_high_baseline:
            return config.social_high_baseline * config.social_total_rate
        return _salary * config.social_total_rate

    @classmethod
    def personal_tax(cls, _salary):
        social_fund_money = cls.social_fund(_salary)
        salary_tax_real = _salary - social_fund_money
        pay_tax_part = salary_tax_real - 3500
        if pay_tax_part <= 0:
            return 0
        for Table in TAXQUICKITEM:
            if pay_tax_part > Table.start_point:
                tax = pay_tax_part * Table.tax_rate - Table.quick_subtractor
                return tax

    @classmethod
    def salary_finally(cls, _salary):
        salary_finally = _salary - cls.social_fund(_salary) - cls.personal_tax(_salary)
        return salary_finally

    def result_list(self):
        result = []
        for employee_id, salary in self._userdata:
            social_fund_pay = '{:.2f}'.format(self.social_fund(salary))
            tax_pay = '{:.2f}'.format(self.personal_tax(salary))
            salary_finally_pay = '{:.2f}'.format(self.salary_finally(salary))
            data = [employee_id, '{}'.format(salary), social_fund_pay, tax_pay, salary_finally_pay]
            result.append(data)
        return result

    def output(self):
        result = self.result_list()
        with open(export_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(result)


if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        index = args.index('-c')
        configfile = args[index + 1]
        userdatafile = args[index + 3]
        export_path = args[index + 5]
    except:
        print("Parameter Error")
        exit()

    config = Config(configfile)
    userdata = UserData(userdatafile)
    calculator = Calculator(userdata)
    calculator.output()

