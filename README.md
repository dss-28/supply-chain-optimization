
# 📦 AI-Driven End-to-End Supply Chain Optimization System

An **end-to-end decision-making system** for supply chain planning integrating:

* Demand simulation & forecasting
* Inventory modeling
* Linear programming–based shipment optimization
* Vehicle routing optimization
* What-if scenario analysis

This is not a single ML model.
It is a **structured optimization pipeline** that models real-world logistics trade-offs under constraints.

---

## 🔎 Problem Statement

Modern logistics systems must answer:

* How much should each warehouse ship to each city?
* How do we balance transportation cost, emissions, and stockouts?
* How should shipments be distributed across vehicles with capacity constraints?
* What happens under demand surge or inventory disruption?

This project builds a programmable system to answer those questions across a 30-day horizon.

---

## 🧠 System Architecture

```
Demand Simulation
        ↓
Demand Forecasting (P10 / P50 / P90)
        ↓
Inventory & LP Parameter Builder
        ↓
Shipment Optimization (Linear Programming)
        ↓
Vehicle Routing Optimization
        ↓
What-If Scenario Re-Optimization
```

Each stage produces structured outputs used by the next stage, forming a complete decision pipeline.

---

## ⚙️ Core Components

### 1️⃣ Demand Simulation

* City-level daily demand generation
* Seasonal pattern using sinusoidal variation
* 30-day planning horizon
* Outputs structured demand table

Purpose:
Create controlled but realistic demand dynamics for optimization testing.

---

### 2️⃣ Demand Forecasting

* Moving Average (MA9)
* Generates:

  * P50 (expected demand)
  * P10 / P90 (uncertainty bands)

P90 is used for safety-aware planning.

Purpose:
Introduce uncertainty-aware planning instead of deterministic allocation.

---

### 3️⃣ Inventory & LP Parameter Modeling

For each warehouse → city pair:

* Available inventory
* Distance (Euclidean)
* Transportation cost per unit
* CO₂ emissions per unit
* Multi-day setup

This stage converts raw simulation into **LP-ready structured data**.

---

### 4️⃣ Shipment Optimization (Linear Programming)

Decision Variables:

* Shipment quantity (warehouse → city → day)
* Unmet demand

Objective:

Minimize:

Total Transport Cost

* λ₁ × CO₂ Emissions
* λ₂ × Stockout Penalty

Subject to:

* Warehouse inventory constraints
* Non-negativity constraints

This explicitly models trade-offs between:

* Cost efficiency
* Sustainability
* Service level

Solver: PuLP (CBC)

Output:
`shipment_plan_lp.csv`

---

### 5️⃣ Vehicle Routing Optimization

Given shipment quantities:

* Multiple vehicles per warehouse
* Vehicle capacity constraints
* Allocation of shipments to vehicles
* Objective: minimize emissions

This bridges planning-level optimization with operational execution.

Output:
`vehicle_routes_optimized.csv`

---

### 6️⃣ What-If Scenario Analysis

Supports:

* Demand surge scenarios
* Reduced warehouse inventory
* Re-optimization under new constraints

Demonstrates robustness testing and stress analysis.

Output:
`shipment_plan_whatif.csv`

---

## 📊 Key Design Decisions

* Deterministic simulation for controlled evaluation
* Forecast uncertainty incorporated into planning
* Explicit multi-objective trade-off modeling
* Separation of planning layer and routing layer
* Fully modular pipeline (each stage independently executable)

---

## 🛠️ Tech Stack

* Python 3.10+
* pandas
* numpy
* PuLP (LP solver)
* CSV-based modular data exchange

---

## 🚀 What This Project Demonstrates

* Systems thinking across forecasting + optimization + operations
* Mathematical modeling of constrained decision systems
* Multi-objective trade-off design
* Operational constraint integration
* Structured pipeline architecture
* Scenario-based strategic planning

This is not a toy ML project.
It is a simplified but complete logistics decision system.

---

## 🔮 Future Extensions

* Replace moving average with ML forecasting (ARIMA / LSTM / Transformer)
* Full VRP solver integration
* Stochastic programming instead of deterministic LP
* Dynamic multi-period inventory replenishment
* Multi-modal transport modeling
* Reinforcement learning–based adaptive policy optimization

---

# 🎯 Why This Matters

This project demonstrates the ability to:

* Translate a real-world operational problem into mathematical form
* Design structured optimization pipelines
* Model trade-offs explicitly
* Build programmable decision systems

It is built as a foundation for more advanced research in:

* Operations Research
* Optimization + ML hybrid systems
* Reinforcement learning for supply chain control
* Sustainable logistics modeling

---
