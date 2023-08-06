This library is used to plot boxplots for all columns at a time.
we have to give two parameters which are our "dataframe" and column name of output variable i.e our target
for example,
your csv file name is "train.csv" ||
then your code will be ||
from getboxplots import boxplots ||
data=pd.read_csv("train.csv") ||
your output variable column name is "SalePrice"||
boxplots(data,'SalePrice') ||
we will get all boxplots.||
I am goint to publish article about this library.check it on "medium link=https://medium.com/@akashsathe79"