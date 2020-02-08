# Simple Note Recognizer

Desktop GUI applications to show the computation of the Discrete Fourier Transform of a music note singal from WAV file with Python 3 using PyQT5 graphic modul. The application plot the intensity of signal frequency and recognize the music note.

The Fourier transform of a musical instrument recording can be used to determine which music note is being performed and whether the instrument is in tuned.

What note the instrument plays can be determined by the fundamental frequency of the signal and comparing it with the table describing the fundamental frequencies associated with each note:

| Note | Frequency (Hz) |
| :--: | :------------: |
|  G   |     390.0      |
|  G#  |     415.3      |
|  A   |     440.0      |
|  A#  |     466.2      |
|  B   |     493.9      |
|  C   |     523.3      |
|  C#  |     554.4      |
|  D   |     587.3      |
|  D#  |     622.3      |
|  E   |     659.3      |
|  F   |     698.5      |
|  F#  |     740.0      |
|  G   |     784.0      |

## Demo

![program-demo](https://user-images.githubusercontent.com/34337622/73490016-f1989a00-43ab-11ea-8b42-8ce0bb2bd129.gif)

## Technologies

-   Python 3.7
-   PyQT5 graphic module
-   NumPy module
-   SciPy module
-   Matplotlib module

## Prerequisites

-   [Python](https://www.python.org/downloads/)
-   [pip](https://pip.pypa.io/en/stable/installing/)
-   [pipenv](https://pipenv.readthedocs.io/en/latest/install/#make-sure-you-ve-got-python-pip)

## Installation

-   [Clone](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) this repo to your local machine using:

```
$ git clone https://github.com/tarnowski-git/Simple_Note_Recognizer.git
```

-   Setup your [local environment](https://thoughtbot.com/blog/how-to-manage-your-python-projects-with-pipenv):

```
# Spawn a shell with the virtualenv activated
$ pipenv shell

# Install dependencies
$ pipenv install

# Run script into local environment
$ pipenv run python note_recognizer.py
```

-   Compile with Pyinstaller to exectutable file:

```
# Windows
pyinstaller --hidden-import pkg_resources.py2_warn --onefile --windowed note_recognizer.py
```

## [License](https://github.com/tarnowski-git/Simple_Note_Recognizer/blob/master/LICENSE)

MIT © [Konrad Tarnowski](https://github.com/tarnowski-git)
