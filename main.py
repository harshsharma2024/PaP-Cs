from utils import main, plot_graph



if __name__ == "__main__":
    group_sizes = list(range(5, 100, 8))
    group_sizes += list(range(100, 500, 20))
    group_sizes += list(range(500, 1000, 50))
    group_sizes += list(range(1000, 2050, 100))

    # group_sizes = [5]

    print("Group sizes: ", group_sizes)

    time_ms = []
    for grp_size in group_sizes:
        print("Group size: ", grp_size)
        timediff = main(grp_size)
        time_ms.append(timediff)
        print("Time taken for group size ", grp_size, " is ", timediff)
    print(time_ms)

    plot_graph(group_sizes, time_ms)  # Plot the graph
