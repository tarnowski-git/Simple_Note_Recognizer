import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class SpectralPlot(FigureCanvasQTAgg):
    """Compute and draw a Power Spectral Denisity of wave.

    Parameters
    ----------
    `parent` : master widget
        Represents a widget to act as the parent of the current object
    `xval` : 1-D array or sequence
        The number of data points in timeline.
    `yval` : 1-D array or sequence
        Array containing wave samples.
    """

    def __init__(self, parent=None, xval=np.zeros(1000), yval=[0] * 1000):
        # init variables
        self.FFTfregs = xval
        self.FFT = yval

        # create the Figure
        fig = Figure(figsize=(5, 5), dpi=100)   # figsize - in inch
        FigureCanvasQTAgg.__init__(self, fig)

        # create the axes
        self.axes = fig.add_subplot(111)
        # setup axes
        self.configureAxes()
        self.axes.set_xlim(left=0)
        self.axes.plot(self.FFTfregs, self.FFT)
        self.draw()
        self.setParent(parent)

    def plot(self, FFTfregs=None, FFT=None):
        """Updating a WavePlot Figure instance and drawing plot."""
        self.FFTfregs = FFTfregs
        self.FFT = FFT
        # clear current plot
        self.axes.clear()
        self.configureAxes()
        # set range between searching values
        self.axes.set_xlim(left=350, right=800)
        self.axes.plot(self.FFTfregs, abs(self.FFT))
        self.draw()

    def configureAxes(self):
        self.axes.grid(True)
        self.axes.set_title("Single-Sided Magnitude Spectrum", size=15)
        self.axes.set_ylabel("Magnitude")
        self.axes.set_xlabel("Frequency(Hz)")

    def cleanAxes(self):
        # clear current plot
        self.axes.clear()
        self.configureAxes()
        self.draw()
