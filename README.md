# zerodhacapitalgaintax-2024-25
Calculate  Capital Gain tax  for 2024-25 from Zerodha Tax P&L

This small program calculates capital gain tax from the zerodha tax P&L for  the financial year 2024-25. There is a difference in rates as the rates hikes are proposed in July. This program considers LTCG  as 12.5 as the exemption is different after the new rate  introdution.

Need python installed


### Setup  Virtual Environment

a. Create a virtual environment for the first time

```bash
python -m venv capital_gains
```

b. Activate the virtual environment

```bash
source capital_gains/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

### Run the python program

1. Run the program

```bash
python calculate_tax.py
```

2. Access the following url through browser and upload the report and press submit to see the result.

http://127.0.0.1:7860/