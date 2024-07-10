import pygame
import heapq



class Map_:
    def __init__(self, map_, cost_obstacles):
        self.map_ = map_
        self.cost_obstacles = cost_obstacles
      
    def get_obstacle(self):
        while True:
            obstacle = input("Ingrese las coordenadas de los obstaculos y que tipo de obstaculo es (en formato x, y) o fin para terminar: ").lower()
            if obstacle == 'fin':
                break
            try:
                x, y = map(int, obstacle.split())
                if x < 0 or x >= len(self.map_) or y < 0 or y >= len(self.map_[0]):
                    print("Las coordenadas ingresadas están fuera del rango del mapa, por favor intente de nuevo")
                    continue
                self.map_[x][y] = 1  # Asignar un valor de obstáculo
            except (ValueError, IndexError):
                print("Entrada inválida, por favor ingrese dos números enteros válidos separados por un espacio")
            
    def get_start_point(self):
        while True:
            try:
                start = input("Ingrese las coordenadas de inicio (en formato x, y): ")
                x, y = map(int, start.split())
                if x < 0 or x >= len(self.map_) or y < 0 or y >= len(self.map_[0]):
                    print("Las coordenadas ingresadas están fuera del rango del mapa, por favor intente de nuevo")
                    continue
                if self.map_[x][y] in self.cost_obstacles:
                    print("Las coordenadas ingresadas son un obstáculo, por favor intente de nuevo")
                    continue
                self.map_[x][y] = 'I'
                return (x, y)
            except (ValueError, IndexError):
                print("Entrada inválida, por favor ingrese dos números enteros válidos separados por un espacio")
    
    def get_end_point(self):
        while True:
            try:
                end = input("Ingrese las coordenadas de fin (en formato x, y): ")
                x, y = map(int, end.split())
                if x < 0 or x >= len(self.map_) or y < 0 or y >= len(self.map_[0]):
                    print("Las coordenadas ingresadas están fuera del rango del mapa, por favor intente de nuevo")
                    continue
                if self.map_[x][y] in self.cost_obstacles:
                    print("Las coordenadas ingresadas son un obstáculo, por favor intente de nuevo")
                    continue
                self.map_[x][y] = 'F'
                return (x, y)
            except (ValueError, IndexError):
                print("Entrada inválida, por favor ingrese dos números enteros válidos separados por un espacio")
                
    def print_map(self):
        for row in self.map_:
            print(' '.join(map(str, row)))

class Route_calculator:
    def __init__(self, cost_obstacles):
        self.cost_obstacles = cost_obstacles
    
    def heuristic_function(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, pos, map_):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            neighbor = (pos[0] + d[0], pos[1] + d[1])
            if 0 <= neighbor[0] < len(map_) and 0 <= neighbor[1] < len(map_[0]) and map_[neighbor[0]][neighbor[1]] != 1:
                neighbors.append(neighbor)
        return neighbors

    def get_cost(self, pos, map_):
        if map_[pos[0]][pos[1]] in self.cost_obstacles:
            return self.cost_obstacles[map_[pos[0]][pos[1]]]
        return 1  # Camino libre

    def a_star(self, map_, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic_function(start, goal)}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            for neighbor in self.get_neighbors(current, map_):
                tentative_g_score = g_score[current] + self.get_cost(neighbor, map_)
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic_function(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    
        return None

# Crear el mapa vacío (7x8)
map_ = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

cost_obstacles = [1]

map_instance = Map_(map_, cost_obstacles)
map_instance.print_map()

map_instance.get_obstacle()
print("Mapa actualizado:")
map_instance.print_map()

start_point = map_instance.get_start_point()
end_point = map_instance.get_end_point()
print("Mapa actualizado con puntos de inicio y salida:")
map_instance.print_map()

route_calculator = Route_calculator(cost_obstacles)
path = route_calculator.a_star(map_instance.map_, start_point, end_point)

if path:
    for paso in path:
        if map_[paso[0]][paso[1]] == 0:
            map_[paso[0]][paso[1]] = 'R'
    print("Mapa con la ruta más rápida:")
    map_instance.print_map()
else:
    print("No se encontró un camino desde el inicio hasta la meta.")
