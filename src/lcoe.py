#LCOE Engine
#define key formulas
#Function 1: Capital Recovery Factor (CRF): Annualizes capex: The formula (from my TEA work):
# CRF = wacc / (1 - 1/(1+wacc)^years)
def crf(wacc_real,crp_years):
    return (wacc_real/(1-1/(1+wacc_real)**crp_years))

#Function 2:Fixed Charge Rate (FCR): FCR=CRF*ProFinFactor
def fcr(wacc_real,crp_years,pro_fin_factor):
    return crf(wacc_real,crp_years)*pro_fin_factor

#Function 3: Levelized Cost of Energy (LCOE): LCOE = ((FCR*CAPEX+FOM)*1000)/(CF*8760)+VOM+Fuel:
# capex = overnight-ish capital cost, $/kW
    # fom   = fixed O&M, $/kW-yr
    # cf    = capacity factor, fraction (0.85 = runs 85% of the time)
    # vom   = variable O&M, $/MWh
    # fuel  = fuel cost, $/MWh
    # 8760  = hours in a year
def lcoe(wacc_real,crp_years,pro_fin_factor,capex,fom,cf,vom,fuel):
    this_fcr=fcr(wacc_real,crp_years,pro_fin_factor)
    capital_and_fixed=((this_fcr*capex+fom)*1000)/(cf*8760)
    return capital_and_fixed+vom+fuel

# verify against NREL's PV sample
# NREL PV example inputs (2022 USD):
test = lcoe(
    wacc_real=0.041,      # real WACC for the PV sample
    crp_years=30,
    pro_fin_factor=1.0,
    capex=1327,           # $/kW
    fom=16,               # $/kW-yr
    cf=0.2688,            # capacity factor
    vom=0,                # $/MWh
    fuel=0,               # solar has no fuel
)
print(test)

