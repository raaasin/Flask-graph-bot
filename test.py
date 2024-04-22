import os
import pandas as pd
from pandasai import Agent
import warnings
warnings.filterwarnings("ignore")


agent = Agent(pd.read_csv("uploads/GroceryDataset.csv"))
response=agent.chat(
    "what's the average price of Bakery & Desserts")
print(response)