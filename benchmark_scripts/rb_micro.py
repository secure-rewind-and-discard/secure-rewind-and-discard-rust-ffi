# @author Merve Gulmez (merve.gulmez@ericsson.com)
# @version 0.1
# @date 2023-08-31
# @copyright (c) Ericsson AB 2023
# SPDX-License-Identifier: BSD 3-Clause 

import matplotlib.pyplot as plt
import pandas as pd
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    
    print("Folder path:", folder_path)

    if not os.path.isdir(folder_path):
        print("Error: The specified path is not a directory.")
        sys.exit(1)


    sandcrust = pd.read_csv( folder_path + "/sandcrust_output.txt", sep=',',  header=None)
    sdrad_ffi = pd.read_csv( folder_path + "/sdrad_output.txt", sep=',',  header=None)
    baseline = pd.read_csv( folder_path + "/empty_output.txt", sep=',',  header=None)
    sandcrust.columns = ['execution time', 'std']
    sdrad_ffi.columns = ['execution time', 'std']
    baseline.columns = ['execution time', 'std']
    print([sandcrust["std"][0], sdrad_ffi["std"][0]],sdrad_ffi["std"][0] )
    print(sdrad_ffi)
    # creating the dataset
    data = {'baseline':baseline["execution time"][0], 'sdrad_ffi':sdrad_ffi["execution time"][0],'pkru-safe':baseline["execution time"][0]*8.55, 'sandcrust':sandcrust["execution time"][0] }
    courses = list(data.keys())
    values = list(data.values())
    print(data)
    fig, ax = plt.subplots(figsize = (6, 3))
    
    colors = ["lightpink" if i != 'pkru-safe' else "gray" for i in data.keys()]

    bars = plt.barh(courses, values, height=0.5, color=colors)
    

    patterns = ('.', '*', '+', 'O', '.')
    for bar, pattern in zip(bars, patterns):
        bar.set_hatch(pattern)
    
    ax.set_xscale('log')
    plt.xlabel("Execution Time $ns$")
    ax.xaxis.get_label().set_fontsize(16)
    ax.yaxis.get_label().set_fontsize(15)
    ax.invert_yaxis()
    plt.yticks(fontsize=15)
    plt.yticks(fontsize=15)
    fig.savefig(folder_path + '/micro.png',  bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    main()