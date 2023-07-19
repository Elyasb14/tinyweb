import pandas as pd
import os

bme680_files = [file for file in sorted(os.listdir('data')) if file.endswith("bme680.csv")]
for file in bme680_files:
  df = pd.read_csv(f'data/{file}')  
  df.drop(df[df["temp (c)"].astype(float) <= -25].index, inplace=True)
  df.drop(df[df["temp (c)"].astype(float) >= 60].index, inplace=True)
  # print(df["temp (c)"].min())
  df.to_csv(f"data/{file}")
