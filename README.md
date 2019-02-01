# Miscellaneous Python scripts

This repository contains miscellaneous scripts and snippets that might be useful.

## Dynamic Rating Scale

```
\dynamic-rating-scale\dynamic-rating-scale.py
```

My own rating scale for full flexibility. 
Guidelines from Matejka 2016: No ticks (use bands), 2 labels and dynamic text
feedback.

#### Prerequisites

The task was developed to run on Python 2.7 using the following packages. It can probably be easily adapted to Python 3. 

* [Python 2.7](https://www.python.org/downloads/release/python-2715/)
* [Psychopy 1.90.1](https://www.github.com/psychopy/psychopy/releases/tag/1.90.1) - free package for running neuroscience, psychology and psychophysics experiments

### Sound staircase

```
\dynamic-rating-scale\sound-staircase.py
```

Example of a 1-up-1-down staircase procedure to define an auditory perceptual 
threshold. 

After a detection, the volume is decreased by multiplying its value 
by 0.812, which corresponds to a 3dB reduction in my setup.. If the tone is 
not detected, the volume is divided by 0.812 in order to increase its value.

A **running average of performance** is also calculated (ratio of correct/incorrect
detections). If performance falls below a threshold of 60%, the staircase steps
become smaller (the 0.812 value is increased by 0.05), up to 3 changes of step
size, in order to have a better approximation of the auditory threshold.
The data is then saved in a `.csv` file.

#### Prerequisites

The task was developed to run on Python 2.7 using the following packages. It can probably be easily adapted to Python 3. 

* [Python 2.7](https://www.python.org/downloads/release/python-2715/)
* [Psychopy 1.90.1](https://www.github.com/psychopy/psychopy/releases/tag/1.90.1) - free package for running neuroscience, psychology and psychophysics experiments
* [PYO Ajax Sound Studio](https://www.ajaxsoundstudio.com/software/pyo/) - free package for digital signal processing of sound

## Installing

On the Command Prompt or Terminal

```
>>> cd \folderwherescriptislocated\
>>> python nameofscript.py
```

## Authors

* **Santiago Munoz Moldes** - [Github](https://github.com/santihago)

## License

Released under the MIT license – see the [LICENSE.md](LICENSE.md) file for details

## Disclaimer

All shared material was developed for my own research purposes, and I cannot guarantee that it is free of errors or bugs. I am therefore not responsible for any error, bug, or malfunction you may encounter in your own use. If you notice something wrong, please let me know so I can correct it.

## Acknowledgments

* ...
