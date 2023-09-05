import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Sequence, Dict, Tuple

# %%Variables
# DT = 30000 #KG per day Daily transportation
R = 8.3145  # kJ kg mol-1 K-1 //Gas constant [2]
T = 298.15  # K Temperature
M_H2 = 2.016  # g/mol Molar mass of hydrogen
roh_LH2 = 70.8  # g/L Density of liquid hydrogen
proj_hours = 175200  # hours Total project hours
proj_days = 7300  # days total project days
proj_years = 20  # Years total project years
sPerD = 86400  # S Seconds in a day
hPerD = 24  # hours per day
store_prec = 0.005  # Percent of daily transportation stored
Z = 1.1  # Compressibility of hydrogen [4]


PP_IN = 2  # pump inlet pressure bar
PP_OUT = 3  # pump outlet pressure bar
CP_IN = 3  # compressor inlet pressure
CP_OUT = 7  # compressor outlet pressure

# D = 300 #Distance
# %% Electricity Cost
Share_Onshorewind = 0.25
Share_Offshorewind = 0.25
Share_Solar = 0.5
Share_Fossil = 0

Cost_Onshorewind = 0.075  # $ per KWH  LOCE in 2021// https://www.irena.org/publications/2022/Jul/Renewable-Power-Generation-Costs-in-2021
Cost_Offshorewind = 0.033
Cost_Solar = 0.048
Cost_Fossil = 0.167  # High band

Emission_Onshorewind = 0 * Share_Onshorewind
Emission_Offshorewind = 0
Emission_Solar = 0
Emission_Fossil = 0.937  # KG co2 eq COAL//https://carbonintensity.org.uk/

U_elec = (
    Share_Onshorewind * Cost_Onshorewind
    + Share_Offshorewind * Cost_Offshorewind
    + Share_Solar * Cost_Solar
    + Share_Fossil * Cost_Fossil
)
Emission_Uelec = (
    Share_Onshorewind * Emission_Onshorewind
    + Share_Offshorewind * Emission_Offshorewind
    + Share_Solar * Emission_Solar
    + Share_Fossil * Emission_Fossil
)


# %%
def GH_compressor(DailyTrans, P_in, P_out):
    DT = DailyTrans

    Z = 1.1  # Compressibility of hydrogen [4]
    n = 2  # Number of compressor stages with max pressure ratio per stage = 2.1 [VARIABLE] [2]
    n_comp = 0.8  # Compressor efficiency [2]
    k = 1.4  # hydrogen heat capacity ratio
    P_in = P_in  # 300 #Bar Input pressure [VARIABLE]
    P_out = P_out  # 700#Bar Output pressure [VARIABLE]
    dep_rate_comp = 20  # Compressor depreciation rate years
    IF_ct = 1.3  # Terminal compressor installation factor
    IF_cp = 2  # Pipeline compressor installation factor
    Lab_c_cp = 31.6  # USD per hour [2] 2014

    Power_C_max = (
        (Z * DT * R * T * n)
        / (n_comp * sPerD * M_H2)
        * k
        / (k - 1)
        * ((P_out / P_in) ** ((k - 1) / (n * k)) - 1)
    )  # kW []
    Elec_demand = Power_C_max * proj_hours
    CAPEX_eq_tc = (
        40528 * Power_C_max
    ) ** 0.4603 * IF_ct  # CAPEX_Eq for a terminal compressor
    CAPEX_eq_cp = (
        1962.2 * Power_C_max
    ) ** 0.8335 * IF_cp  # CAPEX_Eq for a pipeline compressor

    Cost_Lab_cp = (
        288 * (DT / 100000) ** 0.25 * Lab_c_cp * proj_years
    )  # Labor cost for compressor per year *project years
    Cost_Elec_cp = Power_C_max * proj_hours * U_elec

    RES = {
        "CAPEX_cp": CAPEX_eq_cp,
        "CAPEX_tc": CAPEX_eq_tc,
        "elec_cost": Cost_Elec_cp,
        "lab_cost": Cost_Lab_cp,
        "elec_demand": Elec_demand,
    }
    return RES


