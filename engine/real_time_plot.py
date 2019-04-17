import os
import socket
from collections import Counter
import sys
import matplotlib.animation as animation
import matplotlib.markers as mmarkers
import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib


def add_values_on_bar_plot(plot, spacing=3):

    for rect in plot.patches:

        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        label = f"{int(y_value)}"


        plot.annotate(
            label,
            (x_value, y_value),
            xytext=(0, spacing),
            textcoords="offset points",
            ha='center',
            va="bottom",
            weight="bold"
        )


def fix_over_lapping_text_in_pie_chart(text):
    sigFigures = 2
    positions = [(round(item.get_position()[1], sigFigures), item)
                 for item in text]

    overLapping = Counter((item[0] for item in positions))
    overLapping = [key for key, value in overLapping.items() if value >= 2]
    for key in overLapping:
        textObjects = [text for position, text in positions if position == key]
        if textObjects:
            scale = 0.1
            spacings = np.linspace(0, scale * len(textObjects),
                                   len(textObjects))

            for shift, textObject in zip(spacings, textObjects):
                textObject.set_y(key + shift)


def show_pie_chart(plot, plot_title, data, event_order, colors):

    _, text, autotexts = plot.pie(
        data,
        colors=colors,
        labels=event_order[:len(data)],
        autopct='%1.2f%%',
        shadow=True,
        wedgeprops={
            'linewidth': 3,
            'edgecolor': "white"
        })

    plt.setp(text, weight="bold")
    plt.setp(autotexts, weight="bold")
    plot.set_aspect('equal')
    fix_over_lapping_text_in_pie_chart(text)


def show_scatter_plot(plot1, x_data, y_data, markers, number_of_events, event_order, markers_color, rotation_angle=0):

    marker_data = [markers[value - 1] for value in y_data]
    markers_color_data = [markers_color[value - 1] for value in y_data]

    plot1.grid()
    plot1.set_xticks(range(1, 90, 5))
    plot1.set_xticklabels(
        range(1, 90, 5), rotation=rotation_angle, fontweight="bold")
    plot1.set_yticks(range(1, 1 + number_of_events))
    plot1.set_yticklabels(event_order, fontweight="bold")
    plot1.set_xlabel('Time(secs)', fontweight="bold")

    scatters = plot1.scatter(x_data, y_data, c=markers_color_data)

    paths = []
    for marker in marker_data:
        marker_obj = mmarkers.MarkerStyle(marker)
        path = marker_obj.get_path().transformed(marker_obj.get_transform())
        paths.append(path)

    scatters.set_paths(paths)


def show_bar_plot(plot2, x_data, y_data, number_of_events, event_order, markers_color, data_points, rotation_angle=0):

    plot2.yaxis.grid()
    plot2.set_yticks(range(0, 5+data_points, 5))
    plot2.set_yticklabels([])
    plot2.set_xticks(range(1, 1 + number_of_events))
    plot2.set_xticklabels(
        event_order, rotation=rotation_angle, fontweight="bold")
    x_data = list(x_data)
    y_data = list(y_data)
    bars = plot2.bar(x_data, y_data)

    for bar_index, bar in enumerate(bars):
        bar.set_color(markers_color[bar_index])
    add_values_on_bar_plot(plot2)

def get_proper_data(data):
    return None


