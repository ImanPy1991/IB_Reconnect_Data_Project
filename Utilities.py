import os
import pandas as pd

def save_dataframe_to_csv(df, Myfilename):
    df = pd.DataFrame(df)
    os.makedirs(name= 'data/Monday_Newdata002', exist_ok= True)
    df.to_csv(os.path.join('data/Monday_Newdata002', Myfilename) , index= False , header= False)
