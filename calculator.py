def calculate_director(company, employees, detail):
    income = company["daily_income"]
    for v in employees.values():
        income -= v["wage"]
    income -= detail["advertising_budget"]
    return income

def calculate_bank(TCI, merits, invest, rate): # 银行利率为年化
    if TCI:
        rate *= 1.1
    rate *= 1+merits*0.05
    return invest*rate/100

def calculate_stocks(values, period): # 股票既有31d又有7d，统一按日
    return values/period

def calculate_others(values):
    return values/31