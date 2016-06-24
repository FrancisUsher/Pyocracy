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
Environmentalist
    Environmentalist_income
    Environmentalist_freq
EthnicMinorities
Young
    Young_income
Wealthy
    _HighIncome
    Capitalist_income
Poor
    _LowIncome
    PovertyRate
MiddleIncome
    _MiddleIncome
Conservatives
Patriot
    Patriot_freq
StateEmployees
    StateEmployees_income
    StateEmployees_freq
Socialist
    _global_socialism
TradeUnionist
    TradeUnionist_freq
Motorist
    Motorist_income
    Motorist_freq
Capitalist
Retired
    Retired_income
    Retired_freq
Parents
    Parents_income
    Parents_freq
SelfEmployed
    SelfEmployed_income
    SelfEmployed_freq
Liberal
    _global_liberalism
Commuter
    Commuter_income
    Commuter_freq
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
