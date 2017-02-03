from itertools import cycle
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib import rc
import numpy as np

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

import re
QC_LOG_FILE_NAME = 'logs/kproblog_qc_short.log'

prefix_it = cycle([
    'CONFIGURATION_SET',
    'Starting EXTRACTION',
    'EXTRACTION ellapsed time',
    'FINAL LEARNING train acc:'
])

def config2latex(config):
    bow_list = []
    sp_list = []
    for t, params in config:
        if t == 'bow':
            bow_list.append(params[0][0])
        elif t == 'sp':
            vlabel = params[1][0]
            if vlabel == '_':
                vlabel = '\_'
            elabel = params[0]
            sp_list.append(vlabel)
        else:
            raise ValueError
    bow_list.sort()
    sp_list.sort()
    bow_str = "{}".format(''.join(bow_list)) if bow_list else '\\emptyset'
    sp_str = "{}".format(''.join(sp_list)) if sp_list else '\\emptyset'
    return '${} - {}$'.format(bow_str, sp_str), bow_list, sp_list
    # return '$\\textsc{{u}}:{}, \\textsc{{sp}}:{}$'.format(bow_str, sp_str)

def parse_qc_log():
    result_list = []
    current_result = None
    seconds_list = []
    with open(QC_LOG_FILE_NAME) as qc_log_file:
        for line, prefix in zip(qc_log_file, prefix_it):
            assert line.startswith(prefix)
            line = line.strip()
            # print(line)
            if line.startswith('CONFIGURATION_SET'):
                _, *args = line.split(' ')
                config = eval(" ".join(args))
                current_result = [config]
                # print('config', config)
            elif line.startswith('Starting EXTRACTION'):
                pass
            elif line.startswith('EXTRACTION ellapsed time'):
                seconds_str, = re.findall("([0-9]*\.[0-9]*)", line)
                seconds = float(seconds_str)
                # print('seconds', seconds)
                current_result.append(seconds)
                seconds_list.append(seconds)
            elif line.startswith('FINAL LEARNING train acc:'):
                acc_str_list = re.findall("([0-9]*\.[0-9]*\%)", line)
                train_acc, test_acc = [float(acc_str[:-1]) for acc_str in acc_str_list]
                # print(test_acc)
                current_result.append(test_acc)
                result_list.append(current_result)
                current_result = None
            else:
                raise ValueError
    print('time per extraction {}+/-{} min: {} max: {}'.format(np.mean(seconds_list), np.std(seconds_list), min(seconds_list), max(seconds_list)))
    return result_list

def main():
    TIMES=8
    TOP_K = 16
    result_list = parse_qc_log()
    result_list = sorted(result_list, key=lambda x:x[2], reverse=True)
    result_list = result_list[:TOP_K]

    table_lines = []
    # table_lines.append(r'\begin{tabular}{ c | c | r }')
    # table_lines.append(' & '.join(['unigrams', 'shortest paths', 'accuracy']) + r'\\')
    # table_lines.append(r'\hline')
    x_list = []
    y_list = []
    tick_label=[]
    
    for idx, (x, seconds, y) in enumerate(result_list):
        config_str, unigram_list, sp_list = config2latex(x) 
        # if unigram_list and sp_list:
        x_list.append(x)
        y_list.append(y)
        tick_label.append(config_str)
        if idx % TIMES == 0:
            if table_lines:
                table_lines.append(r'\end{tabular}')
            table_lines.append(r'\begin{tabular}{ c | c | c }')
            table_lines.append(' & '.join(['unigram', 'shortest path', 'test']) + r'\\')
            table_lines.append(' & '.join(['features', 'features', 'accuracy']) + r'\\')
            table_lines.append(r'\hline')
            
        
        aa, bb = config_str.split('-')
        table_lines.append(' & '.join([aa + '$', '$' + bb, '$' + str(y)+r'\%$']) + r'\\')
    table_lines.append(r'\end{tabular}')

    plt.rcdefaults()
    fig, ax = plt.subplots()
    ax.barh(np.arange(len(y_list)), y_list, align='center', color='white', ecolor='black')
    plt.yticks(np.arange(len(y_list)), tick_label, horizontalalignment='left', x=0.2)
    fig.subplots_adjust(left=0.2)
    # plt.show()
    print("\n".join(table_lines))

if __name__ == '__main__':
    main()
#
# plt.show()
# CONFIGURATION_SET [('sp', (False, 'word'))]
# Starting EXTRACTION.
# EXTRACTION ellapsed time 25.521 seconds
# FINAL LEARNING train acc: 100.0% acc test: 80.2%

    
    