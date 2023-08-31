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
from pandas import DataFrame
from scipy.stats.mstats import gmean


import numpy as np

#define custom function
def g_mean(x):
    a = np.log(x)
    return np.exp(a.mean())


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    
    print("Folder path:", folder_path)

    if not os.path.isdir(folder_path):
        print("Error: The specified path is not a directory.")
        sys.exit(1)

    xticks = ["0","1", "$\mathregular{2^3}$", "$\mathregular{2^{6}}$", "$2^{9}$", "$2^{12}$", "$2^{15}$", "$2^{18}$", "$2^{21}$"]
  
    sandcrust = pd.read_csv( folder_path + "/sandcrust_output.txt", sep=',',  header=None)
    baseline = pd.read_csv( folder_path + "/empty_output.txt", sep=',',  header=None)
    sdrob = pd.read_csv( folder_path + "/sdrob_bincode_output.txt", sep=',',  header=None)
    sdrob_bin_v2 = pd.read_csv( folder_path + "/sdrob_bincodev2_output.txt", sep=',',  header=None)
    sdrob_abon_v1 = pd.read_csv( folder_path + "/sdrob_abon_v1_output.txt", sep=',',  header=None)
    sandcrust.columns = ['version', 'buff size', 'execution time', 'std']
    baseline.columns = ['version','buff size', 'execution time', 'std']
    sdrob.columns = ['version','buff size', 'execution time', 'std']
    sdrob_bin_v2.columns = ['version','buff size', 'execution time', 'std']
    sdrob_abon_v1.columns = ['version','buff size', 'execution time', 'std']
  
    # Compress and decompress
    sandcrust_compress = sandcrust[sandcrust["version"] == "compress"].reset_index(drop=True)
    baseline_compress = baseline[baseline["version"]== "compress"].reset_index(drop=True)
    sdrob_compress = sdrob[sdrob["version"] == "compress"].reset_index(drop=True)
    sdrob_bin_v2_compress = sdrob_bin_v2[sdrob_bin_v2["version"] == "compress"].reset_index(drop=True)
    sdrob_abon_v1_compress = sdrob_abon_v1[sdrob_abon_v1["version"]== "compress"].reset_index(drop=True)
    sandcrust_decompress = sandcrust[sandcrust["version"] == "decompress"].reset_index(drop=True)
    print(sandcrust_decompress)
    baseline_decompress = baseline[baseline["version"] == "decompress"].reset_index(drop=True)
    sdrob_decompress =  sdrob[sdrob["version"] == "decompress"].reset_index(drop=True)
    sdrob_bin_v2_decompress = sdrob_bin_v2[sdrob_bin_v2["version"] == "decompress"].reset_index(drop=True)
    sdrob_abon_v1_decompress = sdrob_abon_v1[sdrob_abon_v1["version"] == "decompress"].reset_index(drop=True)

    fig, (ax0) = plt.subplots(figsize=(6,6))

    ax0.set_yscale('log')
    ax0.set(xlabel="number of bytes")
    ax0.set(ylabel="Execution Time $\mu s$")

    ax0.plot(sandcrust_compress["execution time"]/1000, label='sandcrust', marker='o')
    ax0.plot(sdrob_compress["execution time"]/1000,  label='sdrad_bincode_v1', marker='x')
    print(sdrob_compress["execution time"])
    print(gmean(sdrob_abon_v1_compress["execution time"]/1000))
    print(gmean(baseline_compress["execution time"]/1000))
    print(gmean(sandcrust_compress["execution time"]/1000))

    print(gmean(sdrob_abon_v1_decompress["execution time"]/1000))
    print(gmean(baseline_decompress["execution time"]/1000))
    print(gmean(sandcrust_decompress["execution time"]/1000))

    ax0.plot(sdrob_abon_v1_compress["execution time"]/1000,  label='sdrad_abomonation_v1', marker='*')
    ax0.plot(sdrob_bin_v2_compress["execution time"]/1000,  label='sdrad_bincode_v2', marker='+')
    ax0.plot(baseline_compress["execution time"]/1000,  label='baseline', marker='d')

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
    ax1.plot(sandcrust_decompress["execution time"]/1000,  label='sandcrust', marker='o')
    ax1.plot(sdrob_decompress["execution time"]/1000,  label='sdrad_bincode_v1',  marker='x')
    ax1.plot(sdrob_abon_v1_decompress["execution time"]/1000,  label='sdrad_abomonation_v1', marker='*')
    ax1.plot(sdrob_bin_v2_decompress["execution time"]/1000,  label='sdrad_bincode_v2',marker='+')
    ax1.plot(baseline_decompress["execution time"]/1000,  label='baseline', marker="d")
    ax1.xaxis.get_label().set_fontsize(15)
    ax1.yaxis.get_label().set_fontsize(15)
    ax1.set_xticklabels(xticks) 
    ax1.legend(fontsize = 13)
    fig.savefig(folder_path + '/figure_1_decompress.png',  bbox_inches='tight')
    plt.show()
    plt.legend()
  


if __name__ == '__main__':
    main()