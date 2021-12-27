import json as json
import pandas as pd
import numpy as np


def Total_taxable_profit(Net_accounting_profit, Donations_NGO, Donations_Others,\
                        Other_additions):
    """
    Compute total taxable profits afer adding back non-allowable deductions.
    """
    Total_taxable_profit = Net_accounting_profit + Donations_NGO + Donations_Others + \
                           Other_additions
    return Total_taxable_profit

Total_taxable_profit(100,20,25,45)