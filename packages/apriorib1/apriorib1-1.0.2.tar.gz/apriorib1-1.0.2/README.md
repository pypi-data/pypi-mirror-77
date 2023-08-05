# apriorib1

apriorib1 is a Python library that applies the very famous unsupervised learning algorithm, apriori, for Association Rule Mining(ARM) on a dataset of transaction/purchase logs and shows the accepted association rules. 

Currently, this version is limited to a maximum of 4 items in a certain transaction.

![Demo](https://user-images.githubusercontent.com/49288068/90564473-10814100-e1c3-11ea-81c4-4a5a37abff75.png)

## New in this version

1. Displays stage-wise final itemset as pandas DataFrames.

![Demo 2](https://user-images.githubusercontent.com/49288068/90564809-8d141f80-e1c3-11ea-8e2c-d81c08567643.png)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install apriorib1.

```bash
pip install apriorib1
```

## Quick Start

```python
from apriorib1 import Apriori

data = [['MILK', 'BREAD', 'BISCUIT'],
    ['BREAD', 'MILK', 'BISCUIT', 'CORNFLAKES'],
    ['BREAD', 'TEA', 'BOURNVITA'],
    ['JAM', 'MAGGI', 'BREAD', 'MILK'],
    ['MAGGI', 'TEA', 'BISCUIT'],
    ['BREAD', 'TEA', 'BOURNVITA'],
    ['MAGGI', 'TEA', 'CORNFLAKES'],
    ['MAGGI', 'BREAD', 'TEA', 'BISCUIT'],
    ['JAM', 'MAGGI', 'BREAD', 'TEA'],
    ['BREAD', 'MILK'],
    ['COFFEE', 'COCK', 'BISCUIT', 'CORNFLAKES'],
    ['COFFEE', 'COCK', 'BISCUIT', 'CORNFLAKES'],
    ['COFFEE', 'SUGER', 'BOURNVITA'],
    ['BREAD', 'COFFEE', 'COCK'],
    ['BREAD', 'SUGER', 'BISCUIT'],
    ['COFFEE', 'SUGER', 'CORNFLAKES'],
    ['BREAD', 'SUGER', 'BOURNVITA'],
    ['BREAD', 'COFFEE', 'SUGER'],
    ['BREAD', 'COFFEE', 'SUGER'],
    ['TEA', 'MILK', 'COFFEE', 'CORNFLAKES']]

# Testing the Apriori class
apr = Apriori(records=data,min_sup=2,min_conf=50)
df1,df2,df3,df4 = apr.show_as_df(stage=1),apr.show_as_df(stage=2),apr.show_as_df(stage=3),apr.show_as_df(stage=4)
print("VIEWING THE ITEMSET DATAFRAMES AT THE DIFFERENT STAGES :\nSTAGE 1\n{}\nSTAGE 2\n{}\nSTAGE 3\n{}\nSTAGE 4\n{}".format(df1,df2,df3,df4))
apr.checkAssc()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)