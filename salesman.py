import networkx
import matplotlib.pyplot as plt

# Let's implement a function that solves the Travelling Salesman Problem 
# Let's use branch and bound method to make the optimize the fucntion

# Let's define tyhe function
def salesman(city_map):

    # Let's initialize needed variables
    
    n = len(city_map) # Variable for the amount of node
    shortest = [] # Initialization of the list that contains the shortest path
    min_cost = float("inf") # Variable for the cost of the shortest cpath
    current_path = [] # Variable for the current path
    visited = [False]*n # Variable that contains information of wich vertices are visited
    current_index = 0 # The index of the current vertice
    h = 0 # The cost of the current vertice
    visited_vertices = 0 # variable for the amount of visited vertices


    # Let's implement the branch and bound method

    min_weights = [0]*n # List that contains
    for i in range(n): # Loop that goes through all the vertices
        min_weight = city_map[i][0] # Variable for the smallest weight, let's initialize it with the weight of the first node
        for j in range(n): # Loop that finds the edge with the smallest weight
            if min_weight == 0:
                min_weight = city_map[i][j]
            if city_map[i][j] < min_weight and city_map[i][j] != 0:
                min_weight = city_map[i][j]
        min_weights[i] = min_weight
    sum_of_min_weights = sum(min_weights) # Let's calculate the sum of the smallest weights

    # Let's call the recursive fucntion that finds the shortest roud

    salesman_help(n,current_index,current_path,shortest,h,min_cost,visited,city_map,visited_vertices,sum_of_min_weights,min_weights)

    return shortest # Let's return the shortest rote


# Let's implemnt a recursive function that fins the shortest roud
def salesman_help(n,current_index,current_path,shortest,h,min_cost,visited,city_map,visited_vertices,sum_of_min_weights,min_weights):

    sum_of_min_weights = sum_of_min_weights - min_weights[current_index]  # Let's subtract the smallest wieght of the visited vertice from the sum of all smallest weights
    visited[current_index] = True # Let's mark the vertice to be visited
    visited_vertices += 1 # Let's update the amount of visited vartices
    current_path.append(current_index) # Let's add the current vertice to current current_path
    if visited_vertices == n: # If all the vertices are visited, a new candidate for the shortest roud is found
        h = h + city_map[current_index][0] # Let's add the weight of the edge from the last vetrice to the first vertice
        if h < min_cost: 
            # If the cost of the current current_path is smaller than the cost of the shortest current_path the current current_path becomes the new shortest current_path
            min_cost = h 
            shortest.clear()
            for item in current_path:
                shortest.append(item)
            shortest.append(0)
        return min_cost # Let's return the wieght of the shortest current_path
    else: # If all the vetrices are not visited we continue calling the fucntion recursively
        for i in range(n):
            if visited[i] == False and h + city_map[current_index][i] + sum_of_min_weights < min_cost:
                # Let's make temporary variables to save the current lists
                temp_current_path = []
                temp_visited = []
                for item in current_path:
                    temp_current_path.append(item)
                for item in visited:
                    temp_visited.append(item)
                # Let's call the funktion recutsively
                min_cost = salesman_help(n,i,current_path,shortest,h+city_map[current_index][i],min_cost,visited,city_map,visited_vertices,sum_of_min_weights,min_weights)
                current_path.clear()
                visited.clear()
                for item in temp_current_path:
                    current_path.append(item)
                for item in temp_visited:
                    visited.append(item)
        return min_cost
        

# Let's implement a fucntion to draw the  graph
def draw_graph(city_map,current_path):
    n = len(city_map)
    G = networkx.Graph()

    #Let's create the nodes
    for i in range(0,n):
        G.add_node(i)
    pos = networkx.spring_layout(G)

    # Let's create the edges
    for i in range(0,n):   
        for j in range(i+1,n):
            if i != j:
                G.add_edge(i,j,weight=city_map[i][j])

    edge_labels = networkx.get_edge_attributes(G,'weight')

    # Let's define different color for the edges that are included in the shortest path
    excpetions = []
    previous = 0
    for i in range(1,n+1):
       j = current_path[i]
       excpetions.append((previous,j))
       excpetions.append((j,previous))
       previous = j

    edge_colors = []
    for edge in G.edges:
        if edge in excpetions:
            edge_colors.append('blue')
        else:
            edge_colors.append('black')

    # Let's draw the graph
    networkx.draw(G,pos,with_labels=True,edge_color=edge_colors,node_color='lightblue')
    networkx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    plt.show()
    return 


# Example run
if __name__ == "__main__":
    cost = 0
    city_map = [
    #     0   1   2   3   4
        [ 0, 12, 19, 16, 29],   # 0
        [12,  0, 27, 25,  5],   # 1
        [19, 27,  0,  8,  4],   # 2
        [16, 25,  8,  0, 14],   # 3
        [29,  5,  4, 14,  0]    # 4
        ]

    shortest = salesman(city_map)
    draw_graph(city_map,shortest)
    # Let's calculate the cost of the shortest path
    for i in range(len(city_map)):
        cost += city_map[shortest[i]][shortest[i+1]]
    
    print(shortest)     # [0, 1, 4, 2, 3, 0]
    print(cost)     # 45