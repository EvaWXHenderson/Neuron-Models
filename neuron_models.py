import math
import matplotlib.pyplot as plt


"""FIRE & INTEGRATE MODEL:"""
class fire_integrate:

    def __init__(self, input_start = 100, input_end = 400, end = 500, time_int = 0.1, I_min = 1.43, I_max = 1.63, I_interval = 0.04, Rm = 10, Tau = 10, Vrest = -70, Vthreshold = -55, VHyp = -75, VDep = 30): 
        """values: """
        self.dt = time_int #change in time in (ms)
        self.t_end = end #time end of code/model (ms)
        self.t_input_start = input_start #time input current injected (ms)
        self.t_input_end = input_end #time input current ended (ms)

        self.V_r = Vrest #resting membrane potential (mV)
        self.V_th = Vthreshold #activation potential (mV) - V and R_m defined later
        self.V_hyp = VHyp #hyperpolarisation (reset) potential (mV)
        self.V_dep = VDep #maximal depolarisation potential (mV)
        self.V_i = 0 #baseline to be updated later (to allow for indication of use of global variables)
        self.V_last = self.V_r #baseline to be updated

        self.R_m = Rm #membrane resistance (MOhm)
        self.tau = Tau #membrane time constant (ms)

        self.I = 1 #injected current (nA)
        self.I_t_min = I_min #magnitude of injected current min (nA)
        self.I_t_max = I_max #magnitude of injected current max (nA)
        self.I_t = self.I_t_min #current magnitude of injected current (nA) - set to minimum value to b undated
        self.I_int = I_interval #magnitude of intervals of ijected current increase (nA)
        self.I_th = (self.V_th - self.V_r)/self.R_m #current required to induce action potential

        """counters: """
        self.current_time = 0 
        self.V_i_values = [self.V_r]
        self.time = [0]
        self.spikes = 0
        self.spiked_V = []
        self.spiked_t = []
        self.I_t_values = [self.I_t_min]
        self.AveRate = 0
        self.AveRate_values = []

        self.currents_above_V_th = []
        self.r_isi_values = []

    def reset(self):
        self.current_time = 0
        self.V_i_values = [self.V_r]
        self.time = [0]
        self.spikes = 0
        self.spiked_V = []
        self.spiked_t = []
    
    def I_conditions(self,I_t_i):
        if self.current_time < self.t_input_start or self.current_time > self.t_input_end:
            I = 0
        if self.current_time > self.t_input_start and self.current_time < self.t_input_end:
            self.I = self.I_t_values[I_t_i]
    
    def voltage_calc(self):
        self.V = self.V_r + (self.I*self.R_m)
        self.V_i = self.V + (self.V_last - self.V)*math.exp(-self.dt/self.tau)

        self.V_i_values.append(self.V_i)
        
        if self.V_i > self.V_th:
            self.V_i = self.V_hyp
            self.spiking_setting()
        
        self.V_last = self.V_i
   
    def spiking_setting(self):
        self.spikes = self.spikes + 1
        self.spiked_index = len(self.V_i_values) - 1  
        self.spiked_V.append(self.V_dep)
        self.spiked_t.append(self.time[self.spiked_index])
    
    def average_spiking_calc(self):
        self.AveRate = 1000*self.spikes/(self.t_input_end - self.t_input_start)
        self.AveRate_values.append(self.AveRate)
    
    def theoretical_spiking_calc(self):
        for I in range(len(self.I_t_values)):
            if self.I_t_values[I] >= self.I_th:
                self.r_isi = 1000/(self.tau*(math.log(((self.V_hyp - self.V_r - self.I_t_values[I]) * self.R_m)/(self.V_th - self.V_r - self.I_t_values[I] * self.R_m))))
            else:
                self.r_isi = 0
            
            self.r_isi_values.append(self.r_isi)
    
    def results_display_per_I(self):
        print("Number of action potentials reached occured: " + str(self.spikes))
        print("Average rate of action potential generation: " + str(self.AveRate) + " (Hz)")
    
    def comparative_spiking(self):
        for index in range(len(self.I_t_values)):
            print("For: " + str(self.I_t_values[index]) + "\n" + 
                "Theoretical spiking rate:" + str(self.r_isi_values[index]) + "\t Average spiking rate: " + str(self.AveRate_values[index]) + "\n")

