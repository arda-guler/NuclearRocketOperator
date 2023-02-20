# Nuclear Thermal Rocket simulator
import time
import tkinter as tk
from tkinter import ttk

from propellants import H2
from mach import *
from reactor import *
from reactor_control import *
from radiator import *
from sound import *

g = 9.80655

print("You have 500 kg of H2 propellant.\nTry to achieve the best delta-v possible.\nKeep the spacecraft and crew safe.")
input("\nPress Enter to start and see the control panel...")

print("\nSimulation started.")
dry_mass = 5e3 # kg
delta_v = 0

# propellant and propellant feed info
prop = H2()
prop_left = 500 # kg

mdot_nominal = 2 # kg s-1
mdot_max = 3 # kg s-1
mdot_change_rate = 0.1 # kg s-2
T_prop0 = 20 # K

mdot_prop1 = 2 # kg s-1
mdot_prop2 = 2 # kg s-1
mdot_prop3 = 2 # kg s-1

# thrust chamber info
expansion_ratio = 54 # exit area / throat area

# reactor
transfer_efficiency = 0.8 # efficiency

reactor1 = fission_reactor()
reactor1.control_rod_insertion = 0.5
reactor1.neutrons = 0.001

reactor2 = fission_reactor()
reactor2.control_rod_insertion = 0.5
reactor2.neutrons = 0.001

reactor3 = fission_reactor()
reactor3.control_rod_insertion = 0.5
reactor3.neutrons = 0.001

# crew radiation exposure
base_exposure = 5e-9 # sievert / sec.
propulsion_system_exposure = 3e-8 # sievert / sec

# radiator
rad1 = radiator(35E6)
rad2 = radiator(35E6)
rad3 = radiator(35E6)

dt = 1e-8
ctime = 0

# - - - UI - - -
init_sound()
play_sfx("lsback", -1, 3, 0.5)

mw = tk.Tk()
mw.title("AFT LEFT PANEL")
mw.geometry("800x600+50+50")
mw.resizable(False, False)
mw.iconbitmap("ndy.ico")

# alarm board
CWS_MPS1_Tc = tk.Label(text="MPS 1\nTEMP HI")
CWS_MPS1_Tc.config(bg="black", fg="white", width=10, height=2)
CWS_MPS1_Tc.place(x=50, y=10)

CWS_MPS2_Tc = tk.Label(text="MPS 2\nTEMP HI")
CWS_MPS2_Tc.config(bg="black", fg="white", width=10, height=2)
CWS_MPS2_Tc.place(x=150, y=10)

CWS_MPS3_Tc = tk.Label(text="MPS 3\nTEMP HI")
CWS_MPS3_Tc.config(bg="black", fg="white", width=10, height=2)
CWS_MPS3_Tc.place(x=250, y=10)

CWS_MPS1_F = tk.Label(text="MPS 1\nISP")
CWS_MPS1_F.config(bg="black", fg="white", width=10, height=2)
CWS_MPS1_F.place(x=50, y=50)

CWS_MPS2_F = tk.Label(text="MPS 2\nISP")
CWS_MPS2_F.config(bg="black", fg="white", width=10, height=2)
CWS_MPS2_F.place(x=150, y=50)

CWS_MPS3_F = tk.Label(text="MPS 3\nISP")
CWS_MPS3_F.config(bg="black", fg="white", width=10, height=2)
CWS_MPS3_F.place(x=250, y=50)

CWS_RAD1_T = tk.Label(text="TCS 1\nTEMP HI")
CWS_RAD1_T.config(bg="black", fg="white", width=10, height=2)
CWS_RAD1_T.place(x=50, y=90)

CWS_RAD2_T = tk.Label(text="TCS 2\nTEMP HI")
CWS_RAD2_T.config(bg="black", fg="white", width=10, height=2)
CWS_RAD2_T.place(x=150, y=90)

CWS_RAD3_T = tk.Label(text="TCS 3\nTEMP HI")
CWS_RAD3_T.config(bg="black", fg="white", width=10, height=2)
CWS_RAD3_T.place(x=250, y=90)

CWS_IRRAD = tk.Label(text="CREW HAB\nRADTN LVL")
CWS_IRRAD.config(bg="black", fg="white", width=10, height=2)
CWS_IRRAD.place(x=350, y=10)

CWS_PLCHD = tk.Label(text="")
CWS_PLCHD.config(bg="black", fg="white", width=10, height=2)
CWS_PLCHD.place(x=350, y=50)

