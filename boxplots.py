#!/bin/python3
import pandas
import matplotlib.pyplot as plt

df1 = pandas.read_csv('results/result_sample_config_compress_7z.csv')
df2 = pandas.read_csv('results/result_sample_config_compress_bzip2.csv')

print(df1.head())
print(df2.head())

# TODO multi index combining all sample data comp
df_comp = pandas.DataFrame()

# TODO multi index combining all sample data comp
df_decomp = pandas.DataFrame()


plt.title('Time Taken by Classifier')
plt.xlabel('Time_Types')
plt.ylabel('Time_Value in (sec)')


df1.boxplot(by='file')
plt.show()
