import pandas as pd
import pulp as pl

# -----------------------------
# CONFIG
# -----------------------------
SHIPMENT_PLAN_PATH = "data/shipment_plan_lp.csv"
INVENTORY_PATH = "data/inventory_data.csv"  # For distances
OUTPUT_PATH = "data/vehicle_routes_optimized.csv"

WAREHOUSE_VEHICLES = {
    "W1": {"num_vehicles": 3, "capacity": 40},
    "W2": {"num_vehicles": 2, "capacity": 50}
}

CO2_PER_KM_PER_UNIT = 0.9  # example CO2 factor

# -----------------------------
# LOAD DATA
# -----------------------------
ship_df = pd.read_csv(SHIPMENT_PLAN_PATH)
inv_df = pd.read_csv(INVENTORY_PATH)

# Distance lookup: warehouse -> city
dist_lookup = {(row['warehouse'], row['city']): row['distance_km'] for _, row in inv_df.iterrows()}

WAREHOUSES = ship_df['warehouse'].unique()
CITIES = ship_df['city'].unique()
DAYS = sorted(ship_df['day'].unique())

# -----------------------------
# LP PROBLEM
# -----------------------------
prob = pl.LpProblem("Vehicle_Routing_Optimized", pl.LpMinimize)

# Decision variables: shipped quantity from warehouse vehicle to city per day
ship_qty = {}
for _, row in ship_df.iterrows():
    w = row['warehouse']
    day = row['day']
    city = row['city']
    for i in range(WAREHOUSE_VEHICLES[w]['num_vehicles']):
        vid = f"{w}_V{i+1}"
        ship_qty[(w, vid, city, day)] = pl.LpVariable(f"ship_{w}_{vid}_{city}_{day}", lowBound=0)

# -----------------------------
# OBJECTIVE FUNCTION: Minimize CO2 distance cost
# -----------------------------
prob += pl.lpSum([
    ship_qty[(w, vid, city, day)] * dist_lookup[(w, city)] * CO2_PER_KM_PER_UNIT
    for (w, vid, city, day) in ship_qty
]), "Total_CO2"

# -----------------------------
# CONSTRAINTS
# -----------------------------

# 1️⃣ Meet shipment demand per city per day (from LP shipment plan)
for _, row in ship_df.iterrows():
    w = row['warehouse']
    city = row['city']
    day = row['day']
    demand = row['shipped_qty']
    prob += pl.lpSum([ship_qty[(w, vid, city, day)] for i in range(WAREHOUSE_VEHICLES[w]['num_vehicles']) 
                      for vid in [f"{w}_V{i+1}"]]) == demand, f"Demand_{w}_{city}_{day}"

# 2️⃣ Vehicle capacity per day
for w in WAREHOUSES:
    for i in range(WAREHOUSE_VEHICLES[w]['num_vehicles']):
        vid = f"{w}_V{i+1}"
        cap = WAREHOUSE_VEHICLES[w]['capacity']
        for day in DAYS:
            prob += pl.lpSum([ship_qty[(w, vid, city, day)] 
                              for city in CITIES if (w, vid, city, day) in ship_qty]) <= cap, f"Cap_{vid}_{day}"

# -----------------------------
# SOLVE LP
# -----------------------------
prob.solve(pl.PULP_CBC_CMD(msg=1))
print("Status:", pl.LpStatus[prob.status])

# -----------------------------
# SAVE RESULTS
# -----------------------------
results = []
for key, var in ship_qty.items():
    w, vid, city, day = key
    results.append({
        "day": day,
        "warehouse": w,
        "vehicle": vid,
        "city": city,
        "shipped_qty": var.varValue
    })

df_routes = pd.DataFrame(results)
df_routes.to_csv(OUTPUT_PATH, index=False)
print("✅ Optimized vehicle routes saved to", OUTPUT_PATH)
print(df_routes.head(10))
