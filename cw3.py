import numpy as np
import matplotlib.pyplot as plt
import time

global cond_sp
global syn_amp

def updateSum(y):
	global cond_sp
	global syn_amp
	sum = 0
	for a in range(0, 40):
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

def initAmp(time):
	global syn_amp
	s = np.exp(-time / 2)
	for i in range(0, 40):
		syn_amp[i] = s

		
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
	for i in range(0, 40):
		syn_amp = np.append(syn_amp, 0)
	
	spike_or_nah = np.array([])
	for i in range(0, 40):
		spike_or_nah = np.append(spike_or_nah, -1)
        
    
	y[0] = y0
	
    
	for i in range(1, n):
		# keep track of time
		time_ms = i
		# initialise prob of synaptic inputs
		sp = spikes(sp)
		# initialise s
		initAmp(time_ms)
		#print cond_sp
		#print syn_amp
		# check if there were spikes last time
		for a in spike_or_nah:
			if spike_or_nah[a] == 0:
				syn_amp[a] += 1
		# update sum of synaptic inputs
		sum = updateSum(y[i])
		# reset array
		for b in spike_or_nah:
			spike_or_nah[b] = -1
		# euler method
		y[i] = deltax * (((-y[i-1] + v) / m + sum) / c) + y[i-1]
		# check for spikes in synaptic input
		for j in range(0, 40):
			if sp[j] < (f_rate * deltax):
				# store time
				pre_times = np.append(pre_times, time_ms)
				# find delta t
				deltat = post_times[len(post_times)-1] - pre_times[len(pre_times)-1]
				# update spike conductance
				cond_sp[j] += updateCon(a_neg, a_plus, t_neg, t_plus, deltat)
				# check conductance limits
				if cond_sp[j] > 2.0:
					cond_sp[j] = 2.0
				elif cond_sp[j] < 0:
					cond_sp[j] = 0
				spike_or_nah[j] = 0
		# check if spike happened
		if y[i] > s:
			# reset y
			y[i] = r
			# store time
			post_times = np.append(post_times, time_ms)
			# find delta t
			deltat = post_times[len(post_times)-1] - pre_times[len(pre_times)-1]
			# update all conductances
			for k in range(0, 40):
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


		


