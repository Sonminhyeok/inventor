import pandas as pd

df= pd.read_excel("./../dataset/kr_korean_inv.xlsx")
df = df["발명자"].explode("|")
df = df.sort_values(by="발명자")
df.to_csv("./../dataset/kr_korean_inv.csv",index=False)