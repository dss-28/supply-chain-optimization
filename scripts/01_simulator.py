import numpy as np
import pandas as pd
import math
import os

os.makedirs("data", exist_ok=True)

# =====================================================
# Logistics Simulator Class (Deterministic, LP-ready)
# =====================================================

class LogisticsSimulator:
    def __init__(self, warehouses, cities, transport):
        self.warehouses = warehouses
        self.cities = cities
        self.transport = transport

    def distance(self, loc1, loc2):
        return math.sqrt((loc1[0] - loc2[0])**2 +
                         (loc1[1] - loc2[1])**2)

    def simulate_demand_day(self, day):
        """Deterministic demand per city using seasonal sine curve"""
        records = []
        for city in self.cities:
            seasonal = city["seasonality"] * np.sin(day / 5)
            demand = max(0, round(city["base_demand"] + seasonal))
            records.append({
                "day": day + 1,
                "city": city["id"],
                "demand": demand
            })
        return records

    def generate_inventory_table(self):
        """Generate warehouse x city table with LP parameters"""
        records = []
        for wh in self.warehouses:
            for city in self.cities:
                dist = self.distance(wh["loc"], city["loc"])
                records.append({
                    "warehouse": wh["id"],
                    "city": city["id"],
                    "available_inventory": wh["inventory"],
                    "distance_km": round(dist, 2),
                    "cost_per_unit": round(dist * self.transport["cost_per_km"], 2),
                    "co2_per_unit": round(dist * self.transport["co2_per_km"], 2)
                })
        return records

# =====================================================
# CONFIGURATION
# =====================================================

warehouses = [
    {"id": "W1", "loc": (0, 0), "capacity": 1000, "inventory": 15000},
    {"id": "W2", "loc": (10, 5), "capacity": 800, "inventory": 12000},
]

cities = [
    {"id": "Mumbai", "loc": (2, 3), "base_demand": 60, "seasonality": 10},
    {"id": "Pune", "loc": (3, 4), "base_demand": 50, "seasonality": 8},
    {"id": "Delhi", "loc": (12, 15), "base_demand": 80, "seasonality": 15},
    {"id": "Bangalore", "loc": (8, 10), "base_demand": 70, "seasonality": 12},
]

transport = {"cost_per_km": 2.5, "co2_per_km": 0.9}

DAYS = 30

# =====================================================
# RUN SIMULATION
# =====================================================

sim = LogisticsSimulator(warehouses, cities, transport)

# 1️⃣ Demand data
all_demand = []
for day in range(DAYS):
    daily_demand = sim.simulate_demand_day(day)
    all_demand.extend(daily_demand)

demand_df = pd.DataFrame(all_demand)
demand_df.to_csv("data/demand_data.csv", index=False)
print("✅ demand_data.csv created")
print(demand_df.head())

# 2️⃣ Inventory + LP parameters
inventory_df = pd.DataFrame(sim.generate_inventory_table())
inventory_df.to_csv("data/inventory_data.csv", index=False)
print("✅ inventory_data.csv created")
print(inventory_df.head())