# print(GH_compressor(DT,300,700).get('CAPEX_cp'))


def GH_storage_terminal(DT):
    Loss_storeGH = (
        0.005  # precent [VARIABLE] terminal gaseous hydrogen storage loss precentage
    )
    max_cap = DT * store_prec
    CAPEX_eq_TGHS = 1560 * max_cap  # CAPEX_Eq for terminal hydrogen storage in 2013[2]

    RES = {"CAPEX": CAPEX_eq_TGHS, "elec_cost": 0, "lab_cost": 0, "elec_demand": 0}

    return RES


# print(GH_storage_terminal())


def Liquefier(DT):
    CAPEX_Eq_li = (
        5600000 * (DT / 1000) ** 0.8
    )  # CAPEX_Eq for hydrogen liquefiers in 2014 [2]
    Elec_demand = 13.382 * (DT / 1000) ** (-0.1) * DT * proj_days  # Electricity cost
    Cost_Elec_Li = Elec_demand * U_elec
    Lab_c_li = 27.51  # $ per hour in 2014 [2]
    Cost_Lab_Li = (
        17520 * (DT / 100000) ** 0.25 * proj_years * Lab_c_li
    )  # $ Total liquefier labor cost []

    RES = {
        "CAPEX": CAPEX_Eq_li,
        "elec_cost": Cost_Elec_Li,
        "lab_cost": Cost_Lab_Li,
        "elec_demand": Elec_demand,
    }

    return RES


# print(Liquefier())


def LH_pump(DailyTrans, P_in, P_out):
    DT = DailyTrans
    P_in = P_in  # 2bar
    P_out = P_out  # 3bar
    IF_liqp = 1.3  # Liquid hydrogen pump install factor
    CAPEX_eq_LHP = 135000 * IF_liqp  # CAPEX_Eq for liquid hydrogen pumps in 2014 [2]

    n_pump = 0.75  # Pump efficiency
    P_motor = (DT * (P_out - P_in) * 14.696) / (12528 * roh_LH2)
    n_motor = (
        8 * 10 ** (-5) * P_motor**4
        - 1.5 * 10 ** (-3) * P_motor**3
        + 6.1 * 10 ** (-3) * P_motor**2
        + 3.1 * 10 ** (-2) * P_motor
        + 0.7617
    )  # LH pump motor efficiency
    Cost_Elec_LHP = (
        (P_out - P_in) / (522 * roh_LH2 * n_pump * n_motor) * DT * proj_years * U_elec
    )  # Total electricity cost over project years
    Demand_elec = Cost_Elec_LHP / U_elec

    Lab_c_lhp = 31.6  # $ per hour in 2014 [2]
    Cost_Lab_LHP = (
        288 * (DT / 100000) ** 0.25 * proj_years * Lab_c_lhp
    )  # Total labor cost for LHP over project years

    RES = {
        "CAPEX": CAPEX_eq_LHP,
        "elec_cost": Cost_Elec_LHP,
        "lab_cost": Cost_Lab_LHP,
        "elec_demand": Demand_elec,
    }

    return RES


# print(LH_pump(DT,700,750))


def LH_storage_terminal(DailyTrans):
    DT = DailyTrans
    Loss_storeLH = 0.005  # precent
    IF_lhs = 1.3  # Terminal liquid hydrogen storage install factor
    max_cap_liqs = DT
    CAPEX_eq_LHS = (
        0.1674 * max_cap_liqs**2 + 2064.6 * max_cap_liqs + 977886
    ) * IF_lhs

    RES = {"CAPEX": CAPEX_eq_LHS, "elec_cost": 0, "lab_cost": 0, "elec_demand": 0}

    return RES


# print(LH_storage_terminal(DT))


