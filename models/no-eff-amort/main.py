import pandas as pd
import datetime
import math

start_time = datetime.datetime.now()

incr_list = [
     1,
     0.1,
     0.01,
     0.001,
     0.0001
]
# XIRR function is based on the IRR mathematic formula

def xirr_cal(dyn_cf_list: list):
    temp_irr_list = []
    temp_irr = .0001
    for i in range(100000):
        disc_cfs = []
        per = 0
        for cash_flow in dyn_cf_list:
            if per == 0:
                disc_cfs.append(cash_flow[1])
            else:
                disc_cf = cash_flow[1] / (1 + temp_irr/12)**per
                disc_cfs.append(disc_cf)
            per += 1
        incr_val = .0001
        if disc_cfs[0] + sum(disc_cfs[1:-1]) > 0:
            temp_irr += incr_val
            temp_add_irr= temp_irr + incr_val
            temp_irr_list.append(temp_add_irr)  
        elif disc_cfs[0] + sum(disc_cfs[1:-1]) < 0 and len(temp_irr_list) >2:
            temp_irr -= incr_val
            temp_sub_irr = temp_irr - incr_val
            temp_irr_list.append(temp_sub_irr)
        else:
            return temp_irr
        if len(temp_irr_list) > 30 and temp_irr_list[-1] == temp_irr_list[-3]:
            return temp_irr
            break
        
            

test_mode = True

# Can be interchangeable w/ .xlsx files
tape_path = "models/no-eff-amort/loan_tape_amort_ex.csv"
tape_df = pd.DataFrame(pd.read_csv(tape_path))
tape_df.reset_index()

#Define dataframe column names

col_names = {}
required_columns = ["Loan ID", "Original Loan Amount", "Interest Rate", "Original Term", "Funding Date", "UPB", "Payments"]
if test_mode == False:
    print("Please input your data input's corresponding column name: ")
    for i in required_columns:
        while True:
            col_input = input(f"{i}: ")
            if col_input in tape_df.columns:
                col_names[i] = col_input
                break
            print("Column name not found. Please reenter below: ")
else:
    col_names = {item: item for item in required_columns}

port_cf = {}

#Transaction detail entry
if test_mode == False:
    settlement_date = input("Please enter the estimated or actual purchase settlement date: ")
else:
    settlement_date = "01/01/2025"

for index, row in tape_df.iterrows():
    row_bal = row[col_names["UPB"]]
    #Will eventually be amended to a curve, but a single rate will be used temporarily
    smm_curve = [0.01 for _ in range(row[col_names["Original Term"]]+1)]
    mco_curve = [0.001 for _ in range(row[col_names["Original Term"]]+1)]

    #Cash Flow Model / Amort. Table
    loan_cash_flows = []
    loan_cash_flows.append([settlement_date, -row[col_names["UPB"]]])
    for period in range(row[col_names["Original Term"]]+1):
        if period == 0:
            continue
        curr_pmt_period = period + row[col_names["Payments"]]

        #30/360 accrual convention used. Installment loan DOES NOT change modify sched. pmt due to prepayment unless it is the last payment
        sched_pmt = row[col_names["Original Loan Amount"]] * ((row[col_names["Interest Rate"]]/12)) / (1 - (1 + (row[col_names["Interest Rate"]]/12))**(-row[col_names["Original Term"]])) 
        sched_impt = (row[col_names["Interest Rate"]]/12) * (row_bal)
        sched_ppmt = sched_pmt - sched_impt
        pre_ppmt = smm_curve[curr_pmt_period] * row_bal
        co_amt = mco_curve[curr_pmt_period] * row_bal

        if period == 1:
            dt_obj_settle_dt = datetime.datetime.strptime(settlement_date, "%m/%d/%Y")
            curr_per_date = dt_obj_settle_dt + datetime.timedelta(days=30)
        else:
            curr_per_date = loan_cash_flows[-1][0] + datetime.timedelta(days=30)

        if row_bal >= (sched_ppmt + pre_ppmt + co_amt):
            loan_cash_flows.append([curr_per_date, (sched_impt + sched_ppmt + pre_ppmt)])
            row_bal -= (sched_ppmt + pre_ppmt + co_amt)  
        else:
            loan_cash_flows.append([curr_per_date, row_bal])
            row_bal -= row_bal    
            break
    port_cf[row[col_names["Loan ID"]]] = loan_cash_flows

targ_yield = .1
loan_prices = {}
print("====LOADING====")
for loan_id, cash_flows in port_cf.items():
    irr = 0 
    amt_paid = 0
    moe = 0

    irr_tracker = []
    dyn_cf = cash_flows[0:-1]
    
    for i in range(10000):

        price_incr_val = 0.001
        count = 0
        while count < len(incr_list):
            if abs(irr-targ_yield)/incr_list[count] >= 1: 
                price_incr_val = incr_list[count]
                break
            count +=1

        irr = xirr_cal(dyn_cf)
        if irr < targ_yield:
            dyn_cf[0][1] *= (1-price_incr_val)
        elif irr > targ_yield:
            dyn_cf[0][1] *= (1+price_incr_val)
        if len(irr_tracker)>= 3 and (int(irr_tracker[-1]) == int(irr_tracker[-3])):
            amt_paid = -dyn_cf[0][1]
            moe = (float(targ_yield) - float(irr))
            break
        irr_tracker.append(dyn_cf[0][1]) 
    loan_UPB = float(tape_df.loc[tape_df['Loan ID'] == loan_id]["UPB"].iloc[0])
    price_over_under_par = (amt_paid/loan_UPB)*100
    loan_prices[loan_id] = [loan_UPB, price_over_under_par, irr]

sumprod = 0
sum = 0


for key, value in loan_prices.items():
    print(f'{key}: UPB - {value[0]} | Price - {value[1]} | Dollar Price Paid - {value[0] * (value[1]/100)}')
    sumprod += (value[0] * (value[1]/100))  
    sum += value[0]

w_avg_price = (sumprod/sum)*100
port_price = sumprod
print(f'\nWeighted Average Price - {w_avg_price}\nTotal Portfolio Price - {port_price}')
        
   
end_time = datetime.datetime.now()
print(end_time-start_time)


    