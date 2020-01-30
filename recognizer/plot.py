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
        fig = Figure(figsize=(12, 5), dpi=100)   # figsize - in inch
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
        self.peak_freq = 575

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
        self.samplingFrequency, self.signalData = wavfile.read(filePath)
        # select only one audio track from two channel soundtrack
        if len(self.signalData.shape) == 2:
            self.signalData = self.signalData[:, 0]
        # lenth of signal data
        N = len(self.signalData)
        # sampling interval in time (T - period)
        T = 1.0 / self.samplingFrequency
        # signal duration / signal freq [1/secs]
        seconds = N / float(self.samplingFrequency)
        # time vector (array) as scipy arange field / numpy.ndarray
        time = arange(0, seconds, T)
        # calculate fourier transform (complex dtype list)
        FFT = np.abs(fft(self.signalData))
        # you only need half of the fft list (real signal symmetry)
        self.FFT_side = FFT[range(N//2)]
        # Discrete Fourier Transform sample frequencies
        freqs = fftfreq(self.signalData.size, d=(time[1] - time[0]))
        # one side frequency range
        freqs_side = freqs[range(N//2)]
        # convert array to NumPy array
        self.fft_freqs_side = np.array(freqs_side)

        # Find the peak frequency: we can focus on only the positive frequencies
        pos_mask = np.where(freqs > 0)
        sample_freq = freqs[pos_mask]
        self.peak_freq = sample_freq[FFT[pos_mask].argmax()]

    def detectNote(self):
        # define dictionaty to store the data
        note = {"frequency": round(self.peak_freq, 2), "name": ""}
        # define temp var
        freq = self.peak_freq
        # matching freq
        if(freq >= 390 and freq < 403.5):
            note["name"] = "G"
        elif(freq >= 403.5 and freq < 427.5):
            note["name"] = "G#"
        elif(freq >= 427.5 and freq < 451.5):
            note["name"] = "A"
        elif(freq >= 451.5 and freq < 479.5):
            note["name"] = "A#"
        elif(freq >= 479.5 and freq < 508):
            note["name"] = "B"
        elif(freq >= 508 and freq < 538.5):
            note["name"] = "C"
        elif(freq >= 538.5 and freq < 570.5):
            note["name"] = "C#"
        elif(freq >= 570.5 and freq < 604.5):
            note["name"] = "D"
        elif(freq >= 604.5 and freq < 640.5):
            note["name"] = "D#"
        elif(freq >= 640.5 and freq < 678.5):
            note["name"] = "E"
        elif(freq >= 678.5 and freq < 719):
            note["name"] = "F"
        elif(freq >= 719 and freq < 762):
            note["name"] = "F#"
        elif(freq >= 762 and freq < 790):
            note["name"] = "A"
        else:
            note["name"] = "Unidentified"

        return note

    def plot(self):
        """Updating a WavePlot Figure instance and drawing plot."""
        # clear current plot
        self.axes.clear()
        self.configureAxes()
        # set range between searching values
        self.axes.set_xlim(left=self.peak_freq - 225,
                           right=self.peak_freq + 225)
        # Plot the FFT power
        self.axes.plot(self.fft_freqs_side, abs(self.FFT_side))
        # set peak frequency on the plot
        self.axes.axvline(self.peak_freq, linestyle=':', color='k')
        # Draw the plot on the canvas
        self.draw()

    def configureAxes(self):
        self.axes.grid(True)
        self.axes.set_title("Single-Sided Magnitude Spectrum", size=15)
        self.axes.set_ylabel("Magnitude")
        self.axes.set_xlabel("Frequency [Hz]")

    def cleanAxes(self):
        # clear current plot
        self.axes.clear()
        self.configureAxes()
        # set range between searching values
        self.axes.set_xlim(left=self.peak_freq - 225,
                           right=self.peak_freq + 225)
        self.axes.set_ylim([-2000000, 60000000])
        self.axes.plot(self.defaultFFTfregs, self.defaultFFT)
        self.draw()
