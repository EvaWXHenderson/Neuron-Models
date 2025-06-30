import math
import matplotlib.pyplot as plt

"""values: """
dt = 0.1 #change in time in (ms)
t_end = 500 #time end of code/model (ms)
t_input_start = 100 #time input current injected (ms)
t_input_end = 400 #time input current ended (ms)

V_r = -70 #resting membrane potential (mV)
V_th = -55 #activation potential (mV) - V and R_m defined later
V_hyp = -75 #hyperpolarisation (reset) potential (mV)
V_dep = 30 #maximal depolarisation potential (mV)
V_i = 0 #baseline to be updated later (to allow for indication of use of global variables)
V_last = V_r #baseline to be updated

R_m = 10 #membrane resistance (MOhm)
tau = 10 #membrane time constant (ms)
"""membrane time constant different for different types of neurons (measure of how quickly a membrane potential changes
   - fast spiking neurons = 11.9 +/- 6.5 ms
   - regular neurons = 20.2 +/- 14.6 ms)"""

I = 1 #injected current (nA)
I_t = 1.43 #current magnitude of injected current (nA) - set to minimum value to b undated
I_t_min = 1.43 #magnitude of injected current min (nA)
I_t_max = 1.63 #magnitude of injected current max (nA)
I_int = 0.04 #magnitude of intervals of ijected current increase (nA)
I_th = (V_th - V_r)/R_m #current required to induce action potential


"""counters: """
current_time = 0 #(counter)
V_i_values = [V_r]
time = [0]
spikes = 0
spiked_V = []
spiked_t = []
I_t_values = [1.43]
AveRate = 0
AveRate_values = []

currents_above_V_th = []
r_isi_values = []


def reset():
    global current_time, V_i_values, time, spikes, spiked_V, spiked_t

    current_time = 0
    V_i_values = [V_r]
    time = [0]
    spikes = 0
    spiked_V = []
    spiked_t = []
def I_conditions():
    global current_time, t_input_start, t_input_end, I, I_t_values

    if current_time < t_input_start or current_time > t_input_end:
        I = 0
    if current_time > t_input_start and current_time < t_input_end:
        I = I_t_values[I_t_i]
def voltage_calc():
    global V, V_r, I, R_m, V_i, V_last, dt, tau

    V = V_r + (I*R_m)
    V_i = V + (V_last - V)*math.exp(-dt/tau) #[-1] = previous item in list

    V_i_values.append(V_i)
    
    if V_i > V_th:
        V_i =  V_hyp #implies spike occurance, allows for counting of spikes occured
        #causes issues - resetting at this point means value can no longer be used
        spiking_setting()
    
    V_last = V_i
def spiking_setting():
    global spikes, spiked_index, spiked_V, spiked_t
    
    spikes = spikes + 1
    spiked_index = len(V_i_values) - 1  
    spiked_V.append(V_dep)
    spiked_t.append(time[spiked_index])
def average_spiking_calc():
    global AveRate, spikes, t_input_end, t_input_start

    AveRate = 1000*spikes/(t_input_end - t_input_start)
    AveRate_values.append(AveRate)
def theoretical_spiking_calc():
    global I, I_t_values, I_th, r_isi, tau, V_hyp, V_r, R_m, V_th, r_isi_values
    for I in range(len(I_t_values)):
        if I_t_values[I] >= I_th:
            r_isi = 1000/(tau*(math.log(((V_hyp - V_r - I_t_values[I]) * R_m)/(V_th - V_r - I_t_values[I] * R_m))))
        else:
            r_isi = 0
        
        r_isi_values.append(r_isi)
def results_display_per_I():
    global spikes, AveRate

    print("Number of action potentials reached occured: " + str(spikes))
    print("Average rate of action potential generation: " + str(AveRate) + " (Hz)")
def comparative_spiking():
    global I_t_values, r_isi_values, AveRate_values

    for index in range(len(I_t_values)):
        print("For: " + str(I_t_values[index]) + "\n" + 
            "Theoretical spiking rate:" + str(r_isi_values[index]) + "\t Average spiking rate: " + str(AveRate_values[index]) + "\n")



while I_t <= I_t_max:
    I_t = I_t + I_int #change so 0.04 is a mutable interval 
    I_t_values.append(round(I_t, 2))

for I_t_i in range(len(I_t_values)):
    
    while current_time <= t_end:
        current_time = current_time + dt
        time.append(current_time)

        I_conditions()
        
        voltage_calc()

    average_spiking_calc()


    plt.subplot(1, 6, I_t_i+1)
    plt.plot(time, V_i_values)
    for point in range(0, spikes):
        plt.axvline(x = spiked_t[point], ymin = 0, ymax = V_dep)
    if I_t_i == 0:
        plt.xlabel("time (ms)")
        plt.ylabel("Voltage (mV)")
    plt.ylim((V_r, V_dep)) #y axis will extend from resting to depolarised state
    plt.title(str(I_t_values[I_t_i]) + " nA")
    

    results_display_per_I()
    print("V_i = " + str(V_i))

    reset()

theoretical_spiking_calc()

plt.figure()
plt.xlabel("Injected Current (nA)")
plt.ylabel("Theoretical firing rate")
plt.scatter(I_t_values, r_isi_values, color = "red")
plt.plot(I_t_values, r_isi_values, color = "black")

comparative_spiking()



plt.show()