CWS_PLCHD2 = tk.Label(text="")
CWS_PLCHD2.config(bg="black", fg="white", width=10, height=2)
CWS_PLCHD2.place(x=350, y=90)

# MPS1 INDICATORS
IND_MPS1_T_label = tk.Label(text="MPS 1 Tc")
IND_MPS1_T_label.config(width=10, height=1)
IND_MPS1_T_label.place(x=50, y=180)
IND_MPS1_T = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS1_T.config(width=10, height=1)
IND_MPS1_T.place(x=50, y=200)

IND_MPS1_F_label = tk.Label(text="MPS 1 Ft")
IND_MPS1_F_label.config(width=10, height=1)
IND_MPS1_F_label.place(x=50, y=230)
IND_MPS1_F = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS1_F.config(width=10, height=1)
IND_MPS1_F.place(x=50, y=250)

IND_MPS1_M_label = tk.Label(text="MPS 1 M'")
IND_MPS1_M_label.config(width=10, height=1)
IND_MPS1_M_label.place(x=50, y=280)
IND_MPS1_M = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS1_M.config(width=10, height=1)
IND_MPS1_M.place(x=50, y=300)

IND_TCS1_T_label = tk.Label(text="TCS 1 TEMP")
IND_TCS1_T_label.config(width=10, height=1)
IND_TCS1_T_label.place(x=50, y=330)
IND_TCS1_T = tk.Label(text="", borderwidth=2, relief="ridge")
IND_TCS1_T.config(width=10, height=1)
IND_TCS1_T.place(x=50, y=350)

# MPS2 INDICATORS
IND_MPS2_T_label = tk.Label(text="MPS 2 Tc")
IND_MPS2_T_label.config(width=10, height=1)
IND_MPS2_T_label.place(x=150, y=180)
IND_MPS2_T = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS2_T.config(width=10, height=1)
IND_MPS2_T.place(x=150, y=200)

IND_MPS2_F_label = tk.Label(text="MPS 2 Ft")
IND_MPS2_F_label.config(width=10, height=1)
IND_MPS2_F_label.place(x=150, y=230)
IND_MPS2_F = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS2_F.config(width=10, height=1)
IND_MPS2_F.place(x=150, y=250)

IND_MPS2_M_label = tk.Label(text="MPS 2 M'")
IND_MPS2_M_label.config(width=10, height=1)
IND_MPS2_M_label.place(x=150, y=280)
IND_MPS2_M = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS2_M.config(width=10, height=1)
IND_MPS2_M.place(x=150, y=300)

IND_TCS2_T_label = tk.Label(text="TCS 2 TEMP")
IND_TCS2_T_label.config(width=10, height=1)
IND_TCS2_T_label.place(x=150, y=330)
IND_TCS2_T = tk.Label(text="", borderwidth=2, relief="ridge")
IND_TCS2_T.config(width=10, height=1)
IND_TCS2_T.place(x=150, y=350)

# MPS3 INDICATORS
IND_MPS3_T_label = tk.Label(text="MPS 3 Tc")
IND_MPS3_T_label.config(width=10, height=1)
IND_MPS3_T_label.place(x=250, y=180)
IND_MPS3_T = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS3_T.config(width=10, height=1)
IND_MPS3_T.place(x=250, y=200)

IND_MPS3_F_label = tk.Label(text="MPS 3 Ft")
IND_MPS3_F_label.config(width=10, height=1)
IND_MPS3_F_label.place(x=250, y=230)
IND_MPS3_F = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS3_F.config(width=10, height=1)
IND_MPS3_F.place(x=250, y=250)

IND_MPS3_M_label = tk.Label(text="MPS 3 M'")
IND_MPS3_M_label.config(width=10, height=1)
IND_MPS3_M_label.place(x=250, y=280)
IND_MPS3_M = tk.Label(text="", borderwidth=2, relief="ridge")
IND_MPS3_M.config(width=10, height=1)
IND_MPS3_M.place(x=250, y=300)

IND_TCS3_T_label = tk.Label(text="TCS 3 TEMP")
IND_TCS3_T_label.config(width=10, height=1)
IND_TCS3_T_label.place(x=250, y=330)
IND_TCS3_T = tk.Label(text="", borderwidth=2, relief="ridge")
IND_TCS3_T.config(width=10, height=1)
IND_TCS3_T.place(x=250, y=350)

# REACTOR1
IND_MPS1_CTROD_label = tk.Label(text="MPS 1 CTROD")
IND_MPS1_CTROD_label.place(x=50, y=390)
IND_MPS1_CTROD = ttk.Progressbar(orient="vertical",length=150)
IND_MPS1_CTROD.place(x=75, y=420)