def run_FI(model):
        while model.I_t <= model.I_t_max:
            model.I_t = model.I_t + model.I_int
            model.I_t_values.append(round(model.I_t, 2))

        for I_t_i in range(len(model.I_t_values)):
            
            while model.current_time <= model.t_end:
                model.current_time += model.dt
                model.time.append(model.current_time)

                model.I_conditions(I_t_i)
                
                model.voltage_calc()

            model.average_spiking_calc()


            plt.subplot(1, 6, I_t_i+1)
            plt.plot(model.time, model.V_i_values)
            for point in range(0, model.spikes):
                plt.axvline(x = model.spiked_t[point], ymin = 0, ymax = model.V_dep)
            if I_t_i == 0:
                plt.xlabel("time (ms)")
                plt.ylabel("Voltage (mV)")
            plt.ylim((model.V_r, model.V_dep)) #y axis will extend from resting to depolarised state
            plt.title(str(model.I_t_values[I_t_i]) + " nA")
            

            model.results_display_per_I()

            model.reset()

        model.theoretical_spiking_calc()

        plt.figure()
        plt.xlabel("Injected Current (nA)")
        plt.ylabel("Theoretical firing rate")
        plt.scatter(model.I_t_values, model.r_isi_values, color = "red")
        plt.plot(model.I_t_values, model.r_isi_values, color = "black")

        model.comparative_spiking()

        plt.show()



