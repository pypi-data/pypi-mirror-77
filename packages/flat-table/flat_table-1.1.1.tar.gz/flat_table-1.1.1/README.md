## Flat-Table: Dictionary and List Normalizer

This package is a normalizer for [pandas](https://pandas.pydata.org/) dataframe objects that has dictionary or list objects within it's columns. The library will expand all of the columns that has data types in (list, dict) into individual seperate rows and columns.

PS: Flat table will use the current index of the dataframe as an identifier while expanding lists. The output will have an index column of your original dataframe. You can drop it later if you not plan to use it.

### To Install

To install, use pip.

```
pip install flat-table
```

### How to Use It

From a given pandas dataframe, the `index` of the dataframe will be used to create seperate columns and rows. 

``` python
# some dataframe contains dicts and lists in it's columns
df = ...
```

``` python
import flat_table

flat_table.normalize(df)
```

This will give you all the keys in dictionaries as columns, and all the lists as seperate rows.

### Example Illustration

Lets assume that you have a dataframe of the followings shape.


id | user_info | address
-- | --------- | ------ |
1001 | { 'first_name': 'john', 'last_name': 'smith', 'phones': {'mobile': '201-..', 'home': '978-..'} }| [{ 'zip': '07014', 'city': 'clifton' }] |
1002 | NaN| [{'zip': '07014', 'address1': '1 Journal Square'}]|
1003 | { 'first_name': 'marry', 'last_name': 'kate', 'gender': 'female'  } | [{ 'zip': '10001', 'city': 'new york' }, { 'zip': '10008', 'city': 'brooklyn' }]|


This table given above has some dictionaries and lists in it's columns. Normally, what you would do is to use `pd.io.json.json_normalize` function to expand dictionaries. However, in cases you have `NaN` values in your column, `pd.io.json.json_normalize` end up throwing an `AttributeError` error for `NaN` values because they are not of the same type. `flat_table` is a wraper around the `json_normalize` function where it expands it's abilities to be more robust for `NaN` values and also, it expands lists rowwise so that it will be more clear to see the information.

For the above table, the flatten table after applying `flat_table.normalize` will look like the following.

|    |   index |   id | user_info.gender   | user_info.phones.home   | user_info.phones.mobile   | user_info.last_name   | user_info.first_name   | address.address1   | address.city   |   address.zip |
|---:|--------:|-----:|:-------------------|:------------------------|:--------------------------|:----------------------|:-----------------------|:-------------------|:---------------|--------------:|
|  0 |       0 | 1001 | nan                | 978-..                  | 201-..                    | smith                 | john                   | nan                | clifton        |         07014 |
|  1 |       1 | 1002 | nan                | nan                     | nan                       | nan                   | nan                    | 1 Journal Square   | nan            |         07014 |
|  2 |       2 | 1003 | female             | nan                     | nan                       | kate                  | marry                  | nan                | new york       |         10001 |
|  3 |       2 | 1003 | female             | nan                     | nan                       | kate                  | marry                  | nan                | brooklyn       |         10008 |

### New in Version 1.1.0

The expansion for dicts and lists made optional. Now, you can choose to expand list types and dict types with normalize function.

``` python
flat_table.normalize(df, expand_dicts=False, expand_lists=True)
```

Normalized version of df will be following.

|    |   index |   id | user_info                                                                                      | address.address1   | address.city   |   address.zip |
|---:|--------:|-----:|:-----------------------------------------------------------------------------------------------|:-------------------|:---------------|--------------:|
|  0 |       0 | 1001 | {...} | nan                | clifton        |         07014 |
|  1 |       1 | 1002 | nan                                                                                            | 1 Journal Square   | nan            |         07014 |
|  2 |       2 | 1003 | {...}                               | nan                | new york       |         10001 |
|  3 |       2 | 1003 | {...}                               | nan                | brooklyn       |         10008 |

### How it Works?

Basically, `flat_table` will look for each of the series in a dataframe to understand what type of data it contains. 

For every series, it creates a list of information on how to expand it. It will go into all dictionaries and all lists in all levels and expand them as rows and columns. Dictionary `keys` will be used for column names, and The `index` of the giden dataframe will be used for row expansion.

If you want to see how the columns are mapped, you can use `flat_table.mapper` function to get all information about your columns in your original dataframe. For example, for the above table, the mapper function will provide the following table.

|    | parent    | child                   | type   | obj   |
|---:|:----------|:------------------------|:-------|:------|
|  0 | .         | id                      | int    | ...   |
|  1 | .         | user_info               | dict   | ...   |
|  2 | user_info | user_info.gender        | str    | ...   |
|  3 | user_info | user_info.phones.home   | str    | ...   |
|  4 | user_info | user_info.phones.mobile | str    | ...   |
|  5 | user_info | user_info.last_name     | str    | ...   |
|  6 | user_info | user_info.first_name    | str    | ...   |
|  7 | .         | address                 | list   | ...   |
|  8 |           | address                 | dict   | ...   |
|  9 | address   | address.address1        | str    | ...   |
| 10 | address   | address.city            | str    | ...   |
| 11 | address   | address.zip             | str    | ...   |

## Licence

Licence is use it at your own will, with whatever way you want it to use :smiley:.

## Author

Build by [@metinsenturk](https://github.com/metinsenturk/)