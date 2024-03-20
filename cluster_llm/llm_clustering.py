import pandas as pd
from openai import OpenAI
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preprocessing_data.extract_ctr import *
from common.static.config import config
from preprocessing_data.utils import *
from load_dataset import load_data
def get_translated(client, name, prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

import fasttext
model = fasttext.load_model(path='./../dataset/lid_176.bin')

result = model.predict('张斐泓', k=2)
print(result)





# prompt = """
#     i'll give you a name, and you should convert it in korean.
#     For example, if I give 'Ju Hwi LEE',  you should answer '이주휘'.
#     Never answer anything else except name.
#     Given name is [NAME].
#     """

# model = "gpt-3.5-turbo"
# openai_api_key = config['KEY']['openai_api_key']
# client= OpenAI(api_key=openai_api_key)




# if __name__ == "__main__":
#     df = pd.read_csv("./../dataset/result.csv")

#     foreign_df = pd.read_csv("./../dataset/for_inv.csv")
#     foreign_df = explode_split(foreign_df,"발명자")
#     foreign_df= foreign_df.head(10)
#     for_name_list = foreign_df["발명자"].to_list()
#     for name in for_name_list:
        
#         result= get_translated(client, name, prompt.replace("[NAME]",name))
#         #translated 표 만들고, 작업? or 하나하나 받아가면서 작업? llm 쓰는게 맞긴함?  
#         load_data()

