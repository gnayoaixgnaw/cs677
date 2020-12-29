# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:37:29 2018

@author: epinsky
this scripts reads your ticker file (e.g. MSFT.csv) and
constructs a list of lines
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def add_label(x): # this function is to compute the return as label: +, -, when return < 0 add - label else add + label
    if x < 0:
        return "-"
    else:
        return "+"
def add_ensemble_label(x,y,z): # this function is to add ensembel label,by comparing the numbers of +,- label
    num_pos = (x + y + z).count('+')
    num_neg = (x + y + z).count('-')
    if num_pos > num_neg:
        return "+"
    else:
        return "-"



def predict(x,y): # this function is to predict the label based on the frequency on history

    count_result_1 = y.count(x+'-')
    count_result_2 = y.count(x+'+')
    if count_result_1 > count_result_2:
        return "-"
    else:
        return "+"

def accuracy(x,y): #
    id_num = x.groupby(by=['True_Label', 'pre_label_' + str(y)]).size().values
    #id_index = x.groupby(by=['label', 'pre_label_' + str(y)]).size().index # hear is a tuple list , like in pattern (true,predict): (+,+),(+,-),(-,+),(-,-)

    accuracy_ = (id_num[0] + id_num[3]) / (id_num[1] + id_num[2] + id_num[3] + id_num[0])
    return accuracy_

def accuracy_pos(x,y):
    id_num = x.groupby(by=['True_Label', 'pre_label_' + str(y)]).size().values
    accuracy_ = (id_num[0]) / (id_num[1] + id_num[0])
    return accuracy_

def accuracy_neg(x,y):
    id_num = x.groupby(by=['True_Label', 'pre_label_' + str(y)]).size().values
    accuracy_ = (id_num[3]) / (id_num[2] + id_num[3])
    return accuracy_

def accuracy_1(x):
    id_num = x.groupby(by=['True_Label', 'ensemble_label']).size().values
    accuracy_ = (id_num[0] + id_num[3]) / (id_num[1] + id_num[2] + id_num[3] + id_num[0])
    return accuracy_
def accuracy_1_pos(x):
    id_num = x.groupby(by=['True_Label', 'ensemble_label']).size().values
    accuracy_ = (id_num[0]) / (id_num[1] + id_num[0])
    return accuracy_
def accuracy_1_neg(x):
    id_num = x.groupby(by=['True_Label', 'ensemble_label']).size().values
    accuracy_ = (id_num[3]) / (id_num[2] + id_num[3])
    return accuracy_

def TP_FP_TN_FN(x,y):
    id_num = x.groupby(by=['True_Label', y]).size().values
    return [id_num[0],id_num[2],id_num[3],id_num[1],format(id_num[0]/(id_num[0] + id_num[1]), '.2%'),format(id_num[3]/(id_num[3] + id_num[2]), '.2%')]

def draw(x1,x2,init):
    for v in ['True_Label','ensemble_label',"pre_label_2"]: #here i choose W* = W2
        z = init
        keys1 = x1[v].tolist()
        values1 = x1['Return'].tolist()
        date1 = x1['Date'].tolist()
        keys2 = x2[v].tolist()
        values2 = x2['Return'].tolist()
        date2 = x2['Date'].tolist()
        keys = keys1+keys2 # label
        values = values1+values2 # return
        date = date1+date2 # date

        amount = []
        if v =='True_Label':
            for i in range(len(keys)):
                z = z*(1+float(values[i]))
                amount.append(z)
            plt.plot(date, amount,label = 'True')
            plt.xlabel('Date')
            plt.ylabel('Amount')
            plt.title('growth of amount')
        else:
            for i in range(len(keys)):
                if keys[i] == "+":
                    z = z*(1+values[i]) # if predict + then return
                    amount.append(z)
                else:
                    z = z    # if predict - then 0
                    amount.append(z)
            if v == 'ensemble_label':
                plt.plot(date, amount,label = 'ensemble')
                plt.xlabel('Date')
                plt.ylabel('Amount')
                plt.title('growth of amount')
            elif v == 'pre_label_2':
                plt.plot(date, amount, label='w*')
                plt.xlabel('Date')
                plt.ylabel('Amount')
                plt.title('growth of amount')

    plt.legend(loc='best')
    plt.show()


