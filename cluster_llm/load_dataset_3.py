import pandas as pd
import sys
import numpy as np
import os
import datetime
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from openai import OpenAI
from common.static.config import config
from preprocessing_data.extract_ctr import extract_samename_list, extract_kr , merge_to_csv
from preprocessing_data.utils import get_datetime_by_applicant, get_data_by_name, str_to_datetime, datetime_to_str

kr_samename=pd.read_csv("./../dataset/kr_samename.csv")
db_applicant= pd.read_csv("./../dataset/db_applicant.csv")
model = "gpt-3.5-turbo"
question = "hi"

openai_api_key = config['KEY']['openai_api_key']
client= OpenAI(api_key=openai_api_key)
name_list= kr_samename["발명자"].to_list()
applicant_list = kr_samename["출원인"].to_list()
date_list = kr_samename["출원일"].to_list()
address_list = kr_samename["주소"].to_list()
# name_list_db=db_applicant["name"].to_list()
# applicant_list_db = [db_applicant["Record"].to_list()]
name_list_db=db_applicant["name"].to_list()
applicant_list_db = []


try:
    for name, applicant, date, address in zip(name_list, applicant_list, date_list, address_list):
        x = str_to_datetime(date)
        dif_1m = relativedelta(months=1)

        # applicant_list_db가 비어있는지 확인
        if not applicant_list_db:
            applicant_list_db.append({
                "name": name,
                "record": [
                    {
                        "applicant": applicant,
                        "address": address,
                        "start": date,
                        "end": datetime_to_str(x + dif_1m)
                    }
                ]
            })
            continue
        else:
            # applicant_list_db에 name이 존재하는지 확인
            inventor_dict = next((d for d in applicant_list_db if d['name'] == name), None)
            if not inventor_dict:
                # name이 없는 경우
                applicant_list_db.append({
                    "name": name,
                    "record": [
                        {
                            "applicant": applicant,
                            "address": address,
                            "start": date,
                            "end": datetime_to_str(x + dif_1m)
                        }
                    ]
                })
                continue
            else:
                # name이 존재하는 경우
                matched_record = next((r for r in inventor_dict['record'] if r['applicant'] == applicant), None)

                if matched_record:
                    # 같은 출원인인 경우
                    if x + dif_1m > get_datetime_by_applicant(inventor_dict['record'], applicant, "end"):
                        matched_record["end"] = datetime_to_str(x + dif_1m)
                        continue
                    elif x <= get_datetime_by_applicant(inventor_dict['record'], applicant, "start"):
                        matched_record["start"] = datetime_to_str(x - dif_1m)
                        continue
                else:
                    #같은 출원인이 아니고, 날짜가 겹치는 경우 동명이인판정 부분 빠진 것 같음.
                    # 새로운 출원인인 경우
                    # inventor_dict['record'].append({
                    #     "applicant": applicant,
                    #     "address": address,
                    #     "start": date,
                    #     "end": datetime_to_str(x + dif_1m)
                    # })
                    # print(name)
                    # 주소 병합 로직
                    case2 = next((r for r in inventor_dict['record'] if r['applicant'] != applicant), None)
                    if case2:
                        address2 = case2["address"]
                        message = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "user",
                                    "content": f"I'll give two address to you, and you have to find common address. If there is no common address, you have to answer just 'No', don't say other words. If there is a common address, just answer that common address, for example :'경기도 화성시 메타폴리스로 47-7, 1001호 (반송동, 서해더블루)'Here is first addresses{address}, and here is second addresses{address2}",
                                }
                            ],
                            model="gpt-3.5-turbo",
                        )
                        result = message.choices[0].message.content
                        if result != "No": #주소일치 yes 파트
                            case2["address"]= result
                            inventor_dict['record'].append({
                                "applicant": applicant,
                                "address": address,
                                "start": date,
                                "end": datetime_to_str(x + dif_1m)
                            })
                            continue
                            
                        else:# 주소일치의 no 파트
                            applicant_list_db.append({
                                "name": name,
                                "record": [
                                    {
                                        "applicant": applicant,
                                        "address": address,
                                        "start": date,
                                        "end": datetime_to_str(x + dif_1m)
                                    }
                                ]
                            })
                            continue
except:
    result_df = pd.DataFrame(columns=["name", "record"])
    result_df["name"] = [d["name"] for d in applicant_list_db]

    # "record" 열을 문자열로 변환하여 저장
    result_df["record"] = [str(d["record"]) for d in applicant_list_db]
    

    result_df.to_csv("./../dataset/result2.csv",index=False,encoding="utf8")
























# # df = pd.read_excel("./../dataset/skey_inv.xlsx")
# # df2 = pd.read_excel("./../dataset/skey_pat.xlsx")
# # df = extract_kr(df)
# # df = merge_to_csv(df,df2,"skey", "출원일")
# # df.to_csv("./../dataset/kr_korean_inv.csv",index=False)





