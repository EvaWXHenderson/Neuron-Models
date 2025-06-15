import matplotlib.pyplot as plt
import math

def alpha_beta_assign(variable):
    if variable == "m":
        A_m = (0.1*(V_values[-1] + 40))/(1-math.exp(-0.1*(V_values[-1] + 40)))
        B_m = 4*math.exp(-0.0556*(V_values[-1]+65))
        return A_m, B_m
    
    if variable == "h":
        A_h = 0.07*math.exp(-0.05*(V_values[-1] + 65))
        B_h = 1/(1+math.exp(-0.1*(V_values[-1] + 35)))
        return A_h, B_h
    
    if variable == "n":
        A_n = (0.01*(V_values[-1] + 55))/(1-math.exp(-0.1*(V_values[-1] + 55)))
        B_n = 0.125*math.exp(-0.0125*(V_values[-1]+65))
        return A_n, B_n

def variable_inf_calc(variable):
    global V_values, A_m, B_m, A_h, B_h

    if variable == "m":
        A_m, B_m = alpha_beta_assign("m")
        m_inf = A_m/(A_m + B_m)
        tau_m = 1/(A_m + B_m)
        return m_inf, tau_m

    if variable == "h":
        A_h, B_h = alpha_beta_assign("h")
        h_inf = A_h/(A_h + B_h)
        tau_h = 1/(A_h + B_h)
        return h_inf, tau_h
    
    if variable == "n":
        A_n, B_n = alpha_beta_assign("n")
        n_inf = A_n/(A_n + B_n)
        tau_n = 1/(A_n + B_n)
        return n_inf, tau_n 
    
    if variable == "V":
        V_inf = ((G_MAX_L*E_L) + (G_MAX_K*(n_values[-1]**4)*E_K)+(G_MAX_NA*(m_values[-1]**3)*h_values[-1]*E_NA + I_t_values[-1]))/(G_MAX_L + (G_MAX_K*(n_values[-1]**4)) + (G_MAX_NA*(m_values[-1]**3)*h_values[-1]))
        tau_V = C/(G_MAX_L + (G_MAX_K*(n_values[-1]**4)) + (G_MAX_NA*(m_values[-1]**3)*h_values[-1]))
        return V_inf, tau_V

def variable_calc(variable):
    global m_inf, m_values, tau_m, h_inf, h_values, tau_h, n_inf, n_values, tau_n, DT

    if variable == "m":
        m = m_inf + (m_values[-1] - m_inf)*math.exp(-DT/tau_m)
        return m
    
    if variable == "h":
        h = h_inf + (h_values[-1] - h_inf)*math.exp(-DT/tau_h)
        return h
    
    if variable == "n":
        n = n_inf + (n_values[-1] - n_inf)*math.exp(-DT/tau_n)
        return n
    
    if variable == "V":
        V = V_inf + (V_values[-1] - V_inf)*math.exp(-DT/tau_V)
        return V

def average_spiking_rate():
    global spikes 

    AveSRate = 1000*spikes*(T_STIM_END - T_STIM_START)
    return AveSRate

def graph_type(type, scaled, variable = False):
    if type == "single":
        if scaled == "no":
            if variable == "m":
                plt.plot(time, m_values)
            elif variable == "h":
                plt.plot(time, h_values)
            elif variable == "n":
                plt.plot(time, n_values)
            elif variable == "V":
                plt.plot(time, V_values)

        if scaled == "yes":
            if variable == "m":
                plt.plot(time, g1_m_values)
            elif variable == "h":
                plt.plot(time, g_h_values)
            elif variable == "h":
                plt.plot(time, g1_n_values)
            elif variable == "V":
                plt.plot(time, V_values)
    
    if type == "comparison":
        if scaled == "no":
            plt.plot(time, V_values, color = "blue")
            plt.plot(time, g1_m_values, color = "black")
            plt.plot(time, g_h_values, color = "red")
            plt.plot(time, g1_n_values, color = "green")
            plt.xlabel("Voltage (nA)")
            plt.ylabel("Time (ms)")
            plt.legend(["Voltage", "m*100" , "h*100", "n*100"], loc = "lower right")
            plt.xlim(0, T_END)
            plt.ylim(V_values[0] - 15, 100)
        elif scaled == "yes":
            plt.plot(time, V_values, color = "blue")
            plt.plot(time, g2_m_values, color = "black")
            plt.plot(time, g_h_values, color = "red")
            plt.plot(time, g2_n_values, color = "green")
            plt.plot(time,g2_m3_h_values, color = "magenta")
            plt.xlabel("Voltage (nA)")
            plt.ylabel("Time (ms)")
            plt.legend(["Voltage", "m^3*100" , "h*100", "n^4*100", "m^3*h*100"], loc = "lower right")
            plt.xlim(0, T_END)
            plt.ylim(V_values[0] - 15, 100)


