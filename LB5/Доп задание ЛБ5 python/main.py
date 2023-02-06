import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("BestTask.csv", low_memory=False, delimiter=";")
t = sns.catplot(x = "<DATE>",
            y = "<VALUE>",
            hue = "<TYPE>",
            kind='box',
            data = df);
plt.xlabel('')
plt.ylabel('')
sns.move_legend(t, "upper right", title='')
plt.show()