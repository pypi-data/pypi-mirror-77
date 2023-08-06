### Installation
This is an easy to use library to encode categorical data in a feature into optimized set of 
features with each categorical value mapping to a unique bitstring.

Installation : pip install python-optiEncoder
	
```sh
>>> import optiEncoder
>>> enc = optiEncoder.Encoder(["France","Canada","England"])
>>> print("Mappings : ", enc.getMappings())
{'France':[0,0],'Canada':[0,1],'England':[1,0]}
>>> print("Encoded List : ", enc.getEncodedList())
[[0,0],[0,1],[1,0]]
```
### License
MIT
### Author
Sahil Ahuja
