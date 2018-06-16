import numpy as np
import pandas as pd
from read_amr import ReadAmr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tr
from joblib import Parallel, delayed
import multiprocessing
import grid_plot as grplot
from PIL import Image
import general_plot as gp
import os
import pandas as pd

OUTPUT_PATH = '../_output'
def var_plot(num_ens, timestep, fortfile = '../_output/fort.q0005'):
    
    print "Plotting stddev at timestep ", timestep
    #fortfile = "../Assimilated_results/localization_effect/35_obs/radius_15/_output/fort.q0005"


    state_df = pd.DataFrame()
    for p in range(num_ens):

        fortfile = os.path.join(OUTPUT_PATH, '_output_'+str(p)+'_for', 'fort.q'+str(timestep).zfill(4))

        file1 = ReadAmr(fortfile, sort_in_frame=False)
        file1 = file1.pandas_dataframe
        file1 = file1[np.isclose(file1.amrlevel, 1.0)]

        col = 'ens'+str(p)
        state_df[col] = file1.eta


    stddev = state_df.std(axis=1).values

    title = 'Standard deviation | Assimilation step ' + str(timestep)
    savefile = 'var' + str(timestep).zfill(4) + '.pdf'
    gp.general_plot(file1, stddev, 0.0, 0.03, title = title, savefile = savefile, colorbar=True)
    #vmin = np.min(stddev)
    #vmax = np.max(stddev)
    #gp.general_plot(file1, stddev, vmin, vmax, title = title, savefile = savefile, colorbar=True)


def plot_parallel(timesteps):
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(var_plot)(30,timestep) for timestep in timesteps)


if __name__ == "__main__":
    import imageio
    #timesteps = np.arange(3, 12)
    timesteps = np.arange(52, 89)
    
    # *** Plot stddev ***
    plot_parallel(timesteps)

    # *** Construct GIF ***
    print "Making GIF... "
    #var_images_array = []
    #var_images_list = ["var" + str(i) + ".png" for i in timesteps]
    #for var_image in var_images_list:
    #    im = imageio.imread(var_image)
    #    var_images_array.append(im)
    grplot.grid2gif4("var*.pdf", 'variance.gif')

    print "Process done"
