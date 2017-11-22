#!/usr/bin/python3

import sys
import csv
from collections import namedtuple

TaxQuickItem = namedtuple(
    'TaxQuickItem', ['start_point', 'tax_rate', 'quick_subtractor']
)

TAXQUICKTABLE = [
    TaxQuickItem(80000, 0.45, 13505),
    TaxQuickItem(55000, 0.35, 5505),
    TaxQuickItem(35000, 0.30, 2755),
    TaxQuickItem(9000, 0.25, 1005),
    TaxQuickItem(4500, 0.2, 555),
    TaxQuickItem(1500, 0.1, 105),
    TaxQuickItem(0, 0.03, 0)
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
        userdata = {}
        with open(userdatafile) as f:
            for line in f.readlines():
                key_employee_id, value_salary = line.strip().split(',')
                try:
                    userdata[key_employee_id] = int(value_salary)
                except:
                    print("Parameter Error")
                    exit()
        return userdata

    @property
    def __iter__(self):
        return iter(self._userdata)

    def get_salary(self, _employee_id):
        return self._userdata[_employee_id]


class Calculator(object):
    def __init__(self, _salary):
        self.salary = salary

    @staticmethod
    def social_fund(_salary):
        if salary < config.social_low_baseline:
            return config.social_low_baseline * config.social_total_rate
        if salary > config.social_high_baseline:
            return config.social_high_baseline * config.social_total_rate
        return salary * config.social_total_rate

    @classmethod
    def personal_tax(cls, _salary):
        social_fund_money = cls.social_fund(salary)
        salary_tax_real = salary - social_fund_money
        pay_tax_part = salary_tax_real - 3500
        if pay_tax_part < 0:
            return '0.00'
        for item in TAXQUICKTABLE:
            if pay_tax_part > item.start_point:
                tax = pay_tax_part * item.tax_rate - item.quick_subtractor
                return '{:.2f}'.format(tax)

    @classmethod
    def salary_finally(cls, _salary):
        salary_finally = salary - cls.social_fund(salary) - cls.personal_tax(salary)
        return '{:.2f}'.format(salary_finally)


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
    employee_list = userdata.__iter__
    result = []
    for employee_id in employee_list:
        salary = userdata.get_salary(employee_id)
        social_fund_pay = Calculator.social_fund(salary)
        tax_pay = Calculator.personal_tax(salary)
        salary_finally_pay = Calculator.salary_finally(salary)
        result = [employee_id, salary, social_fund_pay, tax_pay, salary_finally_pay]
        with open(export_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writer(result)