"""HODGKIN-HUCKLEY MODEL"""
class hodgkin_huxley:
    def __init__(self, dt = 0.1, input_start = 10, input_end = 60, end = 70, c = 10, I = 200, VRest = -70, VThresh = -50):
        self.DT = dt #change in time in (ms)
        self.T_END = end #duration (ms)
        self.T_STIM_START = input_start #time start of current injection (ms)
        self.T_STIM_END = input_end #time end of current injection (ms)
        self.T_COUNT_START = self.T_STIM_START + 200 #(ms)

        self.C = c #capacitance per unit area(nF/mm^2)

        self.I_0 = I # magnitude of injected current (nA/mm^2)

        self.V_th = VThresh #threshold potential (mV)
        self.V_r = VRest

        self.G_MAX_L = 0.003*10**3 #leak
        self.G_MAX_K = 0.39*10**3 #potassium (K+) 
        self.G_MAX_NA = 1.2*10**3 #sodium (Na+)
        
        self.E_L = -54.387 #leak 
        self.E_K = -77 #potassium
        self.E_NA = 50 #sodium

        self.current_time = 0
        self.time = [0]
        self.I_t_values = [0]

        self.spikes = 0
                
        self.V_values = [self.V_r] #intital value

        self.m_inf, self.tau_m = self.variable_inf_calc("m")
        self.m_values = [self.m_inf] #intital value for V = -65
        self.g1_m_values = [self.m_inf*100] #modified values for graphing (g)
        self.g2_m_values = [(self.m_inf**3)*100]

        self.h_inf, vtau_h = self.variable_inf_calc("h")
        self.h_values = [self.h_inf] #intital value for V = -65
        self.g_h_values = [self.h_inf*100]

        self.n_inf, self.tau_n = self.variable_inf_calc("n")
        self.n_values = [self.n_inf] #intital value for V = -65
        self.g1_n_values = [self.n_inf*100]
        self.g2_n_values = [(self.n_inf**4)*100]

        self.g2_m3_h_values = [(self.m_inf**3)*self.h_inf*100]

        self.V_inf, self.tau_V = self.variable_inf_calc("V")

    def alpha_beta_assign(self, variable):
        if variable == "m":
            self.A_m = (0.1*(self.V_values[-1] + 40))/(1-math.exp(-0.1*(self.V_values[-1] + 40)))
            self.B_m = 4*math.exp(-0.0556*(self.V_values[-1]+65))
            return self.A_m, self.B_m
        
        if variable == "h":
            self.A_h = 0.07*math.exp(-0.05*(self.V_values[-1] + 65))
            self.B_h = 1/(1+math.exp(-0.1*(self.V_values[-1] + 35)))
            return self.A_h, self.B_h
        
        if variable == "n":
            self.A_n = (0.01*(self.V_values[-1] + 55))/(1-math.exp(-0.1*(self.V_values[-1] + 55)))
            self.B_n = 0.125*math.exp(-0.0125*(self.V_values[-1]+65))
            return self.A_n, self.B_n
    
    def variable_inf_calc(self, variable):
        if variable == "m":
            self.A_m, self.B_m = self.alpha_beta_assign("m")
            self.m_inf = self.A_m/(self.A_m + self.B_m)
            self.tau_m = 1/(self.A_m + self.B_m)
            return self.m_inf, self.tau_m

        if variable == "h":
            self.A_h, self.B_h = self.alpha_beta_assign("h")
            self.h_inf = self.A_h/(self.A_h + self.B_h)
            self.tau_h = 1/(self.A_h + self.B_h)
            return self.h_inf, self.tau_h
        
        if variable == "n":
            self.A_n, self.B_n = self.alpha_beta_assign("n")
            self.n_inf = self.A_n/(self.A_n + self.B_n)
            self.tau_n = 1/(self.A_n + self.B_n)
            return self.n_inf, self.tau_n 
        
        if variable == "V":
            self.V_inf = ((self.G_MAX_L*self.E_L) + (self.G_MAX_K*(self.n_values[-1]**4)*self.E_K)+(self.G_MAX_NA*(self.m_values[-1]**3)*self.h_values[-1]*self.E_NA + self.I_t_values[-1]))/(self.G_MAX_L + (self.G_MAX_K*(self.n_values[-1]**4)) + (self.G_MAX_NA*(self.m_values[-1]**3)*self.h_values[-1]))
            self.tau_V = self.C/(self.G_MAX_L + (self.G_MAX_K*(self.n_values[-1]**4)) + (self.G_MAX_NA*(self.m_values[-1]**3)*self.h_values[-1]))
            return self.V_inf, self.tau_V
    
    def variable_calc(self, variable):
        if variable == "m":
            self.m = self.m_inf + (self.m_values[-1] - self.m_inf)*math.exp(-self.DT/self.tau_m)
            return self.m
        
        if variable == "h":
            self.h = self.h_inf + (self.h_values[-1] - self.h_inf)*math.exp(-self.DT/self.tau_h)
            return self.h
        
        if variable == "n":
            self.n = self.n_inf + (self.n_values[-1] - self.n_inf)*math.exp(-self.DT/self.tau_n)
            return self.n
        
        if variable == "V":
            self.V = self.V_inf + (self.V_values[-1] - self.V_inf)*math.exp(-self.DT/self.tau_V)
            return self.V
        
    def counting_interval(self):
        for index in range(len(self.time)-1):
            if self.time[index] > self.T_COUNT_START and self.time[index] <= self.T_STIM_END:
                if self.V_values[-1] < self.V_th and self.V_values[index + 1] > -50:
                    self.spikes += 1
    
    def average_spiking_rate(self):
        self.AveSRate = 1000*self.spikes/(self.T_STIM_END - self.T_COUNT_START)
        return self.AveSRate
    
    def results(self, no_spikes = True, AveRate = True):
        if no_spikes == True:
            print("No. spikes with applied current of " + str(self.I_0) + " nA/mm^2 (over " + str(self.T_COUNT_START - self.T_STIM_END) + " s): " + str(self.spikes))

        if AveRate == True:
            print("Average spiking rate: " + str(round(self.average_spiking_rate())) + "(Hz)")

