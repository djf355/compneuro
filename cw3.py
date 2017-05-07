import numpy as np
import matplotlib.pyplot as plt
import time

global cond_sp
global syn_amp

def updateSum(time, y):
	global cond_sp
	global syn_amp
	global spike_or_nah
	sum = 0
	s = np.exp(-time / 2)
	for a in range(0, 40):
		if spike_or_nah[a] == -1:
			syn_amp[a] = s
		elif spike_or_nah[a] == 0:
			syn_amp[a] = s + 1
		sum += cond_sp[a] * syn_amp[a] * -y
	return sum
		
def spikes(sp):
	if len(sp) == 0:
		for i in range(0, 40):
			rand = np.random.uniform(0, 1)
			sp = np.append(sp, rand)
	else:
		for i in range(0, 40):
			rand = np.random.uniform(0, 1)
			sp[i] = rand
	return sp

def updateCon(a_neg, a_plus, t_neg, t_plus, deltat):
	if deltat <= 0:
		result = -a_neg * np.exp(-abs(deltat) / t_neg)
	elif deltat > 0:
		result = a_plus * np.exp(-abs(deltat) / t_plus)
	return result

		
def main():
	# time start and stop
	x0 = 0
	xf = 200
	# initial value
	y0 = -65
	# number of points
	n = xf * 1000 + 1
	# time step
	deltax = 0.001
	# resting potential
	v = -65
	# spike threshold
	s = -50
	# reset voltage
	r = -65
	m = 100
	# membrane capacitance
	c = 0.1
	
	
	# def x values
	x = np.linspace(x0, xf, n)

	# initialise y value array
	y = np.zeros([n])

	f_rate = 10
	g = 2
	a_plus = 0.1
	a_neg = 0.12
	t_plus = 20
	t_neg = 20
	sum = 0

    # initialize array post synaptic spikes
	post_times = np.array([])
	post_times = np.append(post_times, 0)

    # input_prob
	sp = np.array([])
	sp = spikes(sp)
        
    # intialize array pre synaptic spikes
	pre_times = np.array([])
	pre_times = np.append(pre_times, 0)
	
	global cond_sp
	cond_sp = np.array([])
	for i in range(0, 40):
		cond_sp = np.append(cond_sp, 2.0)
	
	global syn_amp
	syn_amp = np.array([])
	for a in range(0, 40):
		syn_amp = np.append(syn_amp, s)
	
	global spike_or_nah
	spike_or_nah = np.array([])
	for b in range(0, 40):
		spike_or_nah = np.append(spike_or_nah, -1)
        
    
	y[0] = y0
	sum = updateSum(0, y[0])
    
	for i in range(1, n):
		time_ms = i - 1
		sp = spikes(sp)
		y[i] = deltax * (((-(y[i-1] - v) / m) + sum) / c) + y[i-1]
		sum = updateSum(time_ms, y[i])
		for d in range(0, 40):
			spike_or_nah[d] = -1
		for j in range(0, len(sp)):
			if sp[j] < (f_rate * deltax):
				pre_times = np.append(pre_times, time_ms)
				deltat = post_times[len(post_times)-1] - pre_times[len(pre_times)-1]
				cond_sp[j] += updateCon(a_neg, a_plus, t_neg, t_plus, deltat)
				if cond_sp[j] > 2.0:
					cond_sp[j] = 2.0
				elif cond_sp[j] < 0:
					cond_sp[j] = 0
				spike_or_nah[j] = 0
		if y[i] > s:
			y[i] = r
			post_times = np.append(post_times, time_ms)
			deltat = post_times[len(post_times)-1] - pre_times[len(pre_times)-1]
			# update all conductances
			for k in range(0, len(cond_sp)):
				cond_sp[j] += updateCon(a_neg, a_plus, t_neg, t_plus, deltat)
				if cond_sp[j] > 2.0:
					cond_sp[j] = 2.0
				elif cond_sp[j] < 0:
					cond_sp[j] = 0
	
	plt.plot(x, y, 'o')
	plt.margins(0.05)
	plt.show()


	
if __name__ == "__main__":
	main()


		


