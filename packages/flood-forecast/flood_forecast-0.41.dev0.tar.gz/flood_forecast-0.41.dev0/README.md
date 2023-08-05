# Deep learning for time series forecasting
This repository is an open-source DL for time series library. Currently [Task-TS from CoronaWhy](https://github.com/CoronaWhy/task-ts/wiki) maintains this repo. Pull requests are welcome. Historically, this repository provided open source benchmark and codes for flash flood and river flow forecasting. Specifically, it contained baseline methods for forecasting stream flows around the United States. 

| branch  | status                                                                                                                                                                                                            |
| ---     | ---                                                                                                                                                                                                               |
| master  | [![CircleCI](https://circleci.com/gh/AIStream-Peelout/flow-forecast.svg?style=svg&circle-token=f7be0a4863710165969ba0903fa471f08a347df1)](https://circleci.com/gh/AIStream-Peelout/flow-forecast)                 |
| Build PY| ![Upload Python Package](https://github.com/AIStream-Peelout/flow-forecast/workflows/Upload%20Python%20Package/badge.svg)|

Using the library
1. Run `pip install flood-forecast`
2. See documentation in wiki .

For instructions on contributing please se Wiki/Issue Board.

## Task 1 Stream Flow Forecasting 
This task focuses on forecasting a stream's future flow/height (in either cfs or feet respectively) given factors such as current flow, temperature, and precipitation. In the future we plan on adding more variables that help with the stream flow prediction such as snow pack data and the surrounding soil moisture index. 

## Task 2 Flood severity forecasting
Task two focuses on predicting the severity of the flood based on the flood forecast, population information, and topography. Flood severity is defined based on several factors including the number of injuires, property damage, and crop damage.

If you use either the data or code from this repository please cite as
```
@inproceedings{GodfriedFlow2019,
Author = {Isaac Godfried},
Title = {Flow: A large scale dataset for stream flow and flood damage forecasting},
Booktitle  = {Arxiv Preprint},
Year = {2019}
}
```
 