def animate(time_value, file_name, socket_object, ax, ax1, ax2, event_order, markers_color, markers, number_of_events, secs_experiment_ran):

    file = open(file_name, 'a+')
    if time_value == secs_experiment_ran + 1:
        socket_object.close()
        plt.close()

    _data = socket_object.recv(1024).decode("utf-8")

    if _data != '':
        file.write(f'{_data}\n')

    # # test_data = get_proper_data(_data)

    # model = joblib.load('model.pkl')

    # predicted_value = model.predict(test_data)

    file.seek(0)
    data = [tuple(map(int, line.strip().split())) for line in file.readlines()]
    file.close()

    zipped_data = list(zip(*data[:time_value+1]))

    x_data = zipped_data[0]
    y_data = zipped_data[1]

    bar_data = Counter(y_data)

    real_bar_data = dict()
    for number in range(number_of_events):
        real_bar_data[number+1] = 0
    
    for key, value in bar_data.items():
        real_bar_data[key] = value

    x_bar_data = real_bar_data.keys()
    y_bar_data = real_bar_data.values()

    ax1.clear()
    ax2.clear()
    ax.clear()

    ax.set_yticks([])
    ax.set_xticks([])

    [s.set_visible(False) for s in ax.spines.values()]

    time_text = ax.text(0, 1, '', fontweight="bold")
    time_text.set_text(f"Seconds Passed = {time_value + 1}\n\n")

    show_scatter_plot(ax1, x_data, y_data, markers,
                    number_of_events, event_order, markers_color)
    show_bar_plot(ax2, x_bar_data, y_bar_data,
                number_of_events, event_order, markers_color, time_value)

def generate_animation(file_name, socket_object, event_order, markers_color, markers, number_of_events, secs_experiment_ran):

    fig = plt.figure()

    ax = plt.axes()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    animating = animation.FuncAnimation(fig, animate, interval=500, fargs=(
        file_name, socket_object, ax, ax1, ax2, event_order, markers_color, markers, number_of_events, secs_experiment_ran))

    plt.show()

def generate_data_for_final_plot(data):

    zipped_data = list(zip(*data))

    x_scatter_data = zipped_data[0]
    y_scatter_data = zipped_data[1]

    bar_data = Counter(y_scatter_data)
    x_bar_data = list(bar_data.keys())
    y_bar_data = list(bar_data.values())

    pie_data = np.around((np.array(y_bar_data) / x_scatter_data[-1]) * 100, 2)

    return x_scatter_data, y_scatter_data, x_bar_data, y_bar_data, pie_data


def generate_final_plot(file_name, event_order, markers_color, markers, number_of_events, secs_experiment_ran):

    file = open(file_name, 'r')
    data = [tuple(map(int, line.strip().split())) for line in file.readlines()]

    result_figure = plt.figure()

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    ax1 = result_figure.add_subplot(1, 3, 1)
    ax2 = result_figure.add_subplot(1, 3, 2)
    ax3 = result_figure.add_subplot(1, 3, 3)

    x_scatter_data, y_scatter_data, x_bar_data, y_bar_data, pie_data = generate_data_for_final_plot(
        data)

    show_scatter_plot(ax1, x_scatter_data, y_scatter_data,
                      markers, number_of_events, event_order, markers_color, 90)

    show_bar_plot(ax2, x_bar_data, y_bar_data, number_of_events,
                  event_order, markers_color, 315)

    show_pie_chart(ax3, 'Pie Chart', pie_data, event_order, markers_color)

    plt.show()

def main(time_ran, event_names):

    file_name = 'data.txt'

    markers = ['o', '^', 'X', '*', 'D']
    event_order = event_names
    markers_color = ['green', 'yellow', 'orange', 'red', 'brown', 'black']
    number_of_events = len(event_order)
    secs_experiment_ran = time_ran


    if os.path.exists(file_name):
        os.remove(file_name)
    port = 12345                

    socket_object = socket.socket()          
    socket_object.connect(('127.0.0.1', port))

    try:
        generate_animation(file_name, socket_object, event_order, markers_color,
                        markers, number_of_events, secs_experiment_ran)

        generate_final_plot(file_name, event_order, markers_color,
                            markers, number_of_events, secs_experiment_ran)
    except Exception as e:
        print(e)
        pass



if __name__ == "__main__":
    time_ran = 90
    event_names = list('abcde')
    # time_ran = int(sys.argv[1])
    # event_names = list(sys.argv[2])
    main(time_ran, event_names)