def GH_truck(Distance, DT):
    net_H2_gh = 750  # KG #KG Net H2 hauling capacity per container 750kg[6]
    RTD_GHT = Distance*2
    V_a_gh = 40  # KM/h

    Num_truck_gh = (
        DT * hPerD / (net_H2_gh * (RTD_GHT / V_a_gh + 1.5))
    )  # Total number of tube trailer

    Cost_cab_gh = 115000  # $ cost of cab in 2014 [2]  #20000 #ponds
    Cost_trailer_gh = 510000  # $ cost of trailer, including undercarriage in 2012 [2] #100000*0.79 #ponds $65,000-$216,000 ($80-$180 per kg H2 capacity)https://www.hydrogen.energy.gov/pdfs/progress05/v_d_1_aceves.pdf

    CAPEX_cab_gh = Cost_cab_gh * Num_truck_gh
    CAPEX_trailer_gh = Cost_trailer_gh * Num_truck_gh
    CAPEX_eq_GHT = CAPEX_cab_gh + CAPEX_trailer_gh

    Lab_c_ght = 28.75  # $ per hour in 2007 Driver hourly wage[7]
    Cost_Lab_GHT = Lab_c_ght * proj_hours  # $ Total driver cost during project time

    fuel_econ_avg = 2.6  # KM/L Average fuel economy
    U_fuel = 2  # $ Cost of fuel in 2010[7]
    OPEX_fre_GHT = DT * proj_days / net_H2_gh * RTD_GHT * fuel_econ_avg * U_fuel

    Emission_GH_Truck_OPEX = (
        0.0927 * RTD_GHT*Num_truck_gh* proj_days
    )  # 0.0927 kg co2 eq per tkm //IPCC GWP 2007 100a v1.02
    Emission_GH_Truck_cab = (
        Num_truck_gh * 6241.2
    )  # 22360.016 kg co2 eq per cab / s-order design https://www.diva-portal.org/smash/get/diva2:1507961/FULLTEXT01.pdf
    Emission_GH_Truck_trailer = 5.15  # *1500# 5.15kg co2 eq per kg agricultural trailer(1500kg tyer trailer) //IPCC GWP 2007 100a v1.02
    Emission_GH_Truck_tank = (
        net_H2_gh / 36000000 * 3.12e7
    )  ##3.12e7 kg co2 eq per tanker(36000tonnes) for liquedied natural gas
    Emission_GH_Truck_CAPEX = (
        Emission_GH_Truck_cab + Emission_GH_Truck_trailer + Emission_GH_Truck_tank
    )

    RES = {
        "CAPEX": CAPEX_eq_GHT,
        "lab_cost": Cost_Lab_GHT,
        "OPEX_fre": OPEX_fre_GHT,
        "elec_cost": 0,
        "elec_demand": 0,
        "OPEX_emi": Emission_GH_Truck_OPEX,
        "CAPEX_emi": Emission_GH_Truck_CAPEX,
    }

    return RES


# print(GH_truck(D))


