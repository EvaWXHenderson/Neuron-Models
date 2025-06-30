# Neuron-Models

## Basic Fire and Integrate model
The fire and integrate model is a single neuron model, here used to graph the change in voltage and find a theoretical and avergae spiking rate of a neuron over time in response to the external application of a constant current. 

The fire and integrate model is a simplified model, not considering factors such as the roles of ion channels (such as in the hodgkin-huckley model of the neuron).

This implementation is used to visualise the spiking rates and patterns associated with differing input currents (nA) displayed in the below figures:
<p align="center">
  <img src="https://github.com/EvaWXHenderson/Neuron-Models/blob/main/images/fire%26integrate-1.png" width="800" alt="Spiking Graphs">
</p>
<p>
  <em> Figure from Fire_&_Integrate.py displaying change in voltage(mV) against time(secs) as a result of differing input currents(nA).</em>
</p>

<p align="center">
  <img src="https://github.com/EvaWXHenderson/Neuron-Models/blob/main/images/Figure_2.png" width="400" alt="Theoretical Spiking">
</p>
<p>
  <em> Figure from Fire_&_Integrate.py displaying a comparison of theoretical spiking rates corresponding to differing input currents(nA).</em>
</p>

### Sources:
https://goldmanlab.faculty.ucdavis.edu/wp-content/uploads/sites/263/2016/07/IntegrateFire.pdf

Koch, C. (1999). Biophysics of computation : information processing in single neurons. New York: Oxford Univ. Press.

<br />
<br />
<br />

## Hodgkin-Huxley Fire and Integrate model
The hodgkin-huxley neuron model models the voltage and time dependent conductance of channels, adding complexity to the fire and integrate model of the neuron. The consideration of ion channels is represented by the activation variables m and n, and inactivation varibale h. These represent a probability for channel opening.
A combination of m and h variables dicatate the 'opening' of Na<sup>+</sup> channels (seen in graphed results as m<sup>3</sup>(100h)), and variable n dictates the 'opening' of K<sup>+</sup> channels.

Here, graphs displaying the comparative or singular variable change in Hodgkin-huckley variables (m, h, n and V) over time in response to the external application of a constant current can be visualised. An average firing rate through different time intervals can also be found (displayed in figures below).

<p align="center">
  <img src="https://github.com/EvaWXHenderson/Neuron-Models/blob/main/images/Figure_1.png" width="400" alt="Theoretical Spiking">
</p>
<p>
  <em> Figure from Hodgkin-huxley.py displaying change in (scaled) hodgkin-huxley variables (V, m, h, n, etc.) against time(secs) as a result of an input currents of 200 nA/mm^2.</em>
</p>

<p align="center">
  <img src="https://github.com/EvaWXHenderson/Neuron-Models/blob/main/images/Figure_3.png" width="400" alt="Theoretical Spiking">
</p>
<p>
  <em> Figure from Hodgkin-huxley.py displaying a single variable graph of the change in voltage(nA) against time(secs) as a result of an input currents of 200 nA/mm^2.</em>
</p>

### Sources:
https://goldmanlab.faculty.ucdavis.edu/wp-content/uploads/sites/263/2016/07/HodgkinHuxley.pdf

Koch, C. (1999). Biophysics of computation : information processing in single neurons. New York: Oxford Univ. Press.

neuronaldynamics.epfl.ch. (2014). 2.2 Hodgkin-Huxley Model | Neuronal Dynamics online book. [online] Available at: https://neuronaldynamics.epfl.ch/online/Ch2.S2.html.
