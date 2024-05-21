## Project Environment Setup

This document provides instructions for setting up the environment required to run the project. The project interface is a Jupyter Notebook, and the following packages are needed:

- `transformers`
- `requests`
- `string`
- `nltk`
- `pandas`
- `matplotlib`
- `seaborn`
- `numpy`
- `scipy`
- `IPython`
- `scikit-learn`
- `pygwalker`
- `folium`
- `geopy`
- `certifi`
- `ssl`
- `torch`

### Prerequisites

Ensure that you have Python and Jupyter Notebook installed on your system. If not, you can install them using Anaconda or pip.

#### Using Anaconda

1. [Download and install Anaconda](https://www.anaconda.com/products/individual) if you don't have it installed already.
2. Create a new conda environment:

    ```bash
    conda create -n project_env python=3.9
    conda activate project_env
    ```

#### Using pip

1. Ensure you have Python installed. If not, [download and install Python](https://www.python.org/downloads/).
2. Install Jupyter Notebook:

    ```bash
    pip install notebook
    ```

### Installing Required Packages

You can install the required packages using `pip`. Open a terminal and run the following commands:

```bash
pip install transformers requests nltk pandas matplotlib seaborn numpy scipy IPython scikit-learn pygwalker folium geopy certifi ssl torch
```

Alternatively, you can run the following commands:

```bash
pip install -r requirements.txt
```

### Running the Jupyter Notebook

To start the Jupyter Notebook, activate your environment and run:

jupyter notebook

Notice that `presentation.ipynb` is the interface and other python files are helper functions for encapsulation.


### Submission Details
 Team 50 members:
 - `Congcong Zhao (Student ID: 1107156)`
 - `Yesheng Yao (Student ID: 1108951)`
 -	`Chuqiao Wu (Student ID: 1386417)`
 -	`Ruilong Wang (Student ID: 1074694)`
 -	`Qichi Liang (Student ID: 1392005)`

### Project structure
- `Backend/ -- Source code and files for backend (Fission)`
- `Frontend/ -- Source code for client and testing files for frontend (Jupyter NoteBook)`
- `Doc/ -- Documentation about backend function descriptions and routes descriptions and report`
- `Test/ -- Testing codes for backend`
- `Database/ -- Json files for ElasticSearch mapping and settings`


### System architecture
The system architecture designed for this project is deployed on the University of Melbourne Research Cloud. Use Fission as backend. Use k8s for cluster management. For further information, please refer to the project report attached to this submission.
