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

## gas price scenarios (Block 3)
using Henry Hub spot price data (EIA, data/raw/RNGWHHDm.xls) to JUSTIFY scenarios.
from pandas analysis, historical annual range: $2.03 - $8.86 /MMBtu (1997-2026).
recent volatility: 2022=$6.42, 2023-24=~$2.2 (record lows), 2025-26=~$3.5-3.9.

scenarios I will run for LCOE(treat as real 2022 $/MMBtu):
- LOW  = $2.19  (2024 annual avg - record inflation-adjusted low)
- MID  = $3.91  (2021 annual avg - normal pre-crisis year)
- HIGH = $6.42  (2022 annual avg - the energy-crisis spike)

CAVEAT: 
EIA prices are NOMINAL (actual $ of each year), so old years look
artificially low. I am NOT feeding raw historical prices into the engine - I use
them only to justify the scenario RANGE. The scenario values themselves are
treated as real 2022 $ to stay consistent with ATB's real-2022 cost basis.

## Block 3 firm-power comparison - assumptions
coal: heat rate 8.8 MMBtu/MWh + coal price $2/MMBtu = standard textbook values.
  (ATB coal sheet prints heat rate in confusing mislabeled units - used clean
  defaults instead. CF=0.85 baseload, our assumption.)
nuclear: uses 2030 costs (2022 blank). fuel bundled into VOM, so fuel=0.
geothermal: no fuel (earth's heat), CF from sheet (0.9), VOM=0.
gas CC: CF=0.87 baseload assumption, 3 fuel scenarios.
all: real WACC 4.1%, 30yr CRP, real 2022 $ (except nuclear = 2030 $).

@"

## Block 4 - 45Q carbon capture credit (policy inputs)
source: One Big Beautiful Bill Act (OBBBA), signed July 4 2025; IRS 45Q.
- point-source capture (power plant) + geologic storage = 85 USD/tonne CO2
- DAC = 180 USD/tonne (not relevant to us - we're point-source)
- inflation-adjusted from 2027, base year 2025 (we treat as flat real 2025 USD - simplification)
- credit lasts 12 YEARS from plant startup, NOT the full 30yr life (important!)
- OBBBA created storage/EOR parity (EOR now same value as permanent storage)

how we use it: gas/coal + CCS captures CO2 -> earns 85 USD/tonne -> offsets LCOE.
key question: does the 85 USD/ton credit make gas+CCS competitive vs plain gas?
CAVEAT: CCS LCOE excludes CO2 transport & storage (T&S) cost - must note/bound it.
"@ | Add-Content -Encoding utf8 assumptions.md

## T&S cost — for sensitivity anaylsis
CO2 transport + storage is very location-dependent.
- median ~$1.94/t, range $0.78–$14.59 (CMU)
- storage $1–3/t + transport $1–3/t = ~$2–6/t good sites (IEA GHG)
- >200 Gt US capacity at <$8/t, but Northeast ~$40/t (NETL 2024)

my sweep break-even ≈ $21/t. so:
- good geology ($2–15) → CCS keeps its 45Q edge
- bad geology (NE, $40+) → CCS loses
so gas+CCS viability under 45Q is location-dependent, not yes/no.
src: CMU CEIC paper; IEA GHG R&D; NETL Saline Storage Cost Model 2024


## T&S cost - for the sensitivity sweep

CO2 transport + storage is cheap but very location-dependent.
- median ~1.94/t, range 0.78-14.59 (CMU)
- storage 1-3/t + transport 1-3/t = ~2-6/t good sites (IEA GHG)
- 200+ Gt US capacity at under 8/t, but Northeast ~40/t (NETL 2024)

my sweep break-even ~21/t. so:
- good geology (2-15) -> CCS keeps its 45Q edge
- bad geology (NE, 40+) -> CCS loses
so gas+CCS viability under 45Q is location-dependent, not yes/no.
src: CMU CEIC paper; IEA GHG R&D; NETL Saline Storage Cost Model 2024
