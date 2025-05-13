import pandas as pd

def preprocess_data(df_weather, df_sunshine):
    df_weather['일시'] = pd.to_datetime(df_weather['일시'])
    df_sunshine['일시'] = pd.to_datetime(df_sunshine['일시'])
    df_merge = pd.merge(df_weather, df_sunshine, on=['지점명', '일시'], how='left')
    return df_merge
