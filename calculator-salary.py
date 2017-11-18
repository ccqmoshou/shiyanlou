#!/usr/bin/python3

import sys

def social_fund(employee_salary):
    global fund
    fund = employee_salary * 0.165
    return fund

def calculator_tax(salary_real):
    global pay_tax

    if salary_real <= 1500:
        pay_tax = salary_real * 0.03 - 0
    elif 1500 < salary_real <= 4500:
        pay_tax = salary_real * 0.1 - 105
    elif 4500 < salary_real <= 9000:
        pay_tax = salary_real * 0.2 - 555
    elif 9000 < salary_real <= 35000:
        pay_tax = salary_real * 0.25 -1005
    elif 35000 < salary_real <= 55000:
        pay_tax = salary_real * 0.3 - 2755
    elif 55000 < salary_real <= 80000:
        pay_tax = salary_real * 0.35 -5505
    else:
        pay_tax = salary_real * 0.45 -13505

    return pay_tax

try:
    employee_info = sys.argv[1:]
    for arg in employee_info:
        arg_list = arg.split(':')
        employee_id = int(arg_list[0])
        employee_salary = int(arg_list[1])
        social_fund(employee_salary)
        salary_real = employee_salary - fund - 3500
        if salary_real > 0:
            calculator_tax(salary_real)
            salary_finally = employee_salary - fund - pay_tax
        else:
            salary_finally = employee_salary - fund
        print('{0}:{1:.2f}'.format(employee_id, salary_finally)) 

except:
    print("Parameter Error")

