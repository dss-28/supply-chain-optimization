import pandas as pd
import pulp as pl

# -----------------------------
# CONFIG
# -----------------------------
INVENTORY_PATH = "data/inventory_data.csv"
DEMAND_PATH = "data/demand_forecast.csv"
OUTPUT_PATH = "data/shipment_plan_whatif.csv"

LAMBDA = 0.5
MU = 50.0

# -----------------------------
# LOAD DATA
# -----------------------------
inv_df = pd.read_csv(INVENTORY_PATH)
demand_df = pd.read_csv(DEMAND_PATH)

# -----------------------------
# WHAT-IF SCENARIO
# -----------------------------
demand_multiplier = {
    "Mumbai": 1.2,    # 20% higher demand
    "Pune": 1.1,      # 10% higher demand
    "Delhi": 0.9      # 10% lower demand
}

warehouse_multiplier = {
    "W1": 0.9,   # 90% of inventory available
    "W2": 1.0
}

# Apply demand multiplier
demand_df['demand_p90'] = demand_df.apply(
    lambda row: row['demand_p90'] * demand_multiplier.get(row['city'], 1.0), axis=1
)

# Apply warehouse multiplier
inv_df['available_inventory'] = inv_df.apply(
    lambda row: row['available_inventory'] * warehouse_multiplier.get(row['warehouse'], 1.0), axis=1
)

# Merge demand
inv_df = inv_df.merge(demand_df[['city','day','demand_p90']], on='city', how='left')

WAREHOUSES = inv_df['warehouse'].unique()
CITIES = inv_df['city'].unique()
DAYS = sorted(demand_df['day'].unique())

# -----------------------------
# LP PROBLEM
# -----------------------------
prob = pl.LpProblem("Shipment_Plan_WhatIf", pl.LpMinimize)

# Decision Variables
ship_qty = pl.LpVariable.dicts(
    "ship",
    ((row.warehouse, row.city, row.day) for idx, row in inv_df.iterrows()),
    lowBound=0,
    cat='Continuous'
)

unmet_demand = pl.LpVariable.dicts(
    "unmet",
    ((c,d) for c in CITIES for d in DAYS),
    lowBound=0,
    cat='Continuous'
)

# Objective
prob += (
    pl.lpSum([ship_qty[row.warehouse, row.city, row.day] * (row.cost_per_unit + LAMBDA * row.co2_per_unit)
              for idx, row in inv_df.iterrows()]) 
    + MU * pl.lpSum([unmet_demand[c,d] for c in CITIES for d in DAYS])
), "Total_Cost_CO2_Stockout"

# Constraints
# 1️⃣ Meet demand
for c in CITIES:
    for d in DAYS:
        demand_p90 = demand_df.loc[(demand_df.city==c) & (demand_df.day==d), 'demand_p90'].values[0]
        prob += (
            pl.lpSum([ship_qty[w, c, d] for w in WAREHOUSES if (w,c,d) in ship_qty]) + unmet_demand[c,d]
            >= demand_p90
        ), f"SafetyStock_{c}_{d}"

# 2️⃣ Warehouse capacity
inv_available = { (row.warehouse,row.city): row.available_inventory for idx,row in inv_df.iterrows() }

for w in WAREHOUSES:
    for d in DAYS:
        prob += (
            pl.lpSum([ship_qty[w, c, d] for c in CITIES if (w,c,d) in ship_qty])
            <= sum(inv_available.get((w,c),0) for c in CITIES)
        ), f"WarehouseCapacity_{w}_{d}"

# -----------------------------
# Solve
# -----------------------------
prob.solve(pl.PULP_CBC_CMD(msg=1))
print("Status:", pl.LpStatus[prob.status])

# -----------------------------
# Save results
# -----------------------------
results = []
for (w,c,d), var in ship_qty.items():
    results.append({
        "warehouse": w,
        "city": c,
        "day": d,
        "shipped_qty": var.varValue,
        "unmet_demand": unmet_demand[c,d].varValue if (c,d) in unmet_demand else 0
    })

df_results = pd.DataFrame(results)
df_results.to_csv(OUTPUT_PATH, index=False)
print("✅ What-if shipment plan saved to", OUTPUT_PATH)
print(df_results.head())
