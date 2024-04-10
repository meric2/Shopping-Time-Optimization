import numpy as np
from collections import deque
import random
import datetime

# Market Design 

class Product:
    def __init__(self, name, wait_time=1, price=1, aisle=None):
        self.name = name
        self.wait_time = wait_time  # in minutes
        self.price = price
    

class Graph:
    
    def __init__(self):
        self.adjacency_list = {}
        
    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
            
    def add_edge(self, from_node, to_node):
        if from_node in self.adjacency_list and to_node in self.adjacency_list:
            self.adjacency_list[from_node].append((to_node))
            self.adjacency_list[to_node].append((from_node))
    
    def getNode(self, node):
        return node
            
    # find the shortest path between two aisles
    def BFS(self, start, goal):
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == goal:
                return path

            if node not in visited:
                for adjacent in self.adjacency_list.get(node, []):
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)

                    if adjacent == goal:
                        temp = []
                        for t in new_path:
                            temp.append(str(t))
                        return temp

                visited.add(node)

        return None
        
    def get_time(self, start, goal):
        shortest_path = self.BFS(start, goal)
        time = (len(shortest_path) - 1) * 2  # each aisle transition takes 2 minutes
        return time
    
    def get_items_in_path(self, path):
        products = set()
        for node in path:
            products.update(self.Node(node).getItems())
        return products

    def get_items_in_node(self, node):
        print(self.getNode(node), self.Node(node).getItems())
        return self.Node(node).items

    def contains_product(self, aisle, product):
        return product in self.get_items_in_node(aisle)
    
    class Node:

        def __init__(self, name, items=[], time=2):
            self.name = name
            self.items = items
            self.time = time

        def getName(self):
            return self.name

        def getItems(self):
            return self.items
        
        def getTime(self):
            return self.time
        
        def __str__(self):
            return self

        def contains(self, products):
            return any(item in products for item in self.items)
        

# Product List

# Fruits and Vegetables
apple = Product("Apple", price=5)
banana = Product("Banana", price=4)
orange = Product("Orange", price=6)
grapes = Product("Grapes", price=8)
strawberry = Product("Strawberry", price=10)
pear = Product("Pear", price=5)
kiwi = Product("Kiwi", price=7)
carrot = Product("Carrot", price=3)
potato = Product("Potato", price=2)
tomato = Product("Tomato", price=4)
lettuce = Product("Lettuce", price=3)
cucumber = Product("Cucumber", price=2)
peppers = Product("Peppers", price=5)
onion = Product("Onion", price=2)
mushrooms = Product("Mushrooms", price=6)

# Dairy
milk = Product("Milk", price=4)
cheese = Product("Cheese", wait_time=6, price=30)
yoghurt = Product("Yogurt", wait_time=1, price=9)
butter = Product("Butter", price=15)
cream = Product("Cream", price=7)
eggs = Product("Eggs", wait_time=1, price=10)

# Bakery
bread = Product("Bread", price=3)
croissant = Product("Croissant", price=5)
baguette = Product("Baguette", price=4)
muffin = Product("Muffin", price=2)
cake = Product("Cake", wait_time=15, price=20)
pie = Product("Pie", wait_time=8, price=15)

# Meat and Fish
sausage = Product("Sausage", price=20)
bacon = Product("Bacon", price=22)
meat = Product("Meat", wait_time=8, price=50)
fish = Product("Fish", wait_time=10, price=40)
chicken = Product("Chicken", wait_time=15, price=25)
shrimp = Product("Shrimp", wait_time=6, price=35)

# Beverages
orange_juice = Product("Orange Juice", price=6)
coffee = Product("Coffee", price=15)
tea = Product("Tea", price=12)
water = Product("Water", price=1)
soda = Product("Soda", price=3)
beer = Product("Beer", price=5)
wine = Product("Wine", price=15)

# Snacks and Others
chocolate = Product("Chocolate", price=7)
chips = Product("Chips", price=4)
nuts = Product("Nuts", price=10)
crackers = Product("Crackers", price=5)
pasta = Product("Pasta", price=8)
rice = Product("Rice", price=5)
cereal = Product("Cereal", price=8)
honey = Product("Honey", price=12)

