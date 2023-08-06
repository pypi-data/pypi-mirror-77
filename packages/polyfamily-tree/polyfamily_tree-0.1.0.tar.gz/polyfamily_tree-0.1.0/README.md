
# polyfamily_tree
Python package for structuredly managing directional relationship between objects.  
  
Though it uses allegory of 'family tree', it doesn't implement 'tree data structure'.  
Alternatively, relationship in default is drawn by organizing Directed Acyclic Graph(DAG).  
This means that there is a loop-less hierarchy in between members.  
Not like tree, member of this data structure can have multiple parents  
thus the package is named 'poly'family  
  
Graph organizing members is not a concrete object.  
All participants store its vicinity relationship in itself.
By default relationship is build bidirectional - parent knows about children while  
children knows about parent. But this can be manually tweaked using  
lower level methods like `fm_append` `fm_remove`.  
  
Methods use prefix 'fm_' to be distinguished.  
  
## Installation
Use `pip` to install the package.  
`pip install polyfamily_tree`

## Usage
```python
from polyfamily_tree import *    
   
   
class MyMember(FamilyMember): # inherit `FamilyMember`  
    def __init__(self):
        super().__init__()    # vital for initiating required attributes  
        # your __init__ code below
        ...
        
a, b = MyMember(), MyMember()  
a.fm_append_member(parent=a, child=b) # build relationship
print(b.fm_get_parents())
```    

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.    
<https://github.com/grasshopperTrainer/polyfamily_tree>    

## Alternative contect
For any questions :    
<grasshoppertrainer@gmail.com>    
    
## Licence
MIT
