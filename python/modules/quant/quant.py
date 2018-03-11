#!/usr/bin/env python

import pandas as pd

def RSI(close, window, avg='sma'):

	# - Price differences
	delta = close.diff()

	# - Omit first row (nan)
	delta[0] = 0
	
	# - Create the positive gains (up) and negative gains (down)
	up, down = delta.copy(), delta.copy()
	up[up < 0] = 0
	down[down > 0] = 0
	
	if avg == 'ewma':
		# Calculate the EWMA
		roll_up   = pd.stats.moments.ewma(up, window)
		roll_down = pd.stats.moments.ewma(down.abs(), window)
	elif avg == 'sma':
		roll_up   = pd.rolling_mean(up, window)
		roll_down = pd.rolling_mean(down.abs(), window)
	else:
		print('Unknown average {}.'.format(avg))
	
	# Calculate the RSI based on EWMA
	RS = roll_up / roll_down
	RSI = 100.0 - (100.0 / (1.0 + RS))

	return RSI
