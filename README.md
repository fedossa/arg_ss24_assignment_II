# Accounting Reading Group - Assignment II

## P/B Ratios And Future Residual Income

This repository contains the code and data for the second assignment of the Accounting Reading Group. It is implemented in Python and uses the `pandas`, `openpyxl` and `jupyter` libraries.


### How Do I create the output?

Assuming that you have Python installed, this should be relatively straightforward.

1. It is recommend to create a virtual environment for the project. Please do this and activate the virtual environment.

```shell
python3 -m venv venv
source venv/bin/activate # On Linux and Mac OS
# venv\Scripts\activate.bat # If you are using Windows - command prompt
# venv/Script/Activate.ps1 # If you are using Windows - PowerShell and have allowed script execution
```

2. Install the required packages by running `pip install -r requirements.txt` in the terminal. This will install the required packages for the project in the virtual environment.

3. Download the `wscp_static.txt` and `wscp_panel.xlsx` files provided on moodle and place them in the `data/external/` directory (create the `external` directory if it does not exist). We do not provide these files in the repository because they are proprietary data and this repository is intended to be public.

4. If you have make installed, you can run `make all` in the terminal. This will create the output files in the `output` directory. Otherwise, you can run the following commands in the terminal:

```shell
python code/python/do_analysis.py
quarto render doc/paper.qmd
mv doc/paper.pdf output
rm -f doc/paper.ttt doc/paper.fff
quarto render doc/presentation.qmd
mv doc/presentation.pdf output
rm -f doc/presentation.ttt doc/presentation.fff
```

This will create both the paper and the presentation in the `output` directory.