def LH_truck(Distance, DT):
    net_H2_lh = 4000  # kg Net H2 hauling ccpacity per container [6]
    RTD_LHT = Distance*2  # KM Round trip distance
    V_a_lh = 40  # KM/H  average speed [2]
    time_load = 1.5  # hours time spent loading and unloading per trip [2]
    Num_truck_lh = (
        DT * hPerD / (net_H2_lh * (RTD_LHT / V_a_lh + time_load))
    )  # Total number of tube trailer

    Cost_cab_lh = 115000  # $ cost of cab in 2014 [2]
    Cost_trailer_lh = 950000  # $ cost of trailer, including undercarriage in 2012 [2]

    CAPEX_cab_lh = Cost_cab_lh * Num_truck_lh
    CAPEX_trailer_lh = Cost_trailer_lh * Num_truck_lh
    CAPEX_eq_LHT = CAPEX_cab_lh + CAPEX_trailer_lh

    Lab_c_lht = 28.75  # $ per hour in 2007 Driver hourly wage[7]
    Cost_Lab_LHT = Lab_c_lht * proj_hours  # $ Total driver cost during project time

    # net_H2 = M_G #KG Net H2 hauling capacity per container 750kg[6]
    # RTD = D*W_GH2d/net_H2 #KM Round tip distance
    fuel_econ_avg = 2.6  # KM/L Average fuel economy
    U_fuel = 2  # $ Cost of fuel in 2010[7]
    OPEX_fre_LHT = DT * proj_days / net_H2_lh * RTD_LHT * fuel_econ_avg * U_fuel

    Emission_LH_TRUCK_fre = (
        0.0927 * RTD_LHT*Num_truck_lh* proj_days
    )  # 0.0927 kg co2 eq per tkm //IPCC GWP 2007 100a v1.02
    Boil_rate_LH_TRUCK = 0.003  # per day
    Emission_LH_TRUCK_boil = (
        Boil_rate_LH_TRUCK * DT / 1000000000 * proj_days * 5.8
    )  # 100-year GWP for the tropospheric effects of H2 of 5.8//https://archive.ipcc.ch/publications_and_data/ar4/wg1/en/ch2s2-10-3-6.html  // MMTCDE = (million metric tonnes of a gas) * (GWP of the gas)//https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Carbon_dioxide_equivalent
    Emission_LH_Truck_OPEX = Emission_LH_TRUCK_fre + Emission_LH_TRUCK_boil

    Emission_LH_Truck_cab = (
        Num_truck_lh * 6241.2
    )  # 22360.016 kg co2 eq per cab / s-order design https://www.diva-portal.org/smash/get/diva2:1507961/FULLTEXT01.pdf
    Emission_LH_Truck_trailer = 5.15  # *1500# 5.15kg co2 eq per kg agricultural trailer(1500kg tyer trailer) //IPCC GWP 2007 100a v1.02
    Emission_LH_Truck_tank = (
        net_H2_lh / 23000000 * 3.18e7
    )  # 3.18e7 kg co2 eq per tanker(23000tonnes) for liquedied natural gas
    Emission_LH_Truck_CAPEX = (
        Emission_LH_Truck_cab + Emission_LH_Truck_trailer + Emission_LH_Truck_tank
    )

    RES = {
        "CAPEX": CAPEX_eq_LHT,
        "lab_cost": Cost_Lab_LHT,
        "OPEX_fre": OPEX_fre_LHT,
        "elec_cost": 0,
        "elec_demand": 0,
        "OPEX_emi": Emission_LH_Truck_OPEX,
        "CAPEX_emi": Emission_LH_Truck_CAPEX,
    }

    return RES


# print(LH_truck(D))


def GH_pipeline(Distance, DT):
    P_b = 100  # kpa atmospheric pressure [8]
    T_f = 293.75  # K average gas flow temperature [8]
    T_b = 288.75  # K atmospheric temperature [8]
    P_in_pip = 70  # bar input pressure [2,7]
    P_out_pip = 35  # bar output pressure [2,7]
    mu = 8.75 * 10 ** (-5)  # poise Hydrogen gas viscosity [9]
    L = Distance  # KM required pipeline length
    Dia_inches = 41  # 3.880*(DT/(roh_LH2*1000)*P_b*T_f*L*Z*mu*T_b**7*(P_in_pip**2-P_out_pip**2)**7)**0.25/(T_b**2*(P_in_pip**2-P_out_pip**2)**7) #Inches required pipeline diameter
    L_miles = L * 0.621371192  # Miles required pipeline length
    CAPEX_mat = 1.1 * 63027 * math.exp(Dia_inches * 0.0697) * L_miles
    CAPEX_lab = 1.1 * (
        L_miles * (((-51.393) * Dia_inches**2 + 43523 * Dia_inches + 16171))
    )
    CAPEX_misc = 1.1 * (
        L_miles * (((303.13) * Dia_inches**2 + 12908 * Dia_inches + 123245))
    )
    CAPEX_row = L_miles * (
        ((-9 * 10 ** (-13)) * Dia_inches**2 + 4417.1 * Dia_inches + 164241)
    )
    CAPEX_eq_PIP = CAPEX_mat + CAPEX_lab + CAPEX_row

    Lab_c_pip = 28.75  # $ per hour in 2007 Driver hourly wage[7]
    Cost_Lab_GHP = Lab_c_pip * proj_hours  # $ Total driver cost during project time

    loss_pip_rate = 483.43  # kg/km/year  //Pipeline loss rate
    loss_pip = loss_pip_rate * L * proj_years  # kg pipeline loss during project time
    Emission_LH_PIP_boil = loss_pip * 5.8 / 1000000000
    Emission_LH_PIP_CAPEX = 772 *L # 8.57e4 *L ##8.57e4 kg co2 eq per km //IPCC GWP 2007 100a v1.02//Pipeline,natural gas, high pressure//Construction
    Emission_LH_PIP_OPEX = (
        0.0944 * L * DT * proj_days / 1000 + Emission_LH_PIP_boil
    )  # 0.0944kg co2 eq per tkm //IPCC GWP 2007 100a v1.02

    RES = {
        "CAPEX": CAPEX_eq_PIP,
        "lab_cost": Cost_Lab_GHP,
        "elec_cost": 0,
        "elec_demand": 0,
        "OPEX_emi": Emission_LH_PIP_OPEX,
        "CAPEX_emi": Emission_LH_PIP_CAPEX,
    }

    return RES


