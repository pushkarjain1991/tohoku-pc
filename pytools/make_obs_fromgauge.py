import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob, os

dart_info = {#'21401':[152.583, 42.617], 
             #'21413':[152.1167, 30.5153], 
             '21414':[178.281, 48.938], 
             #'21415':[171.849, 50.183],
             '21418':[148.694, 38.711],
             '21419':[155.736, 44.455],
             #'46411':[232.918, 39.333]}
             '51407':[203.484, 19.642]}
             #'52402':[154.116, 11.883]}

#obs_time_list = np.linspace(tstart, tstop, nstops)
#obs_time_list = np.arange(7488.0, 57601.0, 1152.0)
obs_time_list1 = np.arange(7356.0, 15157.0, 600.0)
obs_time_list2 = np.arange(15576.0, 43176.0, 1200.0)
obs_time_list = np.append(obs_time_list1, obs_time_list2)

# Remove obs files if they exist
# This is needed as obs files are created in append mode
for f in glob.glob('obs*.txt'):
    os.remove(f)

for dart in dart_info:
    obs_data = pd.read_csv('../dart/' + dart + '_notide.txt', names=['time','wse'], index_col=False, sep=" " )

    extracted_data = obs_data[np.isclose(obs_data['time'].values[:,None], obs_time_list).any(axis=1)]

    first_val = extracted_data.groupby('time', as_index=False).first()
    first_val['timestep'] = first_val.time/3600.0
    print dart
    print first_val
    #first_val.plot('time','wse',ax=ax1)

    mean_val = extracted_data.groupby('time', as_index=False).mean()

    #fig, ax1 = plt.subplots()
    #mean_val.plot('time', 'wse',ax=ax1)
    #plt.legend(['first', 'mean'])
    #plt.show()

    for i, (t,elevation) in enumerate(zip(first_val.time, first_val.wse)):
        savefile = "obs_step" + str(i+1) + ".txt"
        if t in obs_time_list:
            with open(savefile, 'a') as f1:
                f1.write(str(dart_info[dart][0]) + " " + str(dart_info[dart][1]) + " " + str(elevation))
                f1.write("\n")
