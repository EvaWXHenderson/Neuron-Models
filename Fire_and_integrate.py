import math
import matplotlib.pyplot as plt



"""values: """
dt = 0.1 #change in time in (ms)
t_end = 500 #time end of code/model (ms)
t_input_start = 100 #time input current injected (ms)
t_input_end = 400 #time input current ended (ms)
I = 1 #injected current (nA)
I_t = 1.55 #current magnitude of injected current (nA) - set to minimum value to b undated


V_r = -70 #resting membrane potential (mV)
V_th = -55 #activation potential (mV)
V_hyp = -75 #hyperpolarisation (reset) potential (mV)
V_dep = 30 #maximal depolarisation potential (mV)

R_m = 10 #membrane resistance (MOhm)
tau = 10 #membrane time constant (ms)
"""membrane time constant different for different types of neurons (measure of how quickly a membrane potential changes
   - fast spiking neurons = 11.9 +/- 6.5 ms
   - regular neurons = 20.2 +/- 14.6 ms)"""




"""counters: """
current_time = 0 #(counter)
V_i_values = [V_r]
time = [0]
spikes = 0
spiked_V = []
spiked_t = []



"""model: """
while current_time <= t_end:
    current_time = current_time + dt
    time.append(current_time)
    if current_time < t_input_start or current_time > t_input_end:
        I = 0
    if current_time > t_input_start and current_time < t_input_end:
        I = I_t
    
    V = V_r + (I*R_m)
    V_i = V + (V_i_values[-1] - V)*math.exp(-dt/tau) #[-1] = previous item in list
    
    if V_i > V_th:
        V_i =  V_hyp #implies spike occurance, allows for counting of spikes occured
        spikes = spikes + 1
        spiked_index = len(V_i_values)
        spiked_V.append(V_dep)
        spiked_t.append(time[spiked_index])

    V_i_values.append(V_i)

AveRate = 1000*spikes/(t_input_end - t_input_start) 



"""printing found values: """
print("Number of action potentials reached occured: " + str(spikes))
print("Average rate of action potential generation: " + str(AveRate) + " (Hz)")



"""plotting graph: """
plt.plot(time, V_i_values)
for point in range(0, spikes):
    plt.axvline(x = spiked_t[point], ymin = 0, ymax = V_dep)
plt.xlabel("time (ms)")
plt.ylabel("Voltage (mV)")
plt.ylim((V_r, V_dep)) #y axis will extend from resting to depolarised state
plt.title("Integrate and Fire Model")
plt.show()