# print(GH_pipeline(D))


def GH_rail(Distance):
    Cost_railcontailer_gh = 410000  # $ Cost of one container gor gh in 2012 [2]
    cap_railcontainer_gh = 750  # kg net H2 hauling capacity per container [2]

    IF_ghr = 1.3  # Effective GH2 resale markdown[2]

    D = Distance  # KM
    U_fre_ghrail = 2.75  # $ per mile
    OPEX_fre_ghrail = D / 0.621371192 * U_fre_ghrail  # Cost of rail shipping

    RES = {"OPEX_fre": OPEX_fre_ghrail}

    return RES


# print(GH_rail(D))


def LH_rail(Distance):
    Cost_railcontailer_lh = 850000  # $ Cost of one container gor lh in 2014 [5]
    cap_railcontainer_lh = 4000  # kg net H2 hauling capacity per container [6]

    IF_lhr = 1.3  # Effective LH2 resale markdown[2]

    D = Distance  # KM
    U_fre_lhrail = 2.75  # $ per mile [3]
    OPEX_fre_lhrail = D / 0.621371192 * U_fre_lhrail  # Cost of rail shipping

    boil_rail_rate = 3e-3  # per day LH2 boil off rate [2]
    loss_raillh_rate = 5e-3  # of throughput  LH2 rail loss precent [2]

    RES = {"OPEX_fre": OPEX_fre_lhrail}

    return RES


# print(LH_rail(D))


def GH_ship(Distance):
    Cost_shipcontailer_gh = 410000  # $ Cost of one container gor lh in 2014 [5]
    cap_contailer_ghship = 750  # kg net H2 hauling capacity per container [6]

    IF_ghs = 1.3  # Effective LH2 resale markdown[2]

    D = Distance  # KM
    U_fre_ghship = 0.8  # $ per mile in 2017 [3]
    OPEX_fre_ghship = D / 0.621371192 * U_fre_ghship  # Cost of rail shipping

    RES = {"OPEX_fre": OPEX_fre_ghship}

    return RES


# print(GH_ship(D))


def LH_ship(Distance):
    Cost_shipcontailer_gh = 850000  # $ Cost of one container gor lh in 2014 [5]
    cap_contailer_ghship = 4000  # kg net H2 hauling capacity per container [6]

    IF_lhs = 1.3  # Effective LH2 resale markdown[2]

    D = Distance  # KM
    U_fre_lhship = 0.8  # $ per mile in 2017 [3]
    OPEX_fre_lhship = D / 0.621371192 * U_fre_lhship  # Cost of rail shipping
    boil_ship_rate = 3e-3  # per day LH2 boil off rate [2]
    loss_shiplh_rate = 5e-3  # of throughput  LH2 rail loss precent [2]

    RES = {"OPEX_fre": OPEX_fre_lhship}

    return RES


# print(LH_ship(D))


def terminals(DT):
    Lab_c_terminal = 27.51  # $ per hour in 2014 [2]
    Cost_Lab_T = 17520 * (DT / 100000) ** 0.25 * proj_years

    RES = {"lab_cost": Cost_Lab_T}

    return RES


# print(terminals())

