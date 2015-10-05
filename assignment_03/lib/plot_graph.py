import matplotlib.pyplot as ploty
import numpy as np


def open_file(log_name):
    with open(log_name, 'r') as f:
        read_data = f.readlines()
    f.close()
    return read_data


def parse_data(read_data):
    x1 = []
    y1 = []
    for line in read_data:
        if "ResultBF" in line:
            x1.append(line.split("Generation>")[1].split(":")[0])
            y1.append(line.split("new best>")[1].split("\n")[0])
    return x1, y1


def plot_data(algorithm_name, log_name):
    read_data = open_file(log_name)
    data_plot = parse_data(read_data)
    xv = np.array(data_plot[0])
    yv = np.array(data_plot[1])

    ploty.plot(xv, yv)
    ploty.savefig("{0}.png".format(algorithm_name))
    ploty.xlabel('Iterations')
    ploty.ylabel('Value')
    ploty.title(algorithm_name)
    ploty.grid(True)
    ploty.show()
