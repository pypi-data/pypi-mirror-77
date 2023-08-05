# PandasGui

A GUI built with PyQt5 for analyzing Pandas DataFrames.

<img src="https://raw.githubusercontent.com/adamerose/pandasgui/develop/screenshots/dataframe.png" alt="Screenshot" width="500"/>

## Installation

Install from PyPi:

```python
pip install pandasgui
```

Install directly from Github for the latest changes:

```python
pip install git+https://github.com/adamerose/pandasgui.git
```

## Usage
Create and view a simple DataFrame
```python
import pandas as pd
from pandasgui import show

example_df = pd.DataFrame(([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), columns=['a', 'b', 'c'])

show(example_df, settings={'block': True})
```

View all sample datasets
```python
from pandasgui import show
from pandasgui.datasets import all_datasets

show(**all_datasets, settings={'block': True})
```

The `settings={'block': True}` flag blocks code execution until the GUI window is closed, and can be omitted when working in iPython.

## About
This project is still in version 0.x.y and subject to major changes. Issues, feedback and forks are welcome. 
Latest changes will be on the develop branch, and this will be occasionally merged to master as a release with a
tag indicating the version number, and this will be what is available on PyPi.

## Features
- View DataFrames and Series
- Interactive plotting
- Statistics summary
- MultiIndex support
- Cell editing and copy / paste
- Import CSV files with drag & drop


## Screenshots
DataFrame Viewer  

<img src="https://raw.githubusercontent.com/adamerose/pandasgui/develop/screenshots/dataframe.png" alt="Screenshot" width="500"/>

Statistics  

<img src="https://raw.githubusercontent.com/adamerose/pandasgui/develop/screenshots/statistics.png" alt="Screenshot" width="500"/>

Grapher  

<img src="https://raw.githubusercontent.com/adamerose/pandasgui/develop/screenshots/grapher.png" alt="Screenshot" width="500"/>

MultiIndex Support  

<img src="https://raw.githubusercontent.com/adamerose/pandasgui/develop/screenshots/multi_index.png" alt="Screenshot" width="500"/>