# Delivery items
cheese_delivery = Product("Cheese_delivery", wait_time=0, price=30)
cake_delivery = Product("Cake_delivery", wait_time=0, price=20)
pie_delivery = Product("Pie_delivery", wait_time=0, price=15)
meat_delivery = Product("Meat_delivery", wait_time=0, price=50)
fish_delivery = Product("Fish_delivery", wait_time=0, price=40)
chicken_delivery = Product("Chicken_delivery", wait_time=0, price=25)
shrimp_delivery = Product("Shrimp_delivery", wait_time=0, price=35)


market_graph = Graph()

# defining the aisles and adding the products
entrance = Graph.Node(name="Entrance")
bakery = Graph.Node("Bakery", [bread, croissant, baguette, muffin, cake, pie, cake_delivery, pie_delivery])
meat_fish = Graph.Node("Meat and Fish", [meat, fish, chicken, sausage, bacon, shrimp, meat_delivery, fish_delivery, chicken_delivery, shrimp_delivery])
fruit_veg = Graph.Node("Fruits and Vegetables", [apple, banana, orange, grapes, strawberry, pear, kiwi, carrot, potato, tomato, lettuce, cucumber, peppers, onion, mushrooms])
dairy = Graph.Node("Dairy", [milk, cheese, yoghurt, butter, cream, eggs, cheese_delivery])
beverages = Graph.Node("Beverages", [orange_juice, coffee, tea, water, soda, beer, wine])
snacks = Graph.Node("Snacks", [chocolate, chips, nuts, crackers, pasta, rice, cereal, honey])
checkout = Graph.Node(name="Checkout")

# adding the aisles to the market
market_graph.add_node("Entrance")
market_graph.add_node("Bakery")
market_graph.add_node("Meat and Fish")
market_graph.add_node("Fruits and Vegetables")
market_graph.add_node("Dairy")
market_graph.add_node("Beverages")
market_graph.add_node("Snacks")
market_graph.add_node("Checkout")

# connecting aisles
market_graph.add_edge("Entrance", "Snacks")
market_graph.add_edge("Entrance", "Beverages")
market_graph.add_edge("Entrance", "Dairy")
market_graph.add_edge("Entrance", "Fruits and Vegetables")
market_graph.add_edge("Bakery", "Snacks")
market_graph.add_edge("Bakery", "Beverages")
market_graph.add_edge("Meat and Fish", "Dairy")
market_graph.add_edge("Meat and Fish", "Fruits and Vegetables")
market_graph.add_edge("Snacks", "Beverages")
market_graph.add_edge("Snacks", "Checkout")
market_graph.add_edge("Beverages", "Dairy")
market_graph.add_edge("Beverages", "Checkout")
market_graph.add_edge("Dairy", "Fruits and Vegetables")
market_graph.add_edge("Dairy", "Checkout")
market_graph.add_edge("Fruits and Vegetables", "Checkout")


# creating a list for product locations
product_aisle_map = {
    bakery: [bread, croissant, baguette, muffin, cake, pie, cake_delivery, pie_delivery],
    meat_fish: [meat, fish, chicken, sausage, bacon, shrimp, meat_delivery, fish_delivery, chicken_delivery, shrimp_delivery],
    fruit_veg: [apple, banana, orange, grapes, strawberry, pear, kiwi, carrot, potato, tomato, lettuce, cucumber, peppers, onion, mushrooms],
    dairy: [milk, cheese, yoghurt, butter, cream, eggs, cheese_delivery],
    beverages: [orange_juice, coffee, tea, water, soda, beer, wine],
    snacks: [chocolate, chips, nuts, crackers, pasta, rice, cereal, honey]
}

def get_product_name(list_):
    name_list = []
    for i in list_:
        name_list.append(i.name)
    return name_list

