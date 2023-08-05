This library is used to plot histograms for all columns at a time.
we just have to give one parameter which is our "dataframe"
for example,
your csv file name is "train.csv" ||
then your code will be ||
from getallhistograms import histograms ||
data=pd.read_csv("train.csv") ||
histograms(data) ||
we will get all histograms