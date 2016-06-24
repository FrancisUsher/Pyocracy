# outputs:  voter groups, situations and simulation values/statistics
# some valid targets sampled from the default policies.csv file:
with open(r"D:\MyDev\Democracy 3\data\simulation\policies.csv") as fi:
    x = fi.readlines()
p = [row.split("#Effects")[1] for row in p]
all_effects = [row.split('"')[1::2] for row in p]
all_targets = [[e.split(',')[0] for e in row] for row in all_effects]
target_set = set(t for ts in all_targets for t in ts)

"""
Farmers
    Farmers_income
    Farmers_freq
StateEmployees
    StateEmployees_income
    StateEmployees_freq
TradeUnionist
    TradeUnionist_freq
Retired
    Retired_income
    Retired_freq
SelfEmployed
    SelfEmployed_income
    SelfEmployed_freq
Commuter
    Commuter_income
    Commuter_freq

Environmentalist
    Environmentalist_income
    Environmentalist_freq
EthnicMinorities

Wealthy
    _HighIncome
    Capitalist_income
MiddleIncome
    _MiddleIncome
Poor
    _LowIncome
    PovertyRate
    
Conservatives
Liberal
    _global_liberalism
    
Patriot
    Patriot_freq
Socialist
    _global_socialism
Motorist
    Motorist_income
    Motorist_freq
Capitalist
Young
    Young_income
Parents
    Parents_income
    Parents_freq

Religious
    Religious_income
    Religious_freq

_All_

Unemployment
GDP
Wages
WorkingWeek
WorkerProductivity
Education
PrivateSchools
Technology

TrafficCongestion
AirTravel
BusUsage
CarUsage
RailUsage
OilSupply
OilDemand
EnergyEfficiency
CO2Emissions
Environment


CrimeRate
ViolentCrimeRate

Health
LegalDrugConsumption
AlcoholConsumption
TobaccoUse
Obesity
PrivateHealthcare

_security_
_Terrorism
ForeignRelations
InternationalTrade
Immigration
Tourism

PrivateHousing
Equality
RacialTension

"""
