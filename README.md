# Neuron-Models

## Basic Fire and Integrate model
The fire and integrate model is a single neuron model, here used to graph the change in voltage and find a theoretical and avergae spiking rate of a neuron over time in response to the external application of a constant current. 

The fire and integrate model is a simplified model, not considering factors such as the roles of ion channels (such as in the hodgkin-huckley model of the neuron).



### Sources:
https://goldmanlab.faculty.ucdavis.edu/wp-content/uploads/sites/263/2016/07/IntegrateFire.pdf

Koch, C. (1999). Biophysics of computation : information processing in single neurons. New York: Oxford Univ. Press.

## Hodgkin-Huxley Fire and Integrate model
The hodgkin-huxley neuron model models the voltage and time dependent conductance of channels, adding complexity to the fire and integrate model of the neuron. The consideration of ion channels is represented by the activation variables m and n, and inactivation varibale h. These represent a probability for channel opening.
A combination of m and h variables dicatate the 'opening' of Na<sup>+<sup> channels (seen in graphed results as m<sup>3<sup>(100h)), and variable n dictates the 'opening' of K<sup>+<sup> channels.

Here, different graphs displaying the change in Hodgkin-huckley variables (m, h, n and V) over time in response to the external application of a constant current can be visualised. An average firing rate through different time intervals can also be found.


### Sources:
https://goldmanlab.faculty.ucdavis.edu/wp-content/uploads/sites/263/2016/07/HodgkinHuxley.pdf

Koch, C. (1999). Biophysics of computation : information processing in single neurons. New York: Oxford Univ. Press.

neuronaldynamics.epfl.ch. (2014). 2.2 Hodgkin-Huxley Model | Neuronal Dynamics online book. [online] Available at: https://neuronaldynamics.epfl.ch/online/Ch2.S2.html.