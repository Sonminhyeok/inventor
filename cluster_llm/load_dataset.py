import pandas as pd
import sys
import numpy as np
import os
import datetime
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from openai import OpenAI
from common.static.config import config
from preprocessing_data.extract_ctr import extract_samename, extract_kr , merge_to_csv
from preprocessing_data.utils import *

def load_data(kr_samename):

    db_applicant= pd.read_csv("./../dataset/db_applicant.csv")
    model = "gpt-3.5-turbo"
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
        result=1
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
                inventor_dicts = [d for d in applicant_list_db if d['name'] == name]
                if not inventor_dicts:
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
                    no_list=[]
                    for inventor_dict in inventor_dicts:
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
                            case2 = next((r for r in inventor_dict['record'] if r['applicant'] != applicant), None)
                            if case2:
                                previous_address = case2["address"]
                                result = find_common_address(address, previous_address)
                            if result != "No":
                                inventor_dict['record'].append({
                                    "applicant": applicant,
                                    "address": result,
                                    "start": date,
                                    "end": datetime_to_str(x + dif_1m)
                                })
                                continue
                            else:# 이름은 있지만, 출원인이 다르고 주소도 다른 경우 == 동명이인의 시작 문제는 inventor dict for문이 들어가면서, 
                                no_list.append(inventor_dict)#자기 for문 아닐때 추가하면서 개지랄남
                            if len(no_list)==len(inventor_dicts):
                                # 새로운 출원인인 경우, 기존 레코드에 추가하지 않고 새로운 레코드 생성                       
                                if result=="No":
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
                            
        result_df = pd.DataFrame(columns=["name", "record"])
        result_df["name"] = [d["name"] for d in applicant_list_db]

        # "record" 열을 문자열로 변환하여 저장
        result_df["record"] = [str(d["record"]) for d in applicant_list_db]
        

        result_df.to_csv("./../dataset/result.csv",index=False,encoding="utf8")
    except:
        result_df = pd.DataFrame(columns=["name", "record"])
        result_df["name"] = [d["name"] for d in applicant_list_db]

        # "record" 열을 문자열로 변환하여 저장
        result_df["record"] = [str(d["record"]) for d in applicant_list_db]
        

        result_df.to_csv("./../dataset/result_error.csv",index=False,encoding="utf8")

if __name__ == "__main__":
    df=pd.read_csv("./../dataset/kr_samename.csv")
    load_data(df)

    


    
    
    























# # df = pd.read_excel("./../dataset/skey_inv.xlsx")
# # df2 = pd.read_excel("./../dataset/skey_pat.xlsx")
# # df = extract_kr(df)
# # df = merge_to_csv(df,df2,"skey", "출원일")
# # df.to_csv("./../dataset/kr_korean_inv.csv",index=False)





