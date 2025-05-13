
import pandas as pd

def merge_data(df_weather, df_sunshine):
    df_merge = pd.merge(df_weather, df_sunshine, on=['지점명', '일시'], how='left')
    return df_merge
