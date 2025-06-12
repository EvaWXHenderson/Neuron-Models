import matplotlib as plt
import math

def variable_calc(variable):
    global Voltage_values

    if variable == "n":
        A_n = (0.01*(Voltage_values[0] + 55))/(1-math.exp(-0.1*(Voltage_values[0] + 55)))
        B_n = 0.125*math.exp(-0.0125*(Voltage_values[0]+65))
        n_inf = A_n/(A_n + B_n)
        tau_n = 1/(A_n + B_n)
        return n_inf, tau_n 

    if variable == "m":
        A_m = (0.1*(Voltage_values[0] + 40))/(1-math.exp(-0.1*(Voltage_values[0] + 40)))
        B_m = 4*math.exp(-0.0556*(Voltage_values[0]+65))
        m_inf = A_m/(A_m + B_m)
        tau_m = 1/(A_m + B_m)
        return m_inf, tau_m

    if variable == "h":
        A_h = 0.07*math.exp(-0.05*(Voltage_values[0] + 65))
        B_h = 1/(1+math.exp(-0.1*(Voltage_values[0] + 35)))
        h_inf = A_h/(A_h + B_h)
        tau_h = 1/(A_h + B_h)
        return h_inf, tau_h
def tau_V_calc():
    for index in range(len(n_values)):
        tau_V = c/(G_MAX_L + (G_MAX_K*n_values[index]**4) + (G_MAX_NA*m_values[index]**3*h_values[index]))
        return tau_V
def V_inf_calc():
    for index in range(len(n_values)):
        V_inf = ((G_MAX_L*E_L) + (G_MAX_K*n_values[index]**4*E_K)+(G_MAX_NA*m_values[index]**3*h_values[index]*E_NA))/(G_MAX_L + (G_MAX_K*n_values[index]**4) + (G_MAX_NA*m_values[index]**3*h_values[index]))
        return V_inf

DT = 0.1 #change in time in (ms)
T_END = 70 #duration (ms)
T_STIM_START = 10 #time start of current injection (ms)
T_STIM_END = 60 #time end of current injection (ms)

C = 10 #capacitance per unit area(nF/mm^2)

I_0 = 200 # magnitude of injected current (nA/mm^2)

"""max conductance per unit area (uS/mm^2)"""
G_MAX_L = 0.003*10**3 #leak
G_MAX_K = 0.39*10**3 #potassium (K+) 
G_MAX_NA = 1.2*10**3 #sodium (Na+)

"""conductance reversal potential (mV)"""
E_L = -54.387 #leak 
E_K = -77 #potassium
E_NA = 50 #sodium

"""counters"""
current_time = 0
time = [0]
I_t_values = []



Voltage_values = [-65] #intital value

m_inf,tau_m = variable_calc("m")
m_values = [m_inf] #intital value for V = -65


h_inf, tau_h = variable_calc("h")
h_values = [h_inf] #intital value for V = -65


n_inf, tau_n = variable_calc("n")
n_values = [n_inf] #intital value for V = -65




"""while current_time <= T_END:
    current_time = current_time + DT
    time.append(current_time)
    
    if time <= T_STIM_START or time >= T_STIM_END:
        I = 0"""
