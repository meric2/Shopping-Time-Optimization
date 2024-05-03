# Shopping Time Optimization
This project aims to solve a time optimization problem for a specific market layout. The user will provide a shopping list within the product list and the output will be the optimal (shortest) time to finish shopping.  

## Project Overview

The main components of this project include:  

- Solving the problem with Genetic Algorithm (GA).  
- Converting the matter into Constraint Satisfaction Problem (CSP) and using Gurobi solver.  
  
Input for both algorithms are the market layout and the user input which is the shopping list.  
Output is the optimal path and time for the given list.  
An example market layout is integrated into code for GA, can be found in `MarketData.xlsx` for Gurobi, you can modify starting from there.  
 

## Tech Stack

**Language**: Python  
**Technologies**: Gurobipy  

## Getting Started  

### Prerequisites  
- Python 3  

### Installation  

- Clone the repository
  ```bash
  git clone https://github.com/meric2/Shopping-Time-Optimization.git  
  ```  

- Install dependencies
  ```bash
  pip install -r requirements.txt
  ```  

## Usage

- Run `GeneticAlgorithm.py` for GA solution.  
- Run `CSPsolver.py` for Gurobi (CSP) solution.  