ticker='WMT'
#ticker='SPY'       # select a stock
ticker_file = os.path.join(ticker + '.csv')

try:
    with open(ticker_file) as f:
        lines = f.read().splitlines()
    print('opened file for ticker: ', ticker)

    """    your code for assignment 1 goes here
    """

    df = pd.DataFrame(pd.read_csv(ticker + '.csv'))
    df['True_Label'] = df.apply(lambda x: add_label(x.Return), axis=1) # add true label
    print(df)
    df_15_17 = df.loc[df['Year'].isin([2015,2016,2017])] #df_15_17 is a df which contain year 2015,2016,2017's data
    df_17 = df.loc[df['Year'].isin([2017])] #df_17 is a df which contain year 2017's data
    df_18 = df.loc[df['Year'].isin([2018])]
    df_19 = df.loc[df['Year'].isin([2019])]


    x = df_15_17.groupby(df["True_Label"])
    dict1 = {}
    for i in x:
        dict1[i[0]] = len(i[1])
    p_up = dict1['+']/(dict1['+']+dict1['-']) # count the number of label + from 2015-2017
    print(format(p_up, '.2%'))# question 1.2
    for i in [1,2,3]:
        x1 = (1-p_up)**i*p_up
        x2 = (1-p_up)**(i+1)
        print("k=",i,format(x1, '.2%')) # question 1.3 compute the probability that after seeing k consecutive ”down days”, the next day is an ”up day”
        x3 = (p_up) ** (i+1)
        x4 = (p_up) ** i *(1-p_up)
        print("k=",i,format(x3, '.2%'))  # question 1.4  compute the the probability that afterseeing k consecutive ”up days”, the next day is still an”up day”
    '''
    label_list = ''
    for i in [2015,2016,2017]:
        df2 = df_15_17[(df_15_17["Year"] == i)]
        label_list = label_list.join(df2["True_Label"].values)
    '''

    label_list = ''.join(df_15_17['True_Label'].values) # get all true labels from 2015-2017 and add them to a list
    for w in [2,3,4]:
        label_list_18 = ''.join(df_18["True_Label"].values)
        pre_label_list_18 = []
        for k in range(w):     # the first for loop is for the first w days of the year,cause when you predict the label of 2018.1.1,you need the true labels from 2017.12.30 31
            str1 = ''          # for instance, if w =2, we need 2017.12.30,2017.12.31 to predict 2018.1.1, so i use a for loop to get the label of that two days,
            for j in range(w): #  but when it comes to 2018.1.2, i need to use 2017.12.31 and 2018.1.1, so i use a if function here : if (-w+j+k) > 0 ,it will use
                if (-w+j+k) > 0:# df_18[index], if (-w+j+k) <0, it means i need to get the data from df_17[-index] to get the last data of that dataframe
                    str1 = str1 + df_18.iloc[-w+j+k]['True_Label']
                else:
                    str1 = str1 + df_17.iloc[-w+j+k]['True_Label']
            # generate the string of labels from previous three days
            pre_label_list_18.append(predict(str1,label_list)) # predict the next day's label

        for i in range(len(label_list_18)-w):# this loop is for the days in the year
            str1 = ''
            for j in range(w):
                str1 = str1 + df_18.iloc[i+j]['True_Label']
            pre_label_list_18.append(predict(str1,label_list))

        df_18.insert(17+w-2, 'pre_label_'+str(w), pre_label_list_18) #quesiton 2.1 add predict label base on 1,2,3 years


        label_list_19 = ''.join(df_19["True_Label"].values)
        pre_label_list_19 = []
        for k in range(w):
            str1 = ''
            for j in range(w):
                if (-w + j + k) > 0:
                    str1 = str1 + df_19.iloc[-w + j + k]['True_Label']
                else:
                    str1 = str1 + df_18.iloc[-w + j + k]['True_Label']
            pre_label_list_19.append(predict(str1,label_list))

        for i in range(len(label_list_19)-w):
            str1 = ''
            for j in range(w):
                str1 = str1 + df_19.iloc[i+j]['True_Label']
            pre_label_list_19.append(predict(str1,label_list))

        df_19.insert(17+w-2, 'pre_label_'+str(w), pre_label_list_19) #quesiton 2.1 add predict label base on 1,2,3 years

        '''
    
        id_name = df_18.groupby(by=['label','pre_15_label_'+str(w)]).size().index
        id_num=df_18.groupby(by=['label','pre_15_label_'+str(w)]).size().values
        
    
        accuracy_ = (id_num[0] + id_num[3]) / (id_num[1] + id_num[2] + id_num[3] + id_num[0])
        print('accuracy_'+str(w)+'is ',accuracy_)
        '''
        print(w,18, format(accuracy(df_18, w), '.2%')) # question2.2 w here means the value of w
        print(w,19, format(accuracy(df_19, w), '.2%')) # question2.2
        print(w, 18,"positive_acc", format(accuracy_pos(df_18, w), '.2%'))# question3.3
        print(w, 18,"negative_acc",format(accuracy_neg(df_18, w), '.2%'))# question3.3
        print(w, 19,"positive_acc", format(accuracy_pos(df_19, w), '.2%'))# question3.3
        print(w, 19,"negative_acc",format(accuracy_neg(df_19, w), '.2%'))# question3.3
    print(df_18)
    print(df_19) #question2.1
    # add emsemble_label
    df_18_1 = df_18.loc[1:,['Date', 'Year', 'Month', 'Day', 'Weekday',
                        'Week_Number', 'Year_Week', 'Open',
                        'High', 'Low', 'Close', 'Volume', 'Adj Close',
                        'Return', 'Short_MA', 'Long_MA',"True_Label","pre_label_2","pre_label_3","pre_label_4"]]
    df_19_1 = df_19.loc[1:,['Date', 'Year', 'Month', 'Day', 'Weekday',
                        'Week_Number', 'Year_Week', 'Open',
                        'High', 'Low', 'Close', 'Volume', 'Adj Close',
                        'Return', 'Short_MA', 'Long_MA',"True_Label","pre_label_2","pre_label_3","pre_label_4"]]
    df_18_1['ensemble_label'] = df_18_1.apply(lambda x: add_ensemble_label(x["pre_label_2"],x["pre_label_3"],x["pre_label_4"]), axis=1) # question 3.1
    df_19_1['ensemble_label'] = df_19_1.apply(lambda x: add_ensemble_label(x["pre_label_2"],x["pre_label_3"],x["pre_label_4"]), axis=1) # question 3.1

    print(df_18_1)
    print(df_19_1) #question3.1

    print(18,format(accuracy_1(df_18_1), '.2%')) #qusetion 3.2
    print(19,format(accuracy_1(df_19_1), '.2%')) #qusetion 3.2

    print(18,"pos",format(accuracy_1_pos(df_18_1), '.2%'))# question3.3 by using ensemble label
    print(18,"neg",format(accuracy_1_neg(df_18_1), '.2%'))# question3.3 by using ensemble label
    print(19,"pos",format(accuracy_1_pos(df_19_1), '.2%'))# question3.3 by using ensemble label
    print(19,"neg",format(accuracy_1_neg(df_19_1), '.2%'))# question3.3 by using ensemble label
    for q in ["pre_label_2","pre_label_3","pre_label_4",'ensemble_label']:
        print(18, q,TP_FP_TN_FN(df_18_1,q)) #quesiton 4
        print(19, q, TP_FP_TN_FN(df_19_1, q)) #quesiton 4


    draw(df_18_1, df_19_1,100) #quesiton 5 draw the graph ,begin with $100





except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)












