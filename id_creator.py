import pandas as pd
   

id_list = [f'xxx{i}' for i in range(100)]
pd.DataFrame(id_list).to_csv('ids.csv')