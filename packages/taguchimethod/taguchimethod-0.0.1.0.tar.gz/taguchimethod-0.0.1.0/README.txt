This library is used to find best level of control factors using taguchi method.
Two things you need to use this library. First you have to select which array you want to use. I have given my github link.
There you wil see different orthogonal arrays csv file. You have to select your choise load this csv file into pandas dataframe.
second thing you need is your experimental results which you get from experiments by conducting them according to your selected array.
(For reference I have given "result.csv" file of "thickness of aluminium layer on silicon wafers" in github link.This result get from experiments conducted according to
L16 (2^15) array)
Then you have to load this csv file as pandas dataframe.

for example,
your selected array csv file name is "L16 (2^15).csv" and
results csv file is "result.csv"||
number of levels in your array used are "2"||
column number corresponding to your control factor is "1"||
then your code will be ||
from taguchimethod import getresults_levelwise ||
data=pd.read_csv("L16 (2^15).csv") ||
results=pd.read_csv("result.csv") ||
getresults_levelwise(data,1,2,results)||
we wil get results levelwise||
if output is [0.866 1.26] then it means if you use level "1" for your selected control factor then you will get result 0.866 and for level "2"
yuo will get 1.26||
github_link=https://github.com/akashsathe ||
medium link=https://medium.com/@akashsathe79 ||
I am going to publish a article about this method on medium.