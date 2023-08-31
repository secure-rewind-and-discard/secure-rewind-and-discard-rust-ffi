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

    #xticks = [2**i for i in range(8, 23, 2)]
    #xticks = ["0", "$\mathregular{2^8}$", "$\mathregular{2^{10}}$", "$2^{12}$", "$2^{14}$", "$2^{16}$", "$2^{18}$", "$2^{20}$", "$2^{22}$"]
    xticks = ["0", "$\mathregular{2^0}$", "$\mathregular{2^3}$", "$\mathregular{2^{6}}$", "$2^{9}$", "$2^{12}$", "$2^{15}$", "$2^{18}$", "$2^{23}$"]
    # Figure 1

    # Reading the data 
    #sandcrust_cv = pd.read_csv( folder_path + "/sandcrust_cus_vec_output.txt", sep=',',  header=None)
    sdrob = pd.read_csv( folder_path + "/sdrob_abon_v1_output_release.txt", sep=',',  header=None)
    sdrob_bin_v2 = pd.read_csv( folder_path + "/sdrob_abon_v2_output_release.txt", sep=',',  header=None)
    sdrob_abon_v1 = pd.read_csv( folder_path + "/sdrob_abon_v1_output.txt", sep=',',  header=None)
    sdrob_abon_v2 = pd.read_csv( folder_path + "/sdrob_abon_v2_output.txt", sep=',',  header=None)

    # Assign column names to the data
    sdrob.columns = ['version','buff size', 'execution time', 'std']
    sdrob_bin_v2.columns = ['version','buff size', 'execution time', 'std']
    sdrob_abon_v1.columns = ['version','buff size', 'execution time', 'std']
    sdrob_abon_v2.columns = ['version', 'buff size', 'execution time', 'std']

    # Compress and decompress
    sdrob_compress = sdrob[sdrob["version"] == "compress"].reset_index(drop=True)
    sdrob_bin_v2_compress = sdrob_bin_v2[sdrob_bin_v2["version"] == "compress"].reset_index(drop=True)
    sdrob_abon_v1_compress = sdrob_abon_v1[sdrob_abon_v1["version"]== "compress"].reset_index(drop=True)
    sdrob_abon_v2_compress = sdrob_abon_v2[sdrob_abon_v2["version"] == "compress"].reset_index(drop=True)
    #sandcrust_cv_compress = sandcrust_cv.iloc[0:8:, ]

    sdrob_decompress =  sdrob[sdrob["version"] == "decompress"].reset_index(drop=True)
    sdrob_bin_v2_decompress = sdrob_bin_v2[sdrob_bin_v2["version"] == "decompress"].reset_index(drop=True)
    sdrob_abon_v1_decompress = sdrob_abon_v1[sdrob_abon_v1["version"] == "decompress"].reset_index(drop=True)
    sdrob_abon_v2_decompress = sdrob_abon_v2[sdrob_abon_v2["version"] == "decompress"].reset_index(drop=True)
    #sandcrust_cv_decompress = sandcrust_cv.iloc[8:16:, ]


    fig, (ax0) = plt.subplots(figsize=(6,6))

    ax0.set_yscale('log')
    ax0.set(xlabel="number of bytes")
    ax0.set(ylabel="Execution Time $\mu s$")

    ax0.plot(sdrob_compress["execution time"]/1000,  label='sdrob_abon_v1_release', marker='x')
    ax0.plot(sdrob_abon_v1_compress["execution time"]/1000,  label='sdrob_abon_v1_dev', marker='*')
    ax0.plot(sdrob_abon_v2_compress["execution time"]/1000,  label='sdrob_abon_v2_dev', marker='*')
    ax0.plot(sdrob_bin_v2_compress["execution time"]/1000,  label='sdrob_abon_v2_release', marker='+')

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
    ax1.plot(sdrob_decompress["execution time"]/1000,  label='sdrad_bincode_v1',  marker='x')
    ax1.plot(sdrob_abon_v1_decompress["execution time"]/1000,  label='sdrad_abomonation_v1', marker='*')
    ax1.plot(sdrob_abon_v2_decompress["execution time"]/1000,  label='sdrad_abomonation_v2', marker='*')
    ax1.plot(sdrob_bin_v2_decompress["execution time"]/1000,  label='sdrad_bincode_v2',marker='+')
    ax1.xaxis.get_label().set_fontsize(15)
    ax1.yaxis.get_label().set_fontsize(15)
    ax1.set_xticklabels(xticks) 
    ax1.legend(fontsize = 13)
    fig.savefig(folder_path + '/figure_1_decompress.png',  bbox_inches='tight')
    plt.show()
    plt.legend()




if __name__ == '__main__':
    main()