def run_HH(model):
    while model.current_time <= model.T_END:
        model.current_time = model.current_time + model.DT
        model.time.append(model.current_time)

        if model.current_time < model.T_STIM_START or model.current_time >= model.T_STIM_END:
            model.I = 0
            model.I_t_values.append(model.I)
        if model.current_time >= model.T_STIM_START and model.current_time < model.T_STIM_END:
            model.I = model.I_0
            model.I_t_values.append(model.I)


        model.A_m, model.B_m = model.alpha_beta_assign("m")
        model.A_h, model.B_h = model.alpha_beta_assign("h")
        model.A_n, model.B_n = model.alpha_beta_assign("n")
        

        model.V_inf, model.tau_V = model.variable_inf_calc("V")
        model.V = model.variable_calc("V")
        model.V_values.append(model.V)

        #m = variable_calc("m")
        model.m_inf, model.tau_m = model.variable_inf_calc("m")
        model.m = model.variable_calc("m")
        model.g1_m_values.append(model.m*100)
        model.g2_m_values.append((model.m**3)*100)
        model.m_values.append(model.m)

        #h = variable_calc("h")
        model.h_inf, model.tau_h = model.variable_inf_calc("h")
        model.h = model.variable_calc("h")
        model.g_h_values.append(model.h*100)
        model.h_values.append(model.h)

        #n = variable_calc("n")
        model.n_inf, model.tau_n = model.variable_inf_calc("n")
        model.n = model.variable_calc("n")
        model.g1_n_values.append(model.n*100)
        model.g2_n_values.append((model.n**4)*100)
        model.n_values.append(model.n)

        model.g2_m3_h_values.append((model.m**3)*model.h*100)

    model.counting_interval()
    model.results()

def hh_graph(model, type, scaled, variable = False):
    if type == "single":
        if scaled == "no":
            if variable == "m":
                plt.plot(model.time, model.m_values)
            elif variable == "h":
                plt.plot(model.time, model.h_values)
            elif variable == "n":
                plt.plot(model.time, model.n_values)
            elif variable == "V":
                plt.plot(model.time, model.V_values)
                plt.ylabel("Voltage (nA)")
            
            plt.xlabel("time (secs)")

        if scaled == "yes":
            if variable == "m":
                plt.plot(model.time, model.g1_m_values)
            elif variable == "h":
                plt.plot(model.time, model.g_h_values)
            elif variable == "h":
                plt.plot(model.time, model.g1_n_values)
            elif variable == "V":
                plt.plot(model.time, model.V_values)
                plt.ylabel("Voltage (nA)")
            
            plt.xlabel("time (secs)")
    
    if type == "comparison":
        if scaled == "no":
            plt.plot(model.time, model.V_values, color = "blue")
            plt.plot(model.time, model.g1_m_values, color = "black")
            plt.plot(model.time, model.g_h_values, color = "red")
            plt.plot(model.time, model.g1_n_values, color = "green")
            plt.xlabel("Voltage (nA)")
            plt.ylabel("Time (ms)")
            plt.legend(["Voltage", "m*100" , "h*100", "n*100"], loc = "lower right")
            plt.xlim(0, model.T_END)
            plt.ylim(model.V_values[0] - 15, 100)
        elif scaled == "yes":
            plt.plot(model.time, model.V_values, color = "blue")
            plt.plot(model.time, model.g2_m_values, color = "black")
            plt.plot(model.time, model.g_h_values, color = "red")
            plt.plot(model.time, model.g2_n_values, color = "green")
            plt.plot(model.time, model.g2_m3_h_values, color = "magenta")
            plt.xlabel("Voltage (nA)")
            plt.ylabel("Time (ms)")
            plt.legend(["Voltage", "m^3*100" , "h*100", "n^4*100", "m^3*h*100"], loc = "lower right")
            plt.xlim(0, model.T_END)
            plt.ylim(model.V_values[0] - 15, 100)
    
    plt.show()