# print(GH_compressor(DT,300,700).get('lab_cost'))
# %%Graphs


def calc_costs(D: float, DT: float) -> Dict[str, float]:
    Cost_H2_Alkaline = 44.65 * U_elec * DT * proj_days
    f = DT * proj_days

    COST_LH_TRUCK_CAPEX = (
        LH_truck(D, DT).get("CAPEX")
        + Liquefier(DT).get("CAPEX")
        + LH_pump(DT, PP_IN, PP_OUT).get("CAPEX")
        + LH_storage_terminal(DT).get("CAPEX")
    )
    COST_LH_TRUCK_LAB = (
        LH_truck(D, DT).get("lab_cost")
        + Liquefier(DT).get("lab_cost")
        + LH_pump(DT, PP_IN, PP_OUT).get("lab_cost")
    )
    COST_LH_TRUCK_FRE = LH_truck(D, DT).get("OPEX_fre")
    COST_LH_TRUCK_OPEX = COST_LH_TRUCK_LAB + COST_LH_TRUCK_FRE
    COST_LH_TRUCK_ELEC = (
        Cost_H2_Alkaline
        + Liquefier(DT).get("elec_cost")
        + LH_pump(DT, PP_IN, PP_OUT).get("elec_cost")
    )
    SUM_LH_TRUCK = COST_LH_TRUCK_CAPEX + COST_LH_TRUCK_OPEX + COST_LH_TRUCK_ELEC

    Emission_LH_TRUCK_CAPEX = LH_truck(D, DT).get("CAPEX_emi")
    Emission_LH_TRUCK_OPEX = LH_truck(D, DT).get("OPEX_emi")
    Emission_LH_TRUCK = Emission_LH_TRUCK_CAPEX + Emission_LH_TRUCK_OPEX

    COST_GH_TRUCK_CAPEX = (
        GH_truck(D, DT).get("CAPEX")
        + GH_compressor(DT, PP_IN, PP_OUT).get("CAPEX_tc")
        + GH_storage_terminal(DT).get("CAPEX")
        + Liquefier(DT).get("CAPEX")
        + LH_storage_terminal(DT).get("CAPEX")
    )
    COST_GH_TRUCK_LAB = (
        GH_truck(D, DT).get("lab_cost")
        + GH_compressor(DT, CP_IN, CP_OUT).get("lab_cost")
        + Liquefier(DT).get("lab_cost")
    )
    COST_GH_TRUCK_FRE = GH_truck(D, DT).get("OPEX_fre")
    COST_GH_TRUCK_OPEX = COST_GH_TRUCK_LAB + COST_GH_TRUCK_FRE
    COST_GH_TRUCK_ELEC = (
        Cost_H2_Alkaline
        + GH_compressor(DT, CP_IN, CP_OUT).get("elec_cost")
        + Liquefier(DT).get("elec_cost")
    )
    SUM_GH_TRUCK = COST_GH_TRUCK_CAPEX + COST_GH_TRUCK_OPEX + COST_GH_TRUCK_ELEC

    Emission_GH_TRUCK_CAPEX = GH_truck(D, DT).get("CAPEX_emi")
    Emission_GH_TRUCK_OPEX = GH_truck(D, DT).get("OPEX_emi")
    Emission_GH_TRUCK = Emission_GH_TRUCK_CAPEX + Emission_GH_TRUCK_OPEX

    COST_GH_PIPE_CAPEX = (
        GH_pipeline(D, DT).get("CAPEX")
        + GH_compressor(DT, CP_IN, CP_OUT).get("CAPEX_cp")
        + GH_storage_terminal(DT).get("CAPEX")
        + Liquefier(DT).get("CAPEX")
        + LH_storage_terminal(DT).get("CAPEX")
    )
    COST_GH_PIPE_LAB = (
        GH_pipeline(D, DT).get("lab_cost")
        + GH_compressor(DT, CP_IN, CP_OUT).get("lab_cost")
        + Liquefier(DT).get("lab_cost")
        + LH_pump(DT, CP_IN, CP_OUT).get("lab_cost")
    )
    COST_GH_PIPE_FRE = 0
    COST_GH_PIPE_OPEX = COST_GH_PIPE_LAB + COST_GH_PIPE_FRE
    COST_GH_PIPE_ELEC = (
        Cost_H2_Alkaline
        + GH_compressor(DT, CP_IN, CP_OUT).get("elec_cost")
        + Liquefier(DT).get("elec_cost")
    )
    SUM_GH_PIPE = COST_GH_PIPE_CAPEX + COST_GH_PIPE_OPEX + COST_GH_PIPE_ELEC

    Emission_GH_PIPE_CAPEX = GH_pipeline(D, DT).get("CAPEX_emi")
    Emission_GH_PIPE_OPEX = GH_pipeline(D, DT).get("OPEX_emi")
    Emission_GH_PIPE = Emission_GH_PIPE_CAPEX + Emission_GH_PIPE_OPEX

    return dict(
        COST_LH_TRUCK_CAPEX=COST_LH_TRUCK_CAPEX,
        COST_LH_TRUCK_LAB=COST_LH_TRUCK_LAB,
        COST_LH_TRUCK_FRE=COST_LH_TRUCK_FRE,
        COST_LH_TRUCK_OPEX=COST_LH_TRUCK_OPEX,
        COST_LH_TRUCK_ELEC=COST_LH_TRUCK_ELEC,
        SUM_LH_TRUCK=SUM_LH_TRUCK,
        UNIT_LH_TRUCK=SUM_LH_TRUCK / f,
        Emission_LH_TRUCK_CAPEX=Emission_LH_TRUCK_CAPEX,
        Emission_LH_TRUCK_OPEX=Emission_LH_TRUCK_OPEX,
        Emission_LH_TRUCK=Emission_LH_TRUCK,
        UNIT_Emission_LH_TRUCK=Emission_LH_TRUCK / f,
        ###
        COST_GH_TRUCK_CAPEX=COST_GH_TRUCK_CAPEX,
        COST_GH_TRUCK_LAB=COST_GH_TRUCK_LAB,
        COST_GH_TRUCK_FRE=COST_GH_TRUCK_FRE,
        COST_GH_TRUCK_OPEX=COST_GH_TRUCK_OPEX,
        COST_GH_TRUCK_ELEC=COST_GH_TRUCK_ELEC,
        SUM_GH_TRUCK=SUM_GH_TRUCK,
        UNIT_GH_TRUCK=SUM_GH_TRUCK / f,
        Emission_GH_TRUCK_CAPEX=Emission_GH_TRUCK_CAPEX,
        Emission_GH_TRUCK_OPEX=Emission_GH_TRUCK_OPEX,
        Emission_GH_TRUCK=Emission_GH_TRUCK,
        UNIT_Emission_GH_TRUCK=Emission_GH_TRUCK / f,
        ###
        COST_GH_PIPE_CAPEX=COST_GH_PIPE_CAPEX,
        COST_GH_PIPE_LAB=COST_GH_PIPE_LAB,
        COST_GH_PIPE_FRE=COST_GH_PIPE_FRE,
        COST_GH_PIPE_OPEX=COST_GH_PIPE_OPEX,
        COST_GH_PIPE_ELEC=COST_GH_PIPE_ELEC,
        SUM_GH_PIPE=SUM_GH_PIPE,
        UNIT_GH_PIPE=SUM_GH_PIPE / f,
        Emission_GH_PIPE_CAPEX=Emission_GH_PIPE_CAPEX,
        Emission_GH_PIPE_OPEX=Emission_GH_PIPE_OPEX,
        Emission_GH_PIPE=Emission_GH_PIPE,
        UNIT_Emission_GH_PIPE=Emission_GH_PIPE / f,
        UNIT_Cost_H2_Alkaline = Cost_H2_Alkaline /f,
        
        f=f,
    )


def get_min_cost(
    costs: Dict[str, float],
    names: Sequence[str],
) -> Tuple[str, float]:
    min_name = ""
    min_value = float("inf")

    for name in names:
        if costs[name] < min_value:
            min_value = costs[name]
            min_name = name

    return (min_name, min_value)