IND_MPS2_CTROD_label = tk.Label(text="MPS 2 CTROD")
IND_MPS2_CTROD_label.place(x=150, y=390)
IND_MPS2_CTROD = ttk.Progressbar(orient="vertical",length=150)
IND_MPS2_CTROD.place(x=175, y=420)

IND_MPS3_CTROD_label = tk.Label(text="MPS 3 CTROD")
IND_MPS3_CTROD_label.place(x=250, y=390)
IND_MPS3_CTROD = ttk.Progressbar(orient="vertical",length=150)
IND_MPS3_CTROD.place(x=275, y=420)

# AUTO/MANUAL CONTROL
control_mode = tk.StringVar(mw, "auto")
KNB_CTRL_label = tk.Label(text="CTRL MOD")
KNB_CTRL_label.place(x=350, y=200)
KNB_CTRL_AUTO = tk.Radiobutton(mw, text="AUTO", variable=control_mode, value="auto")
KNB_CTRL_AUTO.place(x=350, y=250)
KNB_CTRL_MAN = tk.Radiobutton(mw, text="MAN", variable=control_mode, value="manual")
KNB_CTRL_MAN.place(x=350, y=280)

MAN_CTRL_1_label = tk.Label(text="MPS 1 CTROD\nMAN SETTING")
MAN_CTRL_1_label.place(x=430, y=200)
MAN_CTRL_1 = tk.Scale(mw, from_=100, to=0, orient="vertical", tickinterval=20, length=300)
MAN_CTRL_1.place(x=430, y=250)

MAN_CTRL_2_label = tk.Label(text="MPS 2 CTROD\nMAN SETTING")
MAN_CTRL_2_label.place(x=530, y=200)
MAN_CTRL_2 = tk.Scale(mw, from_=100, to=0, orient="vertical", tickinterval=20, length=300)
MAN_CTRL_2.place(x=530, y=250)

MAN_CTRL_3_label = tk.Label(text="MPS 3 CTROD\nMAN SETTING")
MAN_CTRL_3_label.place(x=630, y=200)
MAN_CTRL_3 = tk.Scale(mw, from_=100, to=0, orient="vertical", tickinterval=20, length=300)
MAN_CTRL_3.place(x=630, y=250)

quench_mode = tk.StringVar(mw, "enabled")
KNB_QUENCH_label = tk.Label(text="H2 QUENCH\nTHRML STABL")
KNB_QUENCH_label.place(x=530, y=10)
KNB_QUENCH_ENABLE = tk.Radiobutton(mw, text="ENABLED", variable=quench_mode, value="enabled")
KNB_QUENCH_ENABLE.place(x=530, y=50)
KNB_QUENCH_DISABLE = tk.Radiobutton(mw, text="DISABLED", variable=quench_mode, value="disabled")
KNB_QUENCH_DISABLE.place(x=530, y=90)
KNB_QUENCH_OVRRD = tk.Radiobutton(mw, text="EMRGNCY\nACTIVATE", variable=quench_mode, value="override", fg="red")
KNB_QUENCH_OVRRD.place(x=530, y=130)

MPS1_T_timer = 0
MPS2_T_timer = 0
MPS3_T_timer = 0

TCS1_T_timer = 0
TCS2_T_timer = 0
TCS3_T_timer = 0

irrad_timer = 0

