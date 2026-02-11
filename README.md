
# 📦 AI & Optimization-Driven Supply Chain System (End-to-End)

A **deterministic, LP-ready logistics and inventory management system** integrating **demand forecasting, shipment planning, vehicle routing, and dynamic what-if scenario analysis**.

This project demonstrates **cross-domain systems thinking**: from **modeling demand → managing inventory → optimizing shipments and delivery routes** under real-world constraints, implemented in a **fully programmable end-to-end pipeline**.

It’s designed not as a random input → output model, but as a **decision-making system** for real-world logistics operations.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Modules](#modules)

   * [1️⃣ Demand Simulation](#1-demand-simulation)
   * [2️⃣ Demand Forecasting](#2-demand-forecasting)
   * [3️⃣ Inventory & LP Parameters](#3-inventory--lp-parameters)
   * [4️⃣ LP Shipment Planning](#4-lp-shipment-planning)
   * [5️⃣ Vehicle Routing Optimization](#5-vehicle-routing-optimization)
   * [6️⃣ What-If Scenario Analysis](#6-what-if-scenario-analysis)
5. [Technologies Used](#technologies-used)
6. [Learning Outcomes](#learning-outcomes)
7. [How to Run](#how-to-run)
8. [Future Enhancements](#future-enhancements)

---

## Overview

This system simulates **warehouse and city logistics** over a 30-day horizon. It solves **optimization problems** for shipment planning and vehicle routing, incorporates **demand uncertainty**, and enables **dynamic what-if scenario planning**.
**Workflow Diagram:**  
          +----------------+
          |   Simulator    |
          +----------------+
           /              \
          v                v
   +----------------+  +----------------+
   |  Demand Data   |  | Inventory Data |
   +----------------+  +----------------+
          |                |
          v                |
+------------------------+ |
|  Demand Forecasting    | |
+------------------------+ |
| Output: Forecast Output| |
+------------------------+ |
          |                |
          +--------+-------+
                   v
          +------------------------+
          | Inventory Management   |
          +------------------------+
          | Inputs: Forecast Output|
          |         Inventory Data |
          | Outputs: Shipment Plan |
          |          Updated Inventory |
          +------------------------+
                   |          \
                   v           \
          +------------------------+
          |   Vehicle Routing      |
          +------------------------+
          | Inputs: Shipment Plan  |
          |         Updated Inventory |
          | Output: Optimized Routes (per vehicle) |
          +------------------------+
                   |
                   v
          +------------------------+
          |   What-If Scenario     |
          +------------------------+
          | Inputs: Forecast Output|
          |         Shipment Plan  |
          |         Optimized Routes|
          | Output: Adjusted Shipments & Routes |
          +------------------------+

Key focus: **systems-level thinking** rather than just analytics. Integrates:

* Deterministic demand simulation
* Moving-average-based demand forecasting
* Linear programming (LP) for shipment planning
* Multi-vehicle routing optimization
* Scenario-based “what-if” analysis

---

## Features

* **Demand Simulation:** Seasonal demand patterns per city
* **Forecasting:** Moving average with uncertainty bands (P10, P50, P90)
* **Inventory Management:** Warehouse capacity, distance-based cost, CO₂ emissions
* **Vehicle Routing:** Optimize vehicle multiple warehouses with capacity constraints
* **What-If Analysis:** Test scenarios like demand surge or limited warehouse inventory
* **End-to-End System:** From raw demand → forecast → shipment plan → vehicle routing → scenario testing


Ah! Got it — let’s make a **final clean diagram** where **Vehicle Routing has exactly two inputs**:

* **Inventory**
* **Shipment Plan**

And its **output is Optimized Routes (vehicle-level)**. The rest of the flow remains the same. Here’s the corrected ASCII diagram:

```
          +----------------+
          |   Simulator    |
          +----------------+
           /              \
          v                v
   +----------------+  +----------------+
   |  Demand Data   |  | Inventory Data |
   +----------------+  +----------------+
          |                |
          v                |
+------------------------+ |
|  Demand Forecasting    | |
+------------------------+ |
| Output: Forecast Output| |
+------------------------+ |
          |                |
          +--------+-------+
                   v
          +------------------------+
          | Inventory Management   |
          +------------------------+
          | Inputs: Forecast Output|
          |         Inventory Data |
          | Outputs: Shipment Plan |
          |          Updated Inventory |
          +------------------------+
                   |          \
                   v           \
          +------------------------+
          |   Vehicle Routing      |
          +------------------------+
          | Inputs: Shipment Plan  |
          |         Updated Inventory |
          | Output: Optimized Routes (per vehicle) |
          +------------------------+
                   |
                   v
          +------------------------+
          |   What-If Scenario     |
          +------------------------+
          | Inputs: Forecast Output|
          |         Shipment Plan  |
          |         Optimized Routes|
          | Output: Adjusted Shipments & Routes |
          +------------------------+
```

### ✅ Key Features:

1. **Simulator** generates **Demand Data + Inventory Data**.
2. **Demand Forecasting** only takes **Demand Data** → produces **Forecast Output**.
3. **Inventory Management** merges **Forecast Output + Inventory Data** → produces **Shipment Plan + Updated Inventory**.
4. **Vehicle Routing** now correctly takes **Shipment Plan + Updated Inventory** → outputs **Optimized Routes (vehicle-level)**.
5. **What-If Analysis** can adjust all three outputs to produce **final adjusted shipments and routes**.

---

If you want, I can also make a **fully compact “branching arrows” diagram** for README that looks like a **real flowchart but fits in one block**, perfect for portfolio presentation.

Do you want me to do that?


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
│
├── scripts/
│   ├── 01_simulatior.py
│   ├── 02_demand_forecasting.py
│   ├── 03_inventory_management.py
│   ├── 04_vehicle_routing.py
│   └── 05_what_if_scenario_analysis.py
│
├── README.md

```

---

## Modules

### 1️⃣ Demand Simulation

Simulates **daily deterministic demand** per city using **base demand + seasonal sine function**. Generates:

* `demand_data.csv` → daily demand per city
* Initial **warehouse inventory table** with LP parameters

**Key Learnings:**

* Simulating demand patterns
* Preparing LP-ready data
* Distance-based cost and CO₂ calculation

---

### 2️⃣ Demand Forecasting

Performs **moving-average-based forecasting** with uncertainty bands:
MA9 is used.
* `demand_p50` → mean forecast
* `demand_p10` → lower bound (10th percentile)
* `demand_p90` → upper bound (90th percentile)(this is used in further stages for safety)
* 
* 

**Key Learnings:**

* Time series smoothing
* Handling uncertainty dynamically
* City-specific forecasting

---

### 3️⃣ Inventory Data

**Goal:** Create warehouse × city table for LP optimization.

**Setup:**

* **Warehouses:** 2 (W1, W2)
* **Cities:** 4 (Mumbai, Pune, Delhi, Bangalore)
* **Days simulated:** 30
* **Data generated:** ``inventory_data.csv`

**Method:**

* For each warehouse-city pair:

  * Available inventory
  * Distance (Euclidean)
  * Cost per unit (distance × cost/km)
  * CO₂ per unit (distance × CO₂/km)

**Key Learnings:**

* Preparing LP-ready inputs
* Simulating inventory and operational parameters for optimization
* Multi-day, multi-warehouse scenario setup

---

### 4️⃣ LP Shipment Planning(Inventory Management)

Formulates a **Linear Programming (LP)** problem to:

* Decide **shipment quantities** per warehouse → city → day
* **Minimize total cost** = transportation cost + CO₂ emissions + stockout (unmet demand) penalty
* **Objective**: Minimize total transportation cost + weighted CO₂ emissions + stockout (unmet demand) penalty.
* **Constraints:**

  * Total shipments ≤ warehouse available inventory
  * Shipments & unmet demand ≥ 0
* Save results to `shipment_plan_lp.csv`
Here, we are making tradeofs betwwen cost and unment demand to find minimal value of objective.

### 5️⃣ Vehicle Routing Optimization

Optimizes **vehicle-wise shipments** per warehouse:

* Multiple vehicles per warehouse
* Vehicle capacity constraints
* Objective: **Minimize CO₂ emissions**
* Output: `vehicle_routes_optimized.csv`

**Key Learnings:**

* Multi-vehicle routing
* Linking shipment plan → vehicles
* Operational constraint handling

---

### 6️⃣ What-If Scenario Analysis

Dynamic **demand and warehouse inventory adjustments**:

* Increase/decrease demand per city
* Reduce available inventory per warehouse
* Re-run LP to see new shipment and unmet demand results
* Output: `shipment_plan_whatif.csv`

**Key Learnings:**

* Scenario testing for robust planning
* Dynamic LP parameterization
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

## Future Enhancements

* Add **ML-based forecasting models** (ARIMA, LSTM, Prophet) for more adaptive predictions
* Integrate **advanced routing optimization** using VRP/TSP solvers
* Implement **more complex scenario analysis**: seasonal shocks, supply disruptions, dynamic pricing
* Incorporate **multi-modal transport optimization** (road, rail, air) considering CO₂ and time
* Scale system with **additional warehouses and cities**
* Include **inventory replenishment strategies**: safety stock adjustment, lead-time optimization, supplier constraints

---

✅ This project is **not just analytics**, not even MLOps, but a **system-level, end-to-end logistics and optimization solution**, demonstrating skills in **forecasting, optimization, vehicle routing, scenario planning, and dynamic system modeling**.

---
