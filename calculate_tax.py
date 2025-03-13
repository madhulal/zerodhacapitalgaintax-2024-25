import gradio as gr
import pandas as pd


start_row=15
sheet_name='Tradewise Exits from 2024-04-01'

period_of_holding_column='Period of Holding'

short_term_cg_before_rate=0.156
short_term_cg_rate=0.208

taxable_profit_column='Taxable Profit'
long_term_cg_rate=0.130
long_term_cg_exemption=125000


def calculate_ltcg_tax(output,df):
    long_term_capital_gain=df[taxable_profit_column].sum()
    output += f"Long Term Capital Gain: {long_term_capital_gain}\n"
    long_term_cg_tax = 0.0
    if(long_term_capital_gain > long_term_cg_exemption):
        long_term_cg_tax = (long_term_capital_gain-long_term_cg_exemption)*long_term_cg_rate
    output += f"LTCG Tax Due: {long_term_cg_tax}\n"

    return output,long_term_cg_tax

def calculate_stcg_before_tax(output,df):
    short_term_capital_gain=df[taxable_profit_column].sum()
    output += f"Short Term Capital Gain Before July 2024: {short_term_capital_gain}\n"

    short_term_cg_tax = short_term_capital_gain * short_term_cg_before_rate
    output += f"STCG Tax Due(Before): {short_term_cg_tax}\n"

    return output, short_term_cg_tax

def calculate_stcg_after_tax(output, df):
    short_term_capital_gain=df[taxable_profit_column].sum()
    output += f"Short Term Capital Gain After July 2024: {short_term_capital_gain}\n"

    short_term_cg_tax = short_term_capital_gain * short_term_cg_rate
    output += f"STCG Tax Due(After): {short_term_cg_tax}\n"

    return output, short_term_cg_tax


def process_excel(file):

   # Read the Excel file
    xls = pd.ExcelFile(file.name)

    df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=start_row - 1)
    
    # Initialize a list to store rows
    rows = []
    
    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        # Check if the row is blank (all values are NaN)
        if row.isna().all():
            break  # Stop processing if a blank row is encountered
        rows.append(row)
    
    # Convert the collected rows back to a DataFrame
    filtered_df = pd.DataFrame(rows)
    filtered_df = filtered_df.iloc[: , 1:]

    output = f"=========================================================\n"

    longterm_df=filtered_df[filtered_df[period_of_holding_column] > 365]

    output, long_term_cg_tax=calculate_ltcg_tax(output, longterm_df)
    # output += f"LTCG Tax Due: {long_term_cg_tax}\n"

    output += f"=========================================================\n"

    shorterm_df=filtered_df[filtered_df[period_of_holding_column] <= 365]
    
    shorterm_before_df=shorterm_df[shorterm_df['Exit Date']<='2024-07-22']

    output,short_term_cg_tax1=calculate_stcg_before_tax(output, shorterm_before_df)

    shorterm_after_df=shorterm_df[shorterm_df['Exit Date']>'2024-07-22']

    output, short_term_cg_tax2=calculate_stcg_after_tax(output, shorterm_after_df)

    output += f"STCG Tax Due: {short_term_cg_tax1+short_term_cg_tax2}\n"
    output += f"=========================================================\n"

    output += f"Total Capital Gain: {long_term_cg_tax+short_term_cg_tax1+short_term_cg_tax2}\n"

    return output

# Create a Gradio interface
iface = gr.Interface(
    fn=process_excel,  # Function to process the file
    inputs=gr.File(label="Upload the Tax P&L for 2024-25"),  # File input component
    outputs="text",  # Output as text
    title="Capital Gain Calculator for 2024-25",
    description="Upload a file and see the  tax liability"
)

# Launch the interface
iface.launch()