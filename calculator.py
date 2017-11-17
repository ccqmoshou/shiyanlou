#!/usr/bin/python3

import sys

try:
    salary = int(sys.argv[1])
    salary_tax = salary - 3500

    if salary_tax <= 1500:
        pay_tax = salary_tax * 0.03 - 0

    elif 1500 < salary_tax <= 4500:
        pay_tax = salary_tax * 0.1 - 105

    elif 4500 < salary_tax <= 9000:
        pay_tax = salary_tax * 0.2 - 555

    elif 9000 < salary_tax <= 35000:
        pay_tax = salary_tax * 0.25 -1005

    elif 35000 < salary_tax <= 55000:
        pay_tax = salary_tax * 0.3 - 2755

    elif 55000 < salary_tax <= 80000:
        pay_tax = salary_tax * 0.35 -5505

    else:
        pay_tax = salary_tax * 0.45 -13505

    print(format(pay_tax, ".2f"))

except:
    print("Parameter Error")

