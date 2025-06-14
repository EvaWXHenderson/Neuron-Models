import matplotlib.pyplot as plt
import math

def variable_inf_calc(variable):
    global V_values

    if variable == "m":
        A_m = (0.1*(V_values[0] + 40))/(1-math.exp(-0.1*(V_values[0] + 40)))
        B_m = 4*math.exp(-0.0556*(V_values[0]+65))
        m_inf = A_m/(A_m + B_m)
        tau_m = 1/(A_m + B_m)
        return m_inf, tau_m

    if variable == "h":
        A_h = 0.07*math.exp(-0.05*(V_values[0] + 65))
        B_h = 1/(1+math.exp(-0.1*(V_values[0] + 35)))
        h_inf = A_h/(A_h + B_h)
        tau_h = 1/(A_h + B_h)
        return h_inf, tau_h
    
    if variable == "n":
        A_n = (0.01*(V_values[0] + 55))/(1-math.exp(-0.1*(V_values[0] + 55)))
        B_n = 0.125*math.exp(-0.0125*(V_values[0]+65))
        n_inf = A_n/(A_n + B_n)
        tau_n = 1/(A_n + B_n)
        return n_inf, tau_n 
    
    if variable == "V":
        for index in range(len(n_values)):
            V_inf = ((G_MAX_L*E_L) + (G_MAX_K*(n_values[index]**4)*E_K)+(G_MAX_NA*(m_values[index]**3)*h_values[index]*E_NA))/(G_MAX_L + (G_MAX_K*(n_values[index]**4)) + (G_MAX_NA*(m_values[index]**3)*h_values[index]))
        for index in range(len(n_values)):
            tau_V = C/(G_MAX_L + (G_MAX_K*(n_values[index]**4)) + (G_MAX_NA*(m_values[index]**3)*h_values[index]))
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



V_values = [-65] #intital value

m_inf, tau_m = variable_inf_calc("m")
m_values = [m_inf] #intital value for V = -65
g_m_values = [m_inf*100] #modified values for graphing (g)


h_inf, tau_h = variable_inf_calc("h")
h_values = [h_inf] #intital value for V = -65
g_h_values = [h_inf*100]


n_inf, tau_n = variable_inf_calc("n")
n_values = [n_inf] #intital value for V = -65
g_n_values = [n_inf*100]

V_inf, tau_V = variable_inf_calc("V")


while current_time <= T_END:
    current_time = current_time + DT
    time.append(current_time)
    

    m = variable_calc("m")
    g_m_values.append(m*100)
    m_values.append(m)

    h = variable_calc("h")
    g_h_values.append(h*100)
    h_values.append(h)

    n = variable_calc("n")
    g_n_values.append(n*100)
    n_values.append(n)

    V = variable_calc("V")
    V_values.append(V)


"""if time <= T_STIM_START or time >= T_STIM_END:
        I = 0"""

"""print(str(V_values[100]) + "\n" + str(m_values[100]) + "\n" + str(n_values[100]) + "\n" + str(h_values[100]) + "\n" + str(time[100]))
print(g_m_values)
print(V_inf, tau_V)
print(m_inf, tau_m)
print(h_inf, tau_h)
print(n_inf, tau_n)"""

plt.plot(time, V_values, color = "blue")
plt.plot(time, g_m_values, color = "black")
plt.plot(time, g_h_values, color = "red")
plt.plot(time, g_n_values, color = "green")
plt.xlabel("Voltage (nA)")
plt.ylabel("Time (ms)")
plt.legend(["Voltage", "m*100" , "h*100", "n*100"], loc = "lower right")
plt.xlim(0, T_END)
plt.ylim(V_values[0] - 15, 100)
plt.show()