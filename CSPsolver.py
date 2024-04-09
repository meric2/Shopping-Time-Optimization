from gurobipy import Model, GRB, quicksum
import pandas as pd

# Load data from Excel
products_data = pd.read_excel('MarketData.xlsx', sheet_name='Products')

# Parameters
products = {row['Products']: {'wait_time': row['Waiting Time'], 'price': row['Price'], 'aisle': row['Aisle']} for index, row in products_data.iterrows()}
aisles = ['Entrance', 'Snacks', 'Beverages', 'Dairy', 'Meat and Fish', 'Fruits and Vegetables', 'Bakery', 'Checkout']
shopping_list = ['apple', 'cheese', 'chips', 'cake', 'milk', 'chicken']

# Handling user input
delivery_products = []
for p in shopping_list.copy():
    if p not in products:
        print(f"Product {p} is not available in the market.")
        exit()
    else:
        # Add a delivery item for product with wait time > 4
        if products[p]['wait_time'] > 4:
            delivery_item = f"{p}_delivery"
            products[delivery_item] = {'wait_time': products[p]['wait_time'], 'price': 0, 'aisle': products[p]['aisle']}
            delivery_products.append(delivery_item)

model = Model("Market_Optimization")

# Decision variables for visiting aisles and the sequence
visit_vars = model.addVars(aisles, vtype=GRB.BINARY, name="visit")
sequence_vars = model.addVars(aisles, aisles, vtype=GRB.INTEGER, name="seq")
total_time = 0

# Connectivity of market layout
connectivity = {
    'Entrance': ['Snacks', 'Beverages', 'Dairy', 'Fruits and Vegetables'],
    'Snacks': ['Bakery', "Beverages", "Checkout"],
    'Beverages': ['Dairy', "Snacks", "Bakery", "Checkout"],
    'Dairy': ['Meat and Fish', 'Fruits and Vegetables', "Beverages", "Checkout"],
    'Meat and Fish': ['Bakery', "Dairy", "Fruits and Vegetables"],
    'Fruits and Vegetables': ['Meat and Fish', "Dairy", 'Checkout'],
    'Bakery': ["Beverages", "Snacks", 'Meat and Fish'],
    'Checkout': ['Snacks', 'Beverages', 'Dairy', 'Fruits and Vegetables']
}

# Objective: Minimize the total time to grab all products
model.setObjective((quicksum(sequence_vars[i,j] for i in aisles for j in aisles))*2+total_time, GRB.MINIMIZE)

# Constraints

# Continuity: If an aisle is visited, ensure there's a next aisle in the sequence
for i in aisles:
    model.addConstr(quicksum(sequence_vars[i, j] for j in aisles if i != j) == visit_vars[i], f"continuity_{i}")


# Enforce market layout constraints using connectivity
for aisle in aisles:
    connected_aisles = connectivity[aisle]
    model.addConstrs((sequence_vars[aisle, j] == 0 for j in aisles if j not in connected_aisles), f"no_connection_{aisle}_")


due_time = []
# Ensure aisles with products from the shopping list are visited
for product in shopping_list:
    aisle_for_product = products[product]['aisle']
    if products[product]['wait_time'] > 4:
        model.addConstr(visit_vars[aisle_for_product] == 1, f"visit_{aisle_for_product}")
        due_time.append(products[product]['wait_time']+total_time)
        total_time += 1
    else:
        model.addConstr(visit_vars[aisle_for_product] == 1, f"visit_{aisle_for_product}")
        total_time += products[product]['wait_time']


# Ensure aisles with delivery products are visited
count = 0
for product in delivery_products:
    aisle_for_product = products[product]['aisle']
    if due_time[count] >= total_time:
        model.addConstr(visit_vars[aisle_for_product] == 1, f"visit_{aisle_for_product}")
        total_time += products[product]['wait_time'] - 1 
        count += 1


# Entrance and Checkout must be visited for integrity
model.addConstr(visit_vars['Entrance'] == 1, "start_at_entrance")
model.addConstr(visit_vars['Checkout'] == 1, "end_at_checkout")


# Optimize the model
model.optimize()

# Output the optimal sequence if a solution is found
if model.status == GRB.OPTIMAL:
    runtime = model.Runtime
    objective_value = model.ObjVal
    path = ['Entrance']#[aisle for aisle in aisles if visit_vars[aisle].X > 0.5]
    aisles_passed = 0
    for i in aisles:
        for j in aisles:
            if sequence_vars[i, j].X > 0.5:
                aisles_passed += 1
                #print(f"From {i} to {j}")
                if path[-1] != i:
                    path.append(i)
                    path.append(j)
    
    print(f"\nRuntime: {runtime} seconds")
    print(f"Shopping list: {shopping_list}")
    print(f"Path: {path[:-1]}")
    print(f"Total time for shopping: {aisles_passed*2+total_time} minutes\n")
else:
    print("No optimal solution found or the problem is infeasible.")
    model.computeIIS()  # Compute the Irreducible Infeasible Subsystem (IIS)
    model.write("model.ilp")  # Write the IIS to an .ilp file if model is infeasible
    for c in model.getConstrs():
        if c.IISConstr:
            print('%s' % c.constrName)
