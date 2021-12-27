"""
Functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


@iterate_jit(nopython=True)
def Net_accounting_profit(Revenues, Other_revenues, Expenses, Net_accounting_profit):
    """
    Compute accounting profit from business
    """
    Net_accounting_profit = Revenues + Other_revenues - Expenses
    return Net_accounting_profit


@iterate_jit(nopython=True)
def Total_additions_to_GP(Donations_NGO, Donations_Others, Donations_Govt, Other_additions, Total_additions_to_GP):
    """
    Compute accounting profit from business
    """
    Total_additions_to_GP = Donations_NGO + Donations_Others + Donations_Govt + Other_additions
    return Total_additions_to_GP

@iterate_jit(nopython=True)
def Total_taxable_profit(Net_accounting_profit, Total_additions_to_GP, Total_taxable_profit):
    """
    Compute total taxable profits afer adding back non-allowable deductions.
    """
    Total_taxable_profit = Net_accounting_profit + Total_additions_to_GP
    return Total_taxable_profit

@iterate_jit(nopython=True)
def Tax_depreciation(Tax_depreciation, Tax_depr):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Tax_depr = Tax_depreciation
    return Tax_depr

@iterate_jit(nopython=True)
def Total_deductions(Tax_depr, Other_deductions, Donations_Govt, Donations_Govt_rate, Total_deductions):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Total_deductions = Tax_depr + Other_deductions + Donations_Govt_rate*Donations_Govt
    return Total_deductions

@iterate_jit(nopython=True)
def Net_taxable_profit(Total_taxable_profit, Total_deductions, Net_taxable_profit):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Net_taxable_profit = Total_taxable_profit - Total_deductions
    return Net_taxable_profit

@iterate_jit(nopython=True)
def Donations_allowed(Donations_NGO, Donations_Others, Donations_NGO_rate, Net_taxable_profit, Donations_Others_rate, Donations_allowed):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Donations_allowed = min(Donations_NGO, max(0, Donations_NGO_rate*Net_taxable_profit)) + Donations_Others_rate*Donations_Others
    #Donations_allowed = Donations_NGO + Donations_Others_rate*Donations_Others
    return Donations_allowed

@iterate_jit(nopython=True)
def Carried_forward_losses(Carried_forward_losses, CF_losses):
    """
    Compute net taxable profits afer allowing deductions.
    """
    CF_losses = Carried_forward_losses
    return CF_losses

@iterate_jit(nopython=True)
def Tax_base(Net_taxable_profit, Donations_allowed, CF_losses, Tax_base):
    """
    Compute net tax base afer allowing donations and losses.
    """
    Tax_base = Net_taxable_profit - Donations_allowed - CF_losses
    return Tax_base

@iterate_jit(nopython=True)
def Net_tax_base(Tax_base, cit_rate_oil, Sector, Exemptions, Investment_incentive, Net_tax_base):
    """
    Compute net tax base afer allowing donations and losses.
    """
    if Sector == 2:
        Net_tax_base = Tax_base/(1 - cit_rate_oil)
    else:
        Net_tax_base = Tax_base - Exemptions - Investment_incentive
    return Net_tax_base


@iterate_jit(nopython=True)
def Net_tax_base_Egyp_Pounds(Net_tax_base, Exchange_rate, Net_tax_base_Egyp_Pounds):
    """
    Compute net tax base afer allowing donations and losses.
    """
    Net_tax_base_Egyp_Pounds = Net_tax_base * Exchange_rate
    return Net_tax_base_Egyp_Pounds

DEBUG = False
DEBUG_IDX = 0


@iterate_jit(nopython=True)
def cit_liability(cit_rate_oil, cit_rate_other, Sector, Net_tax_base_Egyp_Pounds, citax):
    """
    Compute tax liability given the corporate rate
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = max(Net_tax_base_Egyp_Pounds, 0)
    if Sector == 2:
        citax = cit_rate_oil * taxinc
    else:
        citax = cit_rate_other * taxinc
    
    return citax