def sim_update():
    global ctime, dt, prop, mdot_nominal, mdot_prop1, mdot_prop2, mdot_prop3, mdot_max, mdot_change_rate,\
           T_prop0, expansion_ratio, reactor1, reactor2, reactor3, transfer_efficiency, rad1, rad2, rad3,\
           base_exposure, propulsion_system_exposure, prop_left, delta_v,\
           MPS1_T_timer, MPS2_T_timer, MPS3_T_timer,\
           TCS1_T_timer, TCS2_T_timer, TCS3_T_timer,\
           irrad_timer
    
    stime = time.perf_counter()
    ctime += dt

    # - - - START PHYSICS AND CONTROL SIMULATION - - -
    # reactor update
    reactor1.update(dt)
    reactor2.update(dt)
    reactor3.update(dt)
    reactor_output1 = reactor1.power_output() # W
    reactor_output2 = reactor2.power_output() # W
    reactor_output3 = reactor3.power_output() # W

    # reactor control
    if control_mode.get() == "auto":
        apply_reactor_commands(reactor1, dt)
        apply_reactor_commands(reactor2, dt)
        apply_reactor_commands(reactor3, dt)
        
    else:
        loc1 = MAN_CTRL_1.get()/100
        loc2 = MAN_CTRL_2.get()/100
        loc3 = MAN_CTRL_3.get()/100

        # MPS 1
        if loc1 != reactor1.control_rod_insertion:
            if (reactor1.control_rod_insertion - loc1) > 0:
                if abs(reactor1.control_rod_insertion - loc1) > reactor1.control_rod_movement_speed * dt:
                    reactor1.control_rod_insertion -= reactor1.control_rod_movement_speed * dt
                else:
                    reactor1.control_rod_insertion = loc1

            else:
                if abs(reactor1.control_rod_insertion - loc1) > reactor1.control_rod_movement_speed * dt:
                    reactor1.control_rod_insertion += reactor1.control_rod_movement_speed * dt
                else:
                    reactor1.control_rod_insertion = loc1

        # MPS 2
        if loc2 != reactor2.control_rod_insertion:
            if (reactor2.control_rod_insertion - loc2) > 0:
                if abs(reactor2.control_rod_insertion - loc2) > reactor2.control_rod_movement_speed * dt:
                    reactor2.control_rod_insertion -= reactor2.control_rod_movement_speed * dt
                else:
                    reactor2.control_rod_insertion = loc2

            else:
                if abs(reactor2.control_rod_insertion - loc2) > reactor2.control_rod_movement_speed * dt:
                    reactor2.control_rod_insertion += reactor2.control_rod_movement_speed * dt
                else:
                    reactor2.control_rod_insertion = loc2

        # MPS 3
        if loc3 != reactor3.control_rod_insertion:
            if (reactor3.control_rod_insertion - loc3) > 0:
                if abs(reactor3.control_rod_insertion - loc3) > reactor3.control_rod_movement_speed * dt:
                    reactor3.control_rod_insertion -= reactor3.control_rod_movement_speed * dt
                else:
                    reactor3.control_rod_insertion = loc3

            else:
                if abs(reactor3.control_rod_insertion - loc3) > reactor3.control_rod_movement_speed * dt:
                    reactor3.control_rod_insertion += reactor3.control_rod_movement_speed * dt
                else:
                    reactor3.control_rod_insertion = loc3

    Q_dot1 = reactor_output1 * transfer_efficiency # W
    q_dot1 = Q_dot1 / mdot_prop1 # J kg-1 s-1
    Q_dot2 = reactor_output2 * transfer_efficiency # W
    q_dot2 = Q_dot2 / mdot_prop2 # J kg-1 s-1
    Q_dot3 = reactor_output3 * transfer_efficiency # W
    q_dot3 = Q_dot3 / mdot_prop3 # J kg-1 s-1

    # update radiators
    Q_out1 = reactor_output1 * (1 - transfer_efficiency) # W
    rad1.update(Q_out1, dt)
    Q_out2 = reactor_output2 * (1 - transfer_efficiency) # W
    rad2.update(Q_out2, dt)
    Q_out3 = reactor_output3 * (1 - transfer_efficiency) # W
    rad3.update(Q_out3, dt)

    # crew radiation exposure
    total_exposure = base_exposure + propulsion_system_exposure * ((reactor_output1 + reactor_output2 + reactor_output3)/(reactor1.power_rate * 3))
    #total_exposure must be under 3.2e-8

    # update thrust chambers
    # TC 1
    h2_1 = prop.get_h(T_prop0) + q_dot1
    T_c1 = prop.get_T_by_h(h2_1)

    gamma1 = prop.get_gamma(T_c1)
    M_exit1 = calc_mach_num(expansion_ratio, gamma1)
    T_exit1 = (1 + (gamma1-1)/2 * M_exit1**2)**(-1) * T_c1

    if T_c1 > 1500:
        V_exit1 = M_exit1 * prop.get_speed_of_sound(T_exit1)
    else:
        V_exit1 = 500

    F_thrust1 = mdot_prop1 * V_exit1

    Isp1 = V_exit1/g

    # TC 2
    h2_2 = prop.get_h(T_prop0) + q_dot2
    T_c2 = prop.get_T_by_h(h2_2)

    gamma2 = prop.get_gamma(T_c2)
    M_exit2 = calc_mach_num(expansion_ratio, gamma2)
    T_exit2 = (1 + (gamma2-1)/2 * M_exit2**2)**(-1) * T_c2

    if T_c2 > 1500:
        V_exit2 = M_exit2 * prop.get_speed_of_sound(T_exit2)
    else:
        V_exit2 = 500

    F_thrust2 = mdot_prop2 * V_exit2

    Isp2 = V_exit2/g

    # TC 3
    h2_3 = prop.get_h(T_prop0) + q_dot3
    T_c3 = prop.get_T_by_h(h2_3)

    gamma3 = prop.get_gamma(T_c3)
    M_exit3 = calc_mach_num(expansion_ratio, gamma3)
    T_exit3 = (1 + (gamma3-1)/2 * M_exit3**2)**(-1) * T_c3

    if T_c3 > 1500:
        V_exit3 = M_exit3 * prop.get_speed_of_sound(T_exit3)
    else:
        V_exit3 = 500

    F_thrust3 = mdot_prop3 * V_exit3

    Isp3 = V_exit3/g

    # H2 quench thermal stabilization
    if quench_mode.get() == "enabled":
        # MPS1
        if T_c1 > 4200:
            mdot_prop1 += mdot_change_rate

        elif T_c1 < 4200 and mdot_prop1 > mdot_nominal:
            if mdot_prop1 - mdot_change_rate < mdot_nominal:
                mdot_prop1 -= mdot_prop1 - mdot_nominal
            else:
                mdot_prop1 -= mdot_change_rate

        if mdot_prop1 > mdot_max:
            mdot_prop1 = mdot_max

        # MPS 2
        if T_c2 > 4200:
            mdot_prop2 += mdot_change_rate

        elif T_c2 < 4200 and mdot_prop2 > mdot_nominal:
            if mdot_prop2 - mdot_change_rate < mdot_nominal:
                mdot_prop2 -= mdot_prop2 - mdot_nominal
            else:
                mdot_prop2 -= mdot_change_rate

        if mdot_prop2 > mdot_max:
            mdot_prop2 = mdot_max

        # MPS 3
        if T_c3 > 4200:
            mdot_prop3 += mdot_change_rate

        elif T_c3 < 4200 and mdot_prop3 > mdot_nominal:
            if mdot_prop3 - mdot_change_rate < mdot_nominal:
                mdot_prop3 -= mdot_prop3 - mdot_nominal
            else:
                mdot_prop3 -= mdot_change_rate

        if mdot_prop3 > mdot_max:
            mdot_prop3 = mdot_max

    elif quench_mode.get() == "disabled":
        if mdot_prop1 > mdot_nominal:
            mdot_prop1 -= min(mdot_change_rate, (mdot_prop1 - mdot_nominal))

        if mdot_prop2 > mdot_nominal:
            mdot_prop2 -= min(mdot_change_rate, (mdot_prop2 - mdot_nominal))

        if mdot_prop3 > mdot_nominal:
            mdot_prop3 -= min(mdot_change_rate, (mdot_prop3 - mdot_nominal))

    else:
        if mdot_prop1 < mdot_max:
            mdot_prop1 += min(mdot_change_rate, (mdot_max - mdot_prop1))

        if mdot_prop2 < mdot_max:
            mdot_prop2 += min(mdot_change_rate, (mdot_max - mdot_prop2))

        if mdot_prop3 < mdot_max:
            mdot_prop3 += min(mdot_change_rate, (mdot_max - mdot_prop3))

    # flight dynamics
    prop_left -= (mdot_prop1 + mdot_prop2 + mdot_prop3) * dt
    delta_v += (F_thrust1 + F_thrust2 + F_thrust3)/(dry_mass + prop_left) * dt

    # - - - END PHYSICS AND CONTROL SIMULATION - - -

    # - - - START ALARMS CHECK - - -

    # crew radiation exposure
    if total_exposure > 4e-8:
        CWS_IRRAD.config(bg="red")
        irrad_timer += dt
        if not get_channel_busy(2):
            play_sfx("alarm_crew", -1, 2, 1)
    elif total_exposure > 3.2e-8:
        if get_channel_busy(2):
            stop_channel(2)
        CWS_IRRAD.config(bg="orange")
    else:
        if get_channel_busy(2):
            stop_channel(2)
        CWS_IRRAD.config(bg="black")

    # radiator temperatures
    if rad1.T > rad1.T_max:
        CWS_RAD1_T.config(bg="red")
        TCS1_T_timer += dt
    else:
        CWS_RAD1_T.config(bg="black")

    if rad2.T > rad2.T_max:
        CWS_RAD2_T.config(bg="red")
        TCS2_T_timer += dt
    else:
        CWS_RAD2_T.config(bg="black")

    if rad3.T > rad3.T_max:
        CWS_RAD3_T.config(bg="red")
        TCS3_T_timer += dt
    else:
        CWS_RAD3_T.config(bg="black")

    # thrust chamber temperatures
    if T_c1 > 4500:
        CWS_MPS1_Tc.config(bg="red")
        MPS1_T_timer += dt
    elif 4500 > T_c1 > 4200:
        CWS_MPS1_Tc.config(bg="orange")
    else:
        CWS_MPS1_Tc.config(bg="black")

    if T_c2 > 4500:
        CWS_MPS2_Tc.config(bg="red")
        MPS2_T_timer += dt
    elif 4500 > T_c2 > 4200:
        CWS_MPS2_Tc.config(bg="orange")
    else:
        CWS_MPS2_Tc.config(bg="black")

    if T_c3 > 4500:
        CWS_MPS3_Tc.config(bg="red")
        MPS3_T_timer += dt
    elif 4500 > T_c3 > 4200:
        CWS_MPS3_Tc.config(bg="orange")
    else:
        CWS_MPS3_Tc.config(bg="black")

    # exhaust velocity
    if Isp1 < 800:
        CWS_MPS1_F.config(bg="orange")
    else:
        CWS_MPS1_F.config(bg="black")

    if Isp2 < 800:
        CWS_MPS2_F.config(bg="orange")
    else:
        CWS_MPS2_F.config(bg="black")

    if Isp3 < 800:
        CWS_MPS3_F.config(bg="orange")
    else:
        CWS_MPS3_F.config(bg="black")

    # - - - END ALARMS CHECK - - -

    # - - - START UPDATE UI - - -
    IND_MPS1_T.config(text=str(int(T_c1)))
    IND_MPS2_T.config(text=str(int(T_c2)))
    IND_MPS3_T.config(text=str(int(T_c3)))

    IND_MPS1_F.config(text=str(int(F_thrust1)))
    IND_MPS2_F.config(text=str(int(F_thrust2)))
    IND_MPS3_F.config(text=str(int(F_thrust3)))

    IND_MPS1_M.config(text=str(round(mdot_prop1, 2)))
    IND_MPS2_M.config(text=str(round(mdot_prop2, 2)))
    IND_MPS3_M.config(text=str(round(mdot_prop3, 2)))

    IND_TCS1_T.config(text=str(int(rad1.T)))
    IND_TCS2_T.config(text=str(int(rad2.T)))
    IND_TCS3_T.config(text=str(int(rad3.T)))

    IND_MPS1_CTROD['value'] = reactor1.control_rod_insertion * 100
    IND_MPS2_CTROD['value'] = reactor2.control_rod_insertion * 100
    IND_MPS3_CTROD['value'] = reactor3.control_rod_insertion * 100

    if ((rad1.T > rad1.T_max or rad2.T > rad2.T_max or rad3.T > rad3.T_max) or
        (T_c1 > 4500 or T_c2 > 4500 or T_c3 > 4500)):
        if not get_channel_busy(1):
            play_sfx("master_alarm", -1, 1, 1)
    else:
        if get_channel_busy(1):
            stop_channel(1)

    # - - - END UPDATE UI - - -
    
    dt = time.perf_counter() - stime + 0.001

    # - - - FAILURE CONDITIONS - - -
    if T_c1 > 5000 or T_c2 > 5000 or T_c3 > 5000 or MPS1_T_timer > 10 or MPS2_T_timer > 10 or MPS3_T_timer > 10:
        print("Catastrophic failure due to chamber burn-through.")
        time.sleep(2)
        input("Press Enter to quit...")
        quit()

    if rad1.T > 800 or rad2.T > 800 or rad3.T > 800 or TCS1_T_timer > 10 or TCS2_T_timer > 10 or TCS3_T_timer > 10:
        print("Catastrophic failure due to radiator failure and subsequent overheating.")
        time.sleep(2)
        input("Press Enter to quit...")
        quit()

    if total_exposure > 6e-8 or irrad_timer > 30:
        print("Auto-shutdown due to crew habitation radiation overexposure.")
        time.sleep(2)
        input("Press Enter to quit...")
        quit()

    if prop_left > 0:
        mw.after(1, sim_update)

    else:
        print("Maneuver performed. No failures. Total delta-v achieved: " + str(delta_v))
        time.sleep(2)
        input("Press Enter to quit...")
        quit()

sim_update()
mw.mainloop()
