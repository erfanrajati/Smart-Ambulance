import matplotlib.pyplot as plt

class LivePlot:
    def __init__(self, title="Live Plot", ylabel="Value"):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], marker="o")

        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)

        self.values = []

    def update(self, value):
        """Add a new value and update the plot."""
        self.values.append(value)

        self.line.set_xdata(range(len(self.values)))
        self.line.set_ydata(self.values)

        self.ax.relim()
        self.ax.autoscale_view()

        plt.pause(0.001)

    def finish(self):
        """Keep the final plot open after the algorithm ends."""
        plt.ioff()
        plt.show()
