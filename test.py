import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from datetime import timedelta

times = np.linspace(0, 1, 60*60*2)
y = np.sin(2 * np.pi * times)

print("Generating dataframe")
dataframe = pd.Series(y, index=pd.date_range('14/11/2014', periods=len(times), freq='1S'))

print("Resampling dataframe")
resampled_data = dataframe.resample('%dS' % float(1*60*60), )
new_index = resampled_data.index + timedelta(seconds = float(0.5*60*60))
print(new_index)
resampled_data.index = new_index
print("Plotting resampled dataframe")
resampled_data.plot()

print("Plotting original dataframe")
dataframe.plot()
plt.show()
