import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preprocessing_data.utils import find_common_item
import ast
df = pd.read_csv("./../dataset/result.csv")
dup = df[df.duplicated(subset=["name"],keep=False)]
dup.to_csv("./../dataset/dup.csv",index=False)