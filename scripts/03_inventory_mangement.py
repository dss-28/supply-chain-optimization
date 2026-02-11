import pandas as pd
import pulp as pl

# -----------------------------
# CONFIG
# -----------------------------
INVENTORY_PATH = "data/inventory_data.csv"
DEMAND_PATH = "data/demand_forecast.csv"
OUTPUT_PATH = "data/shipment_plan_lp.csv"

LAMBDA = 0.5   # weight for CO2 in objective
MU = 50.0     # weight for stockout penalty

# -----------------------------
# LOAD DATA
# -----------------------------
inv_df = pd.read_csv(INVENTORY_PATH)
demand_df = pd.read_csv(DEMAND_PATH)

# Merge demand_p90 for safety stock
inv_df = inv_df.merge(demand_df[['city','day','demand_p90']], on='city', how='left')

WAREHOUSES = inv_df['warehouse'].unique()
CITIES = inv_df['city'].unique()
DAYS = sorted(demand_df['day'].unique())

# -----------------------------
# LP PROBLEM
# -----------------------------
prob = pl.LpProblem("Shipment_Plan", pl.LpMinimize)

# -----------------------------
# DECISION VARIABLES
# -----------------------------
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

# -----------------------------
# OBJECTIVE FUNCTION
# -----------------------------
prob += (
    pl.lpSum([
        ship_qty[row.warehouse, row.city, row.day] * (row.cost_per_unit + LAMBDA * row.co2_per_unit)
        for idx, row in inv_df.iterrows()
    ]) + MU * pl.lpSum([unmet_demand[c,d] for c in CITIES for d in DAYS])
), "Total_Cost_CO2_Stockout"

# -----------------------------
# CONSTRAINTS
# -----------------------------
# 1️⃣ Meet demand with safety stock
for c in CITIES:
    for d in DAYS:
        demand_p90 = demand_df.loc[(demand_df.city==c) & (demand_df.day==d), 'demand_p90'].values[0]
        prob += (
            pl.lpSum([ship_qty[w, c, d] for w in WAREHOUSES if (w,c,d) in ship_qty]) + unmet_demand[c,d]
            >= demand_p90
        ), f"SafetyStock_{c}_{d}"

# 2️⃣ Warehouse capacity: cannot ship more than available inventory
inv_available = { (row.warehouse,row.city): row.available_inventory for idx,row in inv_df.iterrows() }

for w in WAREHOUSES:
    for d in DAYS:
        prob += (
            pl.lpSum([ship_qty[w, c, d] for c in CITIES if (w,c,d) in ship_qty])
            <= sum(inv_available.get((w,c),0) for c in CITIES)
        ), f"WarehouseCapacity_{w}_{d}"

# -----------------------------
# SOLVE LP
# -----------------------------
prob.solve(pl.PULP_CBC_CMD(msg=1))
print("Status:", pl.LpStatus[prob.status])

# -----------------------------
# SAVE RESULTS
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
print("✅ Shipment plan saved to", OUTPUT_PATH)
print(df_results.head())
