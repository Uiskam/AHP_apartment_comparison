
# Flat ranking tools using AHP method


This application is designed to create a ranking of apartments based on various parameters, primarily targeting students who are searching for a room to rent. It aims to assist individuals who are faced with the decision of choosing a rental room. The application takes into account several aspects of the apartment, including:

- Rental price
- Apartment size
- Room size
- Location:
    - Accessibility to the university
    - Proximity to the city center
    - Availability of shops nearby
- Number of roommates in the apartment
- Standard:
    - Neighborhood noise level
    - Interior decor
    - Sunlight exposure in the apartment
    - Neighborhood safety

Ranking is created using Analytic Hierarchy Process. Two parameter prioritization options are available: EVM (Eigen Value Method, default option) and GMM (Geometric Mean Method). For the EVM option, the consistency index is calculated as Saaty’s consistency index, while for the GMM method, the Geometric consistency index is computed.

### installation

Python 3.10 is required in order to run this application. In addition modules described in requirements.txt are needed. In order to install them run a command:

# Flat ranking tools using AHP method


This application is designed to create a ranking of apartments based on various parameters, primarily targeting students who are searching for a room to rent. It aims to assist individuals who are faced with the decision of choosing a rental room. The application takes into account several aspects of the apartment, including:

- Rental price
- Apartment size
- Room size
- Location:
    - Accessibility to the university
    - Proximity to the city center
    - Availability of shops nearby
- Number of roommates in the apartment
- Standard:
    - Neighborhood noise level
    - Interior decor
    - Sunlight exposure in the apartment
    - Neighborhood safety

Ranking is created using Analytic Hierarchy Process. Two parameter prioritization options are available: EVM (Eigen Value Method, default option) and GMM (Geometric Mean Method). For the EVM option, the consistency index is calculated as Saaty’s consistency index, while for the GMM method, the Geometric consistency index is computed.

### Requirements
Python 3.10 is required in order to run this application. In addition modules described in requirements.txt are needed. In order to install them run a command:

```
python -m pip install -r requirements.txt
```

### Usage
To run an app use command:
```
python main.py resources/config.csv resources/mock_data.csv
```
If you want to use your own data please give a proper path to your .csv file.

In file config.csv you can describe a number of experts in desission process and method (GMM or EVM).

config.csv:
```
number_of_experts
[number]
method
[gmm | evm]
```
