# @author Merve Gulmez (merve.gulmez@ericsson.com)
# @version 0.1
# @date 2023-08-31
# @copyright (c) Ericsson AB 2023
# SPDX-License-Identifier: BSD 3-Clause 

import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
from matplotlib.font_manager import FontProperties



def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    
    print("Folder path:", folder_path)

    if not os.path.isdir(folder_path):
        print("Error: The specified path is not a directory.")
        sys.exit(1)

    xticks = ["0", "$\mathregular{2^0}$", "$\mathregular{2^3}$", "$\mathregular{2^{6}}$", "$2^{9}$", "$2^{12}$", "$2^{15}$", "$2^{18}$", "$2^{21}$"]
    # Figure 1

    sdrob_v1_00 = pd.read_csv( folder_path + "/abon_v1_output_00.txt", sep=',',  header=None)
    sdrob_v1_01 = pd.read_csv( folder_path + "/abon_v1_output_01.txt", sep=',',  header=None)
    sdrob_v1_02 = pd.read_csv( folder_path + "/abon_v1_output_02.txt", sep=',',  header=None)
    sdrob_v1_03 = pd.read_csv( folder_path + "/abon_v1_output_03.txt", sep=',',  header=None)


    sdrob_v2_00 =  pd.read_csv( folder_path + "/abon_v2_output_00.txt", sep=',',  header=None)
    sdrob_v2_01 =  pd.read_csv( folder_path + "/abon_v2_output_01.txt", sep=',',  header=None)
    sdrob_v2_02 =  pd.read_csv( folder_path + "/abon_v2_output_02.txt", sep=',',  header=None)
    sdrob_v2_03 =  pd.read_csv( folder_path + "/abon_v2_output_03.txt", sep=',',  header=None)


    # Assign column names to the data
    sdrob_v1_00.columns = ['version','buff size', 'execution time', 'std']
    sdrob_v1_01.columns = ['version','buff size', 'execution time', 'std']
    sdrob_v1_02.columns = ['version','buff size', 'execution time', 'std']
    sdrob_v1_03.columns = ['version', 'buff size','execution time', 'std']
    sdrob_v2_00.columns = ['version','buff size', 'execution time', 'std']
    sdrob_v2_01.columns = ['version','buff size', 'execution time', 'std']
    sdrob_v2_02.columns = ['version','buff size', 'execution time', 'std']
    sdrob_v2_03.columns = ['version', 'buff size','execution time', 'std']


    sdrob_v1_00_compress = sdrob_v1_00[sdrob_v1_00["version"] == "compress"].reset_index(drop=True)
    sdrob_v1_01_compress = sdrob_v1_01[sdrob_v1_01["version"] == "compress"].reset_index(drop=True)
    sdrob_v1_02_compress = sdrob_v1_02[sdrob_v1_02["version"] == "compress"].reset_index(drop=True)
    sdrob_v1_03_compress = sdrob_v1_03[sdrob_v1_03["version"] == "compress"].reset_index(drop=True)
    sdrob_v2_00_compress = sdrob_v2_00[sdrob_v2_00["version"] == "compress"].reset_index(drop=True)
    sdrob_v2_01_compress = sdrob_v2_01[sdrob_v2_01["version"] == "compress"].reset_index(drop=True)
    sdrob_v2_02_compress = sdrob_v2_02[sdrob_v2_02["version"] == "compress"].reset_index(drop=True)
    sdrob_v2_03_compress = sdrob_v2_03[sdrob_v2_03["version"] == "compress"].reset_index(drop=True)


    sdrob_v1_00_uncompress = sdrob_v1_00[sdrob_v1_00["version"] == "decompress"].reset_index(drop=True)
    sdrob_v1_01_uncompress = sdrob_v1_01[sdrob_v1_01["version"] == "decompress"].reset_index(drop=True)
    sdrob_v1_02_uncompress = sdrob_v1_02[sdrob_v1_02["version"] == "decompress"].reset_index(drop=True)
    sdrob_v1_03_uncompress = sdrob_v1_03[sdrob_v1_03["version"] == "decompress"].reset_index(drop=True)
    sdrob_v2_00_uncompress = sdrob_v2_00[sdrob_v2_00["version"] == "decompress"].reset_index(drop=True)
    sdrob_v2_01_uncompress = sdrob_v2_01[sdrob_v2_01["version"] == "decompress"].reset_index(drop=True)
    sdrob_v2_02_uncompress = sdrob_v2_02[sdrob_v2_02["version"] == "decompress"].reset_index(drop=True)
    sdrob_v2_03_uncompress = sdrob_v2_03[sdrob_v2_03["version"] == "decompress"].reset_index(drop=True)


    fig, (ax0) = plt.subplots(figsize=(6,6))

    ax0.set_yscale('log')
    ax0.set(xlabel="number of bytes")
    ax0.set(ylabel="Execution Time $\mu s$")

    ax0.plot(sdrob_v1_00_compress["execution time"]/1000, label= "v1_opt_0", marker ='x') 
    ax0.plot(sdrob_v1_01_compress["execution time"]/1000, label= "v1_opt_1", marker ='*') 
    ax0.plot(sdrob_v1_02_compress["execution time"]/1000, label= "v1_opt_2", marker ='+') 
    ax0.plot(sdrob_v1_03_compress["execution time"]/1000, label= "v1_opt_3", marker ='d') 
    ax0.plot(sdrob_v2_00_compress["execution time"]/1000, label= "v2_opt_0", marker ='o') 
    ax0.plot(sdrob_v2_01_compress["execution time"]/1000, label= "v2_opt_1", marker ='v') 
    ax0.plot(sdrob_v2_02_compress["execution time"]/1000, label= "v2_opt_2", marker ='s') 
    ax0.plot(sdrob_v2_03_compress["execution time"]/1000, label= "v2_opt_3", marker ='p') 


    ax0.set_xticklabels(xticks) 
    ax0.xaxis.get_label().set_fontsize(15)
    ax0.yaxis.get_label().set_fontsize(15)
    ax0.legend(fontsize = 13)
    fig.savefig(folder_path + '/figure_1_compress.png',  bbox_inches='tight')
    plt.show()
    plt.legend()


    fig, (ax1) = plt.subplots(figsize=(6,6))
    ax1.set_yscale('log')
    ax1.set(xlabel="number of bytes")
    ax1.set(ylabel="Execution Time $\mu s$")
    ax1.plot(sdrob_v1_00_uncompress["execution time"]/1000, label= "v1_opt_0", marker ='x') 
    ax1.plot(sdrob_v1_01_uncompress["execution time"]/1000, label= "v1_opt_1", marker ='*') 
    ax1.plot(sdrob_v1_02_uncompress["execution time"]/1000, label= "v1_opt_2", marker ='+') 
    ax1.plot(sdrob_v1_03_uncompress["execution time"]/1000, label= "v1_opt_3", marker ='d') 
    ax1.plot(sdrob_v2_00_uncompress["execution time"]/1000, label= "v2_opt_0", marker ='o') 
    ax1.plot(sdrob_v2_01_uncompress["execution time"]/1000, label= "v2_opt_1", marker ='v') 
    ax1.plot(sdrob_v2_02_uncompress["execution time"]/1000, label= "v2_opt_2", marker ='s') 
    ax1.plot(sdrob_v2_03_uncompress["execution time"]/1000, label= "v2_opt_3", marker ='p')  
    ax1.xaxis.get_label().set_fontsize(15)
    ax1.yaxis.get_label().set_fontsize(15)
    ax1.set_xticklabels(xticks) 
    ax1.legend(fontsize = 13)
    fig.savefig(folder_path + '/figure_1_decompress.png',  bbox_inches='tight')
    plt.show()
    plt.legend()


if __name__ == '__main__':
    main()