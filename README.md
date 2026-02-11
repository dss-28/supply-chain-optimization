

# 📦 AI-Driven Supply Chain Optimization (End-to-End)


A **deterministic, LP-ready logistics and inventory management system** that integrates **demand forecasting, shipment planning, vehicle routing, and dynamic what-if scenario analysis**. This project demonstrates **cross-domain systems thinking**—modeling demand, managing inventory, and optimizing shipments and delivery routes under real-world constraints—implemented in a fully programmable, end-to-end pipeline.

---

It is designed not as a random input → output model but as a **decision-making system** for real-world logistics.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Modules](#modules)

   * [1️⃣ Demand Simulation](#1-demand-simulation)
   * [2️⃣ Demand Forecasting](#2-demand-forecasting)
   * [3️⃣ Inventory & LP Shipment Planning](#3-inventory--lp-shipment-planning)
   * [4️⃣ Vehicle Routing Optimization](#4-vehicle-routing-optimization)
   * [5️⃣ What-If Scenario Analysis](#5-what-if-scenario-analysis)
5. [Technologies Used](#technologies-used)
6. [Learning Outcomes](#learning-outcomes)
7. [How to Run](#how-to-run)
8. [Future Enhancements](#future-enhancements)

---

## Overview

This system simulates **warehouse and city logistics** for multiple cities and warehouses over a 30-day horizon. It solves **optimization problems** for shipment planning and vehicle routing, while incorporating **demand uncertainty** via forecasting and enabling **what-if scenario planning**.

The focus is **systems-level thinking** rather than just analytics. It integrates:

* Deterministic demand simulation
* Moving-average-based demand forecasting
* Linear programming for shipment planning
* Multi-vehicle routing optimization
* Scenario-based “what-if” analysis

---

## Features

* **Demand Simulation:** Seasonal demand patterns per city
* **Forecasting:** Moving average with uncertainty bands (P10, P50, P90)
* **Inventory Management:** Warehouse capacity, distance-based cost, CO2 emissions
* **LP-based Shipment Planning:** Optimize shipments to meet demand while minimizing cost, CO2, and stockouts
* **Vehicle Routing:** Optimize vehicle routes for multiple warehouses, respecting vehicle capacities
* **What-If Analysis:** Test scenarios like demand surge or limited warehouse inventory
* **Dynamic & Scalable:** Multipliers and constraints are parameterized to handle new scenarios easily
* **End-to-End System:** From raw demand → forecast → shipment plan → vehicle routing → scenario testing

---

## Project Structure

```
project/
│
├── data/
│   ├── demand_data.csv
│   ├── demand_forecast.csv
│   ├── inventory_data.csv
│   ├── shipment_plan_lp.csv
│   ├── vehicle_routes_optimized.csv
│   └── shipment_plan_whatif.csv
│
├── notebooks/
│   └── exploratory.ipynb
│
├── scripts/
│   ├── 01_demand_simulation.py
│   ├── 02_demand_forecasting.py
│   ├── 03_shipment_plan_lp.py
│   ├── 04_vehicle_routing.py
│   └── 05_shipment_plan_whatif.py
│
├── README.md
└── requirements.txt
```

---

## Modules

### 1️⃣ Demand Simulation

Simulates **daily deterministic demand** per city using **base demand + seasonal sine function**. Generates:

* `demand_data.csv` with columns: `day`, `city`, `demand`
* Initial **warehouse inventory table** with LP parameters (distance, cost per unit, CO2 per unit)

**Key Learnings:**

* Simulation of demand patterns
* Distance calculation for cost/CO2
* Preparing LP-ready data

---

### 2️⃣ Demand Forecasting

Performs **moving-average-based forecasting** with uncertainty bands:

* `demand_p50` → mean forecast
* `demand_p10` → lower bound (10th percentile)
* `demand_p90` → upper bound (90th percentile)

**Key Learnings:**

* Time series smoothing
* Handling uncertainty
* Dynamic, city-specific forecast

---

### 3️⃣ Inventory & LP Shipment Planning

Formulates **Linear Programming (LP)** problem to:

* Decide **shipment quantities** per warehouse → city → day
* **Minimize total cost** = transportation cost + CO2 + stockout penalty
* Respect **warehouse inventory constraints**
* Save results to `shipment_plan_lp.csv`

**Key Learnings:**

* LP problem formulation and solution using PuLP
* Balancing multiple objectives (cost + CO2 + stockout)
* Handling multi-day, multi-warehouse constraints

---

### 4️⃣ Vehicle Routing Optimization

Optimizes **vehicle-wise shipments** per warehouse:

* Multiple vehicles per warehouse
* Vehicle capacity constraints
* Objective: **Minimize CO2 emissions**
* Output: `vehicle_routes_optimized.csv`

**Key Learnings:**

* Multi-vehicle routing
* Operational constraints in optimization
* Linking shipment plan → vehicles

---

### 5️⃣ What-If Scenario Analysis

Allows dynamic **demand and warehouse inventory adjustments**:

* Increase/decrease demand by city
* Reduce available inventory per warehouse
* Re-run LP to see new shipment and unmet demand results
* Output: `shipment_plan_whatif.csv`

**Key Learnings:**

* Scenario testing for robust planning
* Dynamic parameterization in LP
* Strategic planning under uncertainty

---

## Technologies Used

* Python 3.10+
* Libraries: `pandas`, `numpy`, `math`, `os`, `PuLP`
* Linear Programming solver: CBC (built-in with PuLP)
* CSV for intermediate data storage

---

## Learning Outcomes

* **End-to-end system design** from demand → forecast → planning → routing → scenario
* **Cross-domain thinking** (operations + analytics + optimization + sustainability)
* **Dynamic, LP-ready modeling** for decision-making systems
* **Vehicle routing and capacity management**
* **Scenario-based planning and robust system design**
* **Real-world problem-solving mindset** beyond simple ML

---

## How to Run

1. Clone repo:

```bash
git clone <repo_url>
cd project
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run scripts in order:

```bash
python scripts/01_demand_simulation.py
python scripts/02_demand_forecasting.py
python scripts/03_shipment_plan_lp.py
python scripts/04_vehicle_routing.py
python scripts/05_shipment_plan_whatif.py
```

4. Check results in `data/` folder.

---

## Future Enhancements

* Include **real stochastic demand** using probabilistic models
* Add **ML-based forecasting models** (ARIMA, LSTM, Prophet)
* Integrate **real routing optimization** (VRP, TSP solvers)
* Add **real-time dashboard** for shipment & CO2 monitoring
* Incorporate **cost optimization with multi-modal transport**

---

✅ This project is **not just analytics**, not pure MLOps, but a **system-level, end-to-end logistics and optimization solution**, demonstrating skills in **forecasting, optimization, vehicle routing, scenario planning, and dynamic system modeling**.

---

Do you want me to do that?
