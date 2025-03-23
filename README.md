# Metro Route Optimization Simulator 🚇

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

A Python simulation for finding optimal metro routes using:
- **BFS Algorithm** for routes with **least transfers** 🔄
- **A*** **Algorithm** for **fastest routes** ⏱️

Developed for the Global AI Hub x Akbank - Python & AI Bootcamp.

## Features
- 🗺️ Graph-based metro network modeling
- 🚉 Real-world inspired test scenarios (Ankara Metro)
- 📊 Two distinct optimization strategies
- 🚦 Automatic transfer handling between lines

## Technologies & Libraries
- **Algorithms**: BFS, A* (Dijkstra-inspired)
- **Python Core**: `collections.deque` (BFS), `heapq` (A*)
- **Tools**: GitHub, PyCharm

## How It Works
### Algorithms
| Algorithm  | Use Case         | Complexity  | Key Feature                       |
|------------|------------------|-------------|-----------------------------------|
| **BFS**    | Least Transfers  | O(V + E)    | Guarantees minimum station changes|
| **A***     | Fastest Route    | O(E log V)  | Optimizes for travel time         |

#### Complexity Terms
- **V**: Number of stations (vertices) in the metro network.
- **E**: Number of connections (edges) between stations.

#### Why These Algorithms?
- **BFS** explores all stations at current depth before moving deeper, ensuring minimal transfers.
- **A*** prioritizes paths with the lowest accumulated time using a priority queue.

### Transfer Handling
Transfers between lines (e.g., Kızılay Red Line ↔ Kızılay Blue Line) are treated as regular connections with 2-minute transfer time.

## Example Usage
```python
# Initialize metro network
metro = MetroNetwork()

# Add stations (ID, Name, Line)
metro.add_station("A1", "Alpha", "Line Red")
metro.add_station("A2", "Central Hub", "Line Red")  # Transfer station
metro.add_station("A3", "Omega", "Line Red")

metro.add_station("B1", "Central Hub", "Line Blue")  # Transfer station (same name, different line)
metro.add_station("B2", "Downtown", "Line Blue")

# Create connections (time in minutes)
metro.add_connection("A1", "A2", 3)  # Line Red: Alpha → Central Hub (3 mins)
metro.add_connection("A2", "A3", 5)  # Line Red: Central Hub → Omega (5 mins)
metro.add_connection("B1", "B2", 4)  # Line Blue: Central Hub → Downtown (4 mins)

# Add transfer between lines (same station, different lines)
metro.add_connection("A2", "B1", 2)  # Transfer: Line Red ↔ Line Blue (2 mins)

# Find routes
print("1. Least transfers from Alpha to Downtown:")
route = metro.find_the_least_transfer("A1", "B2")
if route:
    print(" → ".join(station.name for station in route))

print("\n2. Fastest route from Omega to Downtown:")
result = metro.find_fastest_route("A3", "B2")
if result:
    route, time = result
    print(f"{' → '.join(station.name for station in route)} ({time} minutes)")

# Output
# 1. Least transfers from Alpha to Downtown:
# Alpha → Central Hub → Central Hub → Downtown

# 2. Fastest route from Omega to Downtown:
# Omega → Central Hub → Central Hub → Downtown (11 minutes)

```
## Installation & Usage
1. Clone repository:
```bash
git clone https://github.com/OzgunKasapoglu/MetroSimulation.git
```
2. Run simulation:
```bash
python OzgunKasapoglu_MetroSimulation.py
```
## Future Improvements
- 🖥️ **Interactive GUI**: Build a visual interface (e.g., Tkinter/PyQt) to display metro lines and routes dynamically.  
- 📡 **Real-Time Data**: Integrate live delays or congestion updates to adjust route calculations.  
- 🗺️ **Geospatial Mapping**: Plot stations on a real map using APIs like Google Maps or OpenStreetMap.  
- 📦 **JSON/YAML Configuration**: Allow metro networks to be defined via config files for easy scalability.  
- 🤖 **Machine Learning**: Predict optimal routes based on historical passenger data or peak hours.  
- 🌐 **Web App Deployment**: Convert the project into a Flask/Django web application for broader access.   
- 🔋 **Energy Efficiency Mode**: Optimize routes for reduced energy consumption (e.g., fewer stops).  
- 🔄 **API Integration**: Connect to public transit APIs for hybrid metro/bus route planning.  
- ♿ **Accessibility Features**: Highlight routes with elevator/ramp access for disabled passengers.  
