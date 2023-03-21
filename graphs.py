import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read output file
df = pd.read_csv('./results/output3.txt', header=None)
print(df)