class GeneticAlgorithm:
    def __init__(self, product_list, product_aisle_map, market_graph, population_size=50, generations=100, mutation_rate=0, crossover_rate=0.8):
        self.product_list = sorted(product_list, key=lambda product: product.wait_time, reverse=True)# so that algorithm orders products with longer wait times first
        self.product_aisle_map = product_aisle_map
        self.market_graph = market_graph
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.aisles = list(product_aisle_map.keys())

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = self.aisles.copy()
            random.shuffle(individual)
            population.append(individual)
        return population

    def fitness(self, individual):
        total_time = 0
        items_picked = set()
        current_location = 'Entrance'
        due_time = {}
        for aisle in individual:
            # Add time to move to the next aisle
            total_time += self.market_graph.get_time(current_location, aisle.getName())#BFS
            current_location = aisle.getName()
            
            # Check products in the current aisle
            for product in self.product_aisle_map[aisle]:
                #print(product.name, total_time, product.wait_time)
                if product in self.product_list and product not in items_picked:
                    #print(product.name, total_time, product.wait_time)
                    if "delivery" in product.name:
                        #print(product.name, total_time, product.wait_time)
                        # If it's a delivery item, pick it up if the order is ready
                        if product.name in due_time and due_time[product.name] <= total_time:
                            # do not pick up delivery item before it is ordered
                            items_picked.add(product)
                            total_time += 1
                            #items_picked.add(product)
                    elif product.wait_time > 4:# chicken 15, cheese 6
                        # If the product has a long wait time, pick it up and order it (_delivery item)
                        total_time += 1
                        due_time[product.name + "_delivery"] = total_time + product.wait_time - 1
                        items_picked.add(product)
                    else:
                        # For other products, add their wait time
                        total_time += product.wait_time
                        items_picked.add(product)

        # Add time to move to checkout from the last aisle
        total_time += self.market_graph.get_time(current_location, 'Checkout')

        # Check if all products were picked up, add penalty if not
        if len(items_picked) < len(self.product_list):
            total_time += 10 * (len(self.product_list) - len(items_picked))

        return total_time



    def select_parents(self, population, fitnesses):
        parents = []
        for _ in range(self.population_size):
            tournament = random.sample(list(zip(population, fitnesses)), k=5)
            best_individual = min(tournament, key=lambda x: x[1])[0]
            parents.append(best_individual)
        return parents

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 2)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    def mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                swap_with = random.randint(0, len(individual) - 1)
                # Ensure we are not creating consecutive duplicates
                while individual[i].name == individual[swap_with].name and len(set([node.name for node in individual])) > 1:
                    swap_with = random.randint(0, len(individual) - 1)
                individual[i], individual[swap_with] = individual[swap_with], individual[i]
        return individual

    def run(self):
        population = self.initialize_population()
        for generation in range(self.generations):
            fitnesses = [self.fitness(individual) for individual in population]
            parents = self.select_parents(population, fitnesses)
            offspring = []
            for i in range(0, self.population_size, 2):
                child1, child2 = self.crossover(parents[i], parents[i+1])
                offspring.append(self.mutate(child1))
                offspring.append(self.mutate(child2))
            population = offspring  # replace the old population with offspring
            best_fitness = min(fitnesses)
            print(f"Generation {generation+1}: Best Fitness = {best_fitness}")
        best_individual = population[fitnesses.index(min(fitnesses))]
        return best_individual, min(fitnesses)



start_time = datetime.datetime.now()
shopping_list = [apple, cheese, chips, chicken]  # Define the product list the user wants to buy

# Handling the user input
for p in shopping_list:
    if p.wait_time > 4:
        delivery_item = f"{p.name}_delivery"
        for aisle, products in product_aisle_map.items():
            for curr_p in products:
                if curr_p.name == delivery_item:
                    shopping_list.append(curr_p)
                    break

ga = GeneticAlgorithm(
    product_list=shopping_list,
    product_aisle_map=product_aisle_map,
    market_graph=market_graph
)

best_path, best_fitness = ga.run()
optimal_path_names = ['Entrance'] + [node.name for node in best_path] + ['Checkout']
end_time = datetime.datetime.now()
elapsed_time = end_time - start_time
total_seconds = elapsed_time.total_seconds()

print(f"\nThe algorithm took {total_seconds} seconds to find the optimal path:")
print(f"Shopping List: {get_product_name(shopping_list)}")
print(f"Optimal Shopping Path: {optimal_path_names}")
print(f"Optimal Shopping Time: {best_fitness} minutes\n")