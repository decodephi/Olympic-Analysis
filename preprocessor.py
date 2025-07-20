import pandas as pd


def preprocessor(df,region_df):

    #filtering the dataset to avilable only for summer
    df = df[df['Season'] == 'Summer']
    #merge the both dataset
    #dfr = dfr.drop(columns=['region', 'notes'], errors='ignore')
    df = df.merge(region_df, on='NOC', how='left')
    #drop dulicate
    df.drop_duplicates(inplace =True)
    #One hot encoding for boolean to int
    df = pd.concat([df,pd.get_dummies(df['Medal'],dtype=int)], axis=1)
    return df