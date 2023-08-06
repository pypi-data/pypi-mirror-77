### Description
This is an easy to use library to encode categorical data in a feature into optimized set of 
features with each categorical value mapping to a unique bitstring.

```sh
>>> import optiEncoder
>>> enc = optiEncoder.Encoder(["France","Canada","England"])
>>> print("Mappings : ", enc.getMappings())
{'France':[0,0],'Canada':[0,1],'England':[1,0]}
>>> print("Encoded List : ", enc.getEncodedList())
[[0,0],[0,1],[1,0]]
```

### Usage in Data Preprocessing
```sh
>>> import optiEncoder
>>> import pandas
>>> d = pd.read_csv('data.csv').dropna()
        Performance Measure  BRATS 2018  
0          Dice Coefficient       90  
1       Jaccard Coefficient       80  
2            Area under ROC       90  
4        Hausdorff Distance       10  
5               Sensitivity       90  
6               Specificity       90  
7                 F-Measure       90  
8                 Precision       80  
9   Vol Similarity Distance       90  
10                  Fallout        7  
12                       TP     1900  
13                       FP      200  
14                       TN     2500  
15                       FN      600  

>>> enc = optiEncoder.Encoder(list('Performance Measure'))
>>> enc.getEncodedList()
[[1, 0, 0, 1], [1, 1, 0, 0], [1, 0, 0, 0], [0, 1, 1, 1], [0, 1, 0, 0], [1, 0, 0, 0], [0, 1, 1, 0], [1, 0, 1, 0], [0, 0, 1, 1], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0]]
>>> d = d.iloc[:,1:]
>>> d
    BRATS 2018  
0        90  
1        80  
2        90  
4        10  
5        90  
6        90  
7        90  
8        80  
9        90  
10        7  
12     1900  
13      200  
14     2500  
15      600  

>>> encodedList = enc.getEncodedList()
>>> for i in range(0,len(encodedList[0])):
...     d[str(i)]=pd.DataFrame(encodedList).iloc[:,i]
...
>>> d
    BRATS 2018  0  1  2  3
0        90  1  0  0  1
1        80  1  1  0  0
2        90  1  0  0  0
4        10  0  1  0  0
5        90  1  0  0  0
6        90  0  1  1  0
7        90  1  0  1  0
8        80  0  0  1  1
9        90  1  0  1  1
10        7  1  1  0  0
12     1900  0  0  1  0
13      200  1  1  0  0
14     2500  1  0  1  0
15      600  0  1  0  1

```

### License
MIT
### Author
Sahil Ahuja
