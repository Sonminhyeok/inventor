import re
import pandas as pd
def extract_kr(df):
    korean_pattern = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    kr_df = df[df["출원인국적"] == "KR"]
    kr_korean_df = kr_df[kr_df["발명자"].apply(lambda x: korean_pattern.search(x) is not None)]
    return kr_korean_df
def extract_samename_list(df):
    name_list = []
    for name in df["발명자"]:
        if isinstance(name, str) and "|" in name:
            name_list.extend(name.split("|"))
        else:
            name_list.append(name)
    duplicates = set([x for x in name_list if name_list.count(x) > 1])
    if duplicates:
        print(f"중복된 이름: {', '.join(duplicates)}")
    else:
        print("중복된 이름이 없습니다.")
def merge_to_csv(df1,df2,overlap_col, target_col):
    common_skeys = df2[df2[overlap_col].isin(df1[overlap_col])]
    merged_df = pd.merge(df1, df2, on=overlap_col, how='left')

    # 'skey'가 일치하는 행에 '출원일' 열 추가
    merged_df[target_col] = merged_df[target_col].fillna(merged_df[target_col])
    sorted_df = merged_df.sort_values(by='출원일')
    return sorted_df
    