import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from scipy import arange
from scipy.io import wavfile
from scipy.fftpack import fft, fftfreq
# from matplotlib import pyplot as plt


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
        # create the Figure
        fig = Figure(figsize=(5, 5), dpi=100)   # figsize - in inch
        FigureCanvasQTAgg.__init__(self, fig)

        # frequency sampling [hz]
        Fs = 44100
        # period time T [sec]
        T = 1.0 / Fs
        # time axes [time array]
        t = arange(0, 1, T)
        # value of the time function
        x = [0] * t
        # generate frequency axis
        n = np.size(t)
        fr = (Fs/2) * np.linspace(0, 1, n/2)
        # compute FFT
        X = fft(x)
        X_m = abs(X[0: np.size(fr)])

        self.defaultFFTfregs = fr
        self.defaultFFT = X_m

        # create the axes
        self.axes = fig.add_subplot(111)
        # setup axes
        self.configureAxes()
        # set range between searching values
        self.axes.set_xlim(left=350, right=800)
        self.axes.set_ylim([-2000000, 60000000])
        # plot
        self.axes.plot(self.defaultFFTfregs, self.defaultFFT)
        self.draw()
        self.setParent(parent)

    def open(self, filePath):
        # open a WAV file
        samplingFrequency, signalData = wavfile.read(filePath)

        # select only one audio track from two channel soundtrack
        if len(signalData.shape) == 2:
            signalData = signalData[:, 0]

        # lenth of signal data
        N = len(signalData)

        # sampling interval in time (T - period)
        T = 1.0 / samplingFrequency

        # signal duration / signal freq [1/secs]
        seconds = N / float(samplingFrequency)

        # time vector (array) as scipy arange field / numpy.ndarray
        time = arange(0, seconds, T)

        # calculate fourier transform (complex numbers list)
        FFT = abs(fft(signalData))

        # you only need half of the fft list (real signal symmetry)
        self.FFT_side = FFT[range(N//2)]

        # Discrete Fourier Transform sample frequencies
        freqs = fftfreq(signalData.size, time[1] - time[0])

        # one side frequency range
        freqs_side = freqs[range(N//2)]

        # convert array to NumPy array
        self.fft_freqs_side = np.array(freqs_side)

    def plot(self):
        """Updating a WavePlot Figure instance and drawing plot."""
        # clear current plot
        self.axes.clear()
        self.configureAxes()
        # set range between searching values
        self.axes.set_xlim(left=350, right=800)
        self.axes.plot(self.fft_freqs_side, abs(self.FFT_side))
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
        # set range between searching values
        self.axes.set_xlim(left=350, right=800)
        self.axes.set_ylim([-2000000, 60000000])
        self.axes.plot(self.defaultFFTfregs, self.defaultFFT)
        self.draw()
