import pandas as pd
import statistics
import matplotlib.pyplot as plt

fannie_cpr = "models/tools/cpr_set/FRE_HDPR_Fctr_201902_to_202303.txt"
fcpr_df = pd.read_csv(fannie_cpr, sep="|")
fcpr_df['Date'] = pd.to_datetime(fcpr_df['Date'], format='%Y%m%d')


cohort_types = fcpr_df['Type of Security'].unique()
cohort_years = fcpr_df['Year'].unique()

    
cohort_cpr_vals = {}
for sec_type in cohort_types:
    cohort_cpr_vals[sec_type] = {}
    for year in cohort_years:
        spec_vals = fcpr_df.loc[(fcpr_df['Year'] == year) & (fcpr_df['Type of Security'] == sec_type ) & (fcpr_df['Date'].dt.day == 1)]
        cohort_cpr_vals[sec_type][year] = spec_vals
        

for mort_type in cohort_types:
    print(mort_type)
    for year in cohort_years:
        y_vals = 1 - (1 - cohort_cpr_vals[mort_type][year]['SMM'])**365
        out_val = 0
        if len(y_vals) <= 2: 
            out_val = "N/A"
        else:
            out_val = statistics.mean(y_vals)
        print(f'{year} Cohort CPR Mean: {out_val}')