"""time duration:"""
DT = 0.1 #change in time in (ms)
T_END = 700 #duration (ms)
T_STIM_START = 100 #time start of current injection (ms)
T_STIM_END = 600 #time end of current injection (ms)
T_COUNT_START = T_STIM_START + 200 #(ms)

C = 10 #capacitance per unit area(nF/mm^2)

I_0 = 200 # magnitude of injected current (nA/mm^2)

V_th = -50 #threshold potential (mV)
"""seems not ideal to set -10mV as a threshold value as is unrealistic, look over other variables to make sure they're realistic values"""

"""max conductance per unit area (uS/mm^2):"""
G_MAX_L = 0.003*10**3 #leak
G_MAX_K = 0.39*10**3 #potassium (K+) 
G_MAX_NA = 1.2*10**3 #sodium (Na+)

"""conductance reversal potential (mV):"""
E_L = -54.387 #leak 
E_K = -77 #potassium
E_NA = 50 #sodium

"""counters:"""
current_time = 0
time = [0]
I_t_values = [0]

spikes = 0

"""initial value setting:"""
V_values = [-70] #intital value

m_inf, tau_m = variable_inf_calc("m")
m_values = [m_inf] #intital value for V = -65
g1_m_values = [m_inf*100] #modified values for graphing (g)
g2_m_values = [(m_inf**3)*100]

h_inf, tau_h = variable_inf_calc("h")
h_values = [h_inf] #intital value for V = -65
g_h_values = [h_inf*100]

n_inf, tau_n = variable_inf_calc("n")
n_values = [n_inf] #intital value for V = -65
g1_n_values = [n_inf*100]
g2_n_values = [(n_inf**4)*100]

g2_m3_h_values = [(m_inf**3)*h_inf*100]

V_inf, tau_V = variable_inf_calc("V")


while current_time <= T_END:
    current_time = current_time + DT
    time.append(current_time)

    if current_time < T_STIM_START or current_time >= T_STIM_END:
        I = 0
        I_t_values.append(I)
    if current_time >= T_STIM_START and current_time < T_STIM_END:
        I = I_0
        I_t_values.append(I)


    A_m, B_m = alpha_beta_assign("m")
    A_h, B_h = alpha_beta_assign("h")
    A_n, B_n = alpha_beta_assign("n")
    

    V_inf, tau_V = variable_inf_calc("V")
    V = variable_calc("V")
    V_values.append(V)

    #m = variable_calc("m")
    m_inf, tau_m = variable_inf_calc("m")
    m = variable_calc("m")
    g1_m_values.append(m*100)
    g2_m_values.append((m**3)*100)
    m_values.append(m)

    #h = variable_calc("h")
    h_inf, tau_h = variable_inf_calc("h")
    h = variable_calc("h")
    g_h_values.append(h*100)
    h_values.append(h)

    #n = variable_calc("n")
    n_inf, tau_n = variable_inf_calc("n")
    n = variable_calc("n")
    g1_n_values.append(n*100)
    g2_n_values.append((n**4)*100)
    n_values.append(n)

    g2_m3_h_values.append((m**3)*h*100)


for index in range(len(time)-1):
    if time[index] > T_COUNT_START and time[index] <= T_STIM_END:
        if V_values[-1] < V_th and V_values[index + 1] > -50:
            spikes = spikes + 1

graph_type("comparison", "yes")

print("Number of spikes with applied current of " + str(I_0) + " nA/mm^2: " + str(spikes))

plt.show()