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
def Tax_base_CF_losses(Net_taxable_profit, Donations_allowed, Loss_CFLimit, 
    Loss_lag1, Loss_lag2, Loss_lag3, Loss_lag4, Loss_lag5, Loss_lag6, Loss_lag7, Loss_lag8,
    newloss1, newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8, Tax_base):
    
    """
    Compute net tax base afer allowing donations and losses.
    """
    BF_loss = np.array([Loss_lag1, Loss_lag2, Loss_lag3, Loss_lag4, 
    Loss_lag5, Loss_lag6, Loss_lag7, Loss_lag8])
    print(BF_loss)
    N = int(Loss_CFLimit)
    BF_loss = BF_loss[:N]
    Gross_Tax_base = min(Net_taxable_profit, max((Net_taxable_profit - Donations_allowed), 0))
    
    if Gross_Tax_base < 0:
        CYL = abs(Gross_Tax_base)
        Used_loss = np.zeros(N)
        
    else:
        CYL = 0
        Cum_used_loss = 0
        Used_loss = np.zeros(N)
        for i in range(N, 0, -1):
            GTI = Gross_Tax_base - Cum_used_loss
            Used_loss[i-1] = min(BF_loss[i-1], GTI)
            Cum_used_loss += Used_loss[i-1]
    
    New_loss = BF_loss - Used_loss
        
    Tax_base = Gross_Tax_base - Used_loss.sum()

    newloss1 = CYL

    (newloss2, newloss3, newloss4, 
    newloss5, newloss6, newloss7, newloss8) = np.append(New_loss[:-1], np.zeros(8-N))

    return (Tax_base, newloss1, newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8)


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
