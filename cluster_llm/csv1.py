import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preprocessing_data.utils import find_common_item
import ast
df = pd.read_csv("./../dataset/result.csv")

def find_common_applicant(df):
    new_records = []

    # DataFrame을 행 단위로 순회
    for index, row in df.iterrows():
        name = row['name']
        records = ast.literal_eval(row['record'])
        common_applicant = None

        # 이전 레코드와 비교하여 겹치는 applicant 찾기
        for prev_index, prev_row in df.iloc[:index].iterrows():
            prev_records = ast.literal_eval(prev_row['record'])
            for prev_record in prev_records:
                for record in records:
                    if 'applicant' in prev_record and 'applicant' in record:  # applicant 비교
                        common = find_common_item(prev_record['applicant'], record['applicant'])
                        if common != "No":
                            common_applicant = common

        # 겹치는 applicant가 있으면 해당 값으로 수정
        if common_applicant:
            for record in records:
                record['applicant'] = common_applicant

        new_records.append({'name': name, 'record': records})

    # 수정된 레코드를 DataFrame으로 변환하여 반환
    new_df = pd.DataFrame(new_records)
    return new_df


df= find_common_applicant(df)
df.to_csv("./../dataset/result2.csv",index=False)