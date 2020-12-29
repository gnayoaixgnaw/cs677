import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

data = pd.read_csv('data_banknote_authentication.csv')

data['color'] = data.apply(lambda x: 'green' if x['class'] == 0 else 'red', axis=1)
f1_mean = data.groupby('class')['variance'].mean().tolist()
f1_std = data.groupby('class')['variance'].std().tolist()
f1_all_mean = data['variance'].mean().tolist()
f1_all_std = data['variance'].std().tolist()
f2_mean = data.groupby('class')['skewness'].mean().tolist()
f2_std = data.groupby('class')['skewness'].std().tolist()
f2_all_mean = data['skewness'].mean().tolist()
f2_all_std = data['skewness'].std().tolist()
f3_mean = data.groupby('class')['curtosis'].mean().tolist()
f3_std = data.groupby('class')['curtosis'].std().tolist()
f3_all_mean = data['curtosis'].mean().tolist()
f3_all_std = data['curtosis'].std().tolist()
f4_mean = data.groupby('class')['entropy'].mean().tolist()
f4_std = data.groupby('class')['entropy'].std().tolist()
f4_all_mean = data['entropy'].mean().tolist()
f4_all_std = data['entropy'].std().tolist()

dic = [
    {'f1_mean':f1_mean[0],'f1_std':f1_std[0],'f2_mean':f2_mean[0],'f2_std':f2_std[0],'f3_mean':f3_mean[0],
     'f3_std':f3_std[0],'f4_mean':f4_mean[0],'f4_std':f4_std[0]},
    {'f1_mean':f1_mean[1],'f1_std':f1_std[1],'f2_mean':f2_mean[1],'f2_std':f2_std[1],'f3_mean':f3_mean[1],
     'f3_std':f3_std[1],'f4_mean':f4_mean[1],'f4_std':f4_std[1]},
    {'f1_mean':f1_all_mean,'f1_std':f1_all_std,'f2_mean':f2_all_mean,'f2_std':f2_all_std,'f3_mean':f3_all_mean,
     'f3_std':f3_all_std,'f4_mean':f4_all_mean,'f4_std':f4_all_std}
]

result = pd.DataFrame(dic, index=list('01a'))

print(result)
