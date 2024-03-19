import re
import pandas as pd
def extract_kr(df):
    korean_pattern = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    kr_df = df[df["출원인국적"].str.contains("KR")]
    kr_korean_df = kr_df[kr_df["발명자"].apply(lambda x: korean_pattern.search(x) is not None)]
    return kr_korean_df
def extract_samename(df, column):
    exploded_df = df.assign(발명자=df[column].str.split("|")).explode(column, ignore_index=True)
    duplicate_names = exploded_df[exploded_df.duplicated(subset=[column], keep=False)]
    duplicate_names=duplicate_names.sort_values(by=column)
    return duplicate_names
def merge_to_csv(df1,df2,overlap_col, target_col):
    common_skeys = df2[df2[overlap_col].isin(df1[overlap_col])]
    merged_df = pd.merge(df1, df2, on=overlap_col, how='left')

    # 'skey'가 일치하는 행에 '출원일' 열 추가
    merged_df[target_col] = merged_df[target_col].fillna(merged_df[target_col])
    sorted_df = merged_df.sort_values(by='출원일')
    return sorted_df
def explode_split(df,column):
    df[column] = df[column].str.split('|')
    split_df=df.explode(column)
    return split_df

