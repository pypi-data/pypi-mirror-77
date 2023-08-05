# Luminaire: A hands-off Anomaly Detection Library

<!-- Badges Start-->
[![PyPI version](https://badge.fury.io/py/luminaire.svg)](https://badge.fury.io/py/luminaire)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/luminaire.svg)](https://pypi.org/project/luminaire/)
[![License](http://img.shields.io/:license-Apache%202-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0.txt)
[![Luminaire CI](https://github.com/zillow/luminaire/workflows/Luminaire%20CI/badge.svg)](https://github.com/zillow/luminaire/actions)
[![Luminaire CD](https://github.com/zillow/luminaire/workflows/Luminaire%20CD/badge.svg)](https://github.com/zillow/luminaire/actions)
<!-- Badges End -->

![Luminaire Logo](luminaire_logo.png)

**Table of contents**

- [What is Luminaire](#what-is-luminaire)
- [Quick Start](#quick-start)
- [Anomaly Detection Flow](#anomaly-detection-flow)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [Development Team](#development-team)


## What is Luminaire

Luminaire is a python package that provides ML driven solutions for monitoring time series data. Luminaire provides 
several anomaly detection and forecasting capabilities that incorporate correlational and seasonal 
patterns in the data over time as well as uncontrollable variations.

Please see the [full Luminaire documentation](luminaire/docs/_build/html/Introduction.html) 
for detailed descriptions of the methods.

## Quick Start

Luminaire can be installed from PyPI.

```bash
pip install luminaire
```

## Time Series Outlier Detection Workflow
![Luminaire Flow](luminaire_flow.gif)

Luminaire outlier detection workflow can be divided into 3 major components.

### Data Preprocessing and Profiling Component

This component can be called for preparing a time series before training an anomaly detection model. This step applies
all necessary fixes (missing data imputation, identifying and removing recent outliers from training data, necessary
mathematical transformations, data truncation based on recent change points etc) and also generates profiling 
information (hostorical change points, trend changes etc) for the training data. 

The profiling information for time series data generates important information for an offline time series data and
can be used to monitor irregular longer term swings or data drifts.

### Modeling Component

This components performs time series model training based on the user specified configuration OR optimized configuration 
(see Luminaire hyperparameter optimization). Luminaire model training is integrated with different structural time series
models as well as filtering based models. See [Luminaire outlier detection](luminaire/docs/_build/html/basic_usage_tutorial/outlier_batch.html)
for more information.
 
Luminaire modeling step can be called after the data preprocessing and profiling step to perform necessary data preparation before training.
 
### Configuration Optimization Component
 
Luminaire is integrated with configuration optimization capability for the hands-off anomaly detection approach where
the user needs to provide almost no configuration for any type of time series data. This step can be combined with
the preprocessing and modeling for any auto configured anomaly detection use case. See [fully automatic outlier detection](luminaire/docs/_build/html/basic_usage_tutorial/optimization.html#fully-automatic-outlier-detection)
for a detailed walkthrough. 

## Anomaly Detection for High Frequency Time Series

Luminaire can monitor  a set of data points over windows instead of tracking individual. This approach becomes relevant
for streaming use cases where individual fluctuations is not of a concern but the data is monitored for more sustained 
fluctuations. See [anomaly detection for streaming data](/luminaire/docs/_build/html/basic_usage_tutorial/streaming.html)
for detailed information.

## Contributing

Want to help improve Luminaire? Check out our [contributing documentation](CONTRIBUTING.rst).

## Acknowledgements

This project has leveraged methods described in the following scientific publications:

1. Soule, Augustin, Kavé Salamatian, and Nina Taft. "Combining filtering and statistical methods for anomaly detection." Proceedings of the 5th ACM SIGCOMM conference on Internet Measurement. 2005.


## Development Team

Luminaire is developped and maintained by [Sayan Chakraborty](https://github.com/sayanchk), [Smit Shah](https://github.com/shahsmit14), 
[Kiumars Soltani](https://github.com/kiumarss), [Luyao Yang]( https://github.com/snazzyfox), [Anna Swigart](https://github.com/annaswigart), 
[Kyle Buckingham](https://github.com/kylebuckingham) and many other contributors from the Zillow Group A.I. team.
