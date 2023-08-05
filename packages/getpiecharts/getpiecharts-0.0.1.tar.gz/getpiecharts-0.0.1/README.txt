This library is used to plot pie charts for all columns at a time having data type "objective".
we just have to give one parameter which is our "dataframe"
for example
your csv file name is "train.csv"

from getpiecharts import piecharts
data=pd.read_csv("train.csv")
piecharts(data)

we will get all pie charts