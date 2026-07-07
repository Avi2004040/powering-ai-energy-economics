## note on avgprice_annual.xlsx (EIA)

this file is RETAIL ELECTRICITY prices (cents/kWh) by state, 1990-2020.
NOT natural gas fuel prices. i mixed these up at first.

- it's what consumers PAY per kWh of finished electricity (output side)
- for fossil LCOE i need gas FUEL price in $/MMBtu (input side) - different thing
- get Henry Hub $/MMBtu from EIA separately for Block 3

still useful though:
- sanity check - retail price should be HIGHER than my busbar LCOE
  (because retail includes delivery + margin, LCOE doesn't)
- convert: cents/kWh x 10 = $/MWh  (e.g. US total 2020 = 10.59 -> ~$105/MWh)

columns: Year, State, Industry Sector Category, then price cols
(Residential/Commercial/Industrial/Transportation/Other/Total).
'Other' col is all NA, 'Transportation' mostly 0 - ignore those.
'US' row = national avg. 'Total Electric Industry' = all providers combined.

## my LCOE formula verified
crf(), fcr(), lcoe() in src/lcoe.py.
tested against NREL PV sample -> got 39.78 $/MWh vs their 39.03 (~2% off).
difference is just my test input values being approximate, not the formula.
formula chain (crf->fcr->lcoe) confirmed correct.
TODO optional: pull exact PV inputs from ATB PV sheet to match 39.03 to the cent.