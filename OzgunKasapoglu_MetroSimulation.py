from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Station:
    def __init__(self, idx: str, name: str, line: str):
        self.idx = idx
        self.name = name
        self.line = line
        self.neighbors: List[Tuple['Station', int]] = []  # (station, time) tuples

    def add_neighbors(self, station: 'Station', time: int):
        self.neighbors.append((station, time))

class MetroNetwork:
    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.lines: Dict[str, List[Station]] = defaultdict(list)

    def add_station(self, idx: str, name: str, line: str) -> None:
        if id not in self.stations:
            station = Station(idx, name, line)
            self.stations[idx] = station
            self.lines[line].append(station)

    def add_connection(self, station1_id: str, station2_id: str, time: int) -> None:
        station1 = self.stations[station1_id]
        station2 = self.stations[station2_id]
        station1.add_neighbors(station2, time)
        station2.add_neighbors(station1, time)
    
    def find_the_least_transfer(self, start_id: str, target_id: str) -> Optional[List[Station]]:
        if start_id not in self.stations or target_id not in self.stations:
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]

        queue = deque()
        queue.append((start, [start]))
        visited = set()
        visited.add(start.idx)

        while queue:
            current_station, path = queue.popleft()
            if current_station.idx == target.idx:
                return path

            for neighbor, _ in current_station.neighbors:
                if neighbor.idx not in visited:
                    visited.add(neighbor.idx)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))

        return None


    def find_fastest_route(self, start_id: str, target_id: str) -> Optional[Tuple[List[Station], int]]:
        if start_id not in self.stations or target_id not in self.stations:
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]

        heap = []
        heapq.heappush(heap, (0, start.idx, start, [start]))  # Added station ID as tiebreaker
        best_times = {start.idx: 0}

        while heap:
            current_time, _, current_station, path = heapq.heappop(heap)

            if current_station.idx == target.idx:
                return (path, current_time)

            if current_time > best_times.get(current_station.idx, float('inf')):
                continue

            for neighbor, time in current_station.neighbors:
                new_time = current_time + time
                if neighbor.idx not in best_times or new_time < best_times[neighbor.idx]:
                    best_times[neighbor.idx] = new_time
                    new_path = path + [neighbor]
                    heapq.heappush(heap, (new_time, neighbor.idx, neighbor, new_path))  # Include ID

        return None

# Example Use
if __name__ == "__main__":
    metro = MetroNetwork()
    
    # Adding Stations

    # Red Line
    metro.add_station("K1", "Kizilay", "Red Line")
    metro.add_station("K2", "Ulus", "Red Line")
    metro.add_station("K3", "Demetevler", "Red Line")
    metro.add_station("K4", "OSB", "Red Line")
    
    # Blue Line
    metro.add_station("M1", "ASTI", "Blue Line")
    metro.add_station("M2", "Kizilay", "Blue Line")  # Transfer point
    metro.add_station("M3", "Sihhiye", "Blue Line")
    metro.add_station("M4", "Gar", "Blue Line")
    
    # Orange Line
    metro.add_station("T1", "Batıkent", "Orange Line")
    metro.add_station("T2", "Demetevler", "Orange Line")  # Transfer point
    metro.add_station("T3", "Gar", "Orange Line")  # Transfer point
    metro.add_station("T4", "Kecioren", "Orange Line")
    
    # Adding connections

    # Red Line connections
    metro.add_connection("K1", "K2", 4)  # Kizilay -> Ulus
    metro.add_connection("K2", "K3", 6)  # Ulus -> Demetevler
    metro.add_connection("K3", "K4", 8)  # Demetevler -> OSB
    
    # Blue Line connections
    metro.add_connection("M1", "M2", 5)  # ASTI -> Kizilay
    metro.add_connection("M2", "M3", 3)  # Kizilay -> Sihhiye
    metro.add_connection("M3", "M4", 4)  # Sihhiye -> Gar
    
    # Orange Line connections
    metro.add_connection("T1", "T2", 7)  # Batikent -> Demetevler
    metro.add_connection("T2", "T3", 9)  # Demetevler -> Gar
    metro.add_connection("T3", "T4", 5)  # Gar -> Kecioren
    
    # Line transfer connections (same station different lines)
    metro.add_connection("K1", "M2", 2)  # Kizilay transfer
    metro.add_connection("K3", "T2", 3)  # Demetevler transfer
    metro.add_connection("M4", "T3", 2)  # Gar transfer
    
    # Test scenarios
    print("\n=== Test Scenarios ===")
    
    # Scenario 1: From ASTI to OSB
    print("\n1. From ASTI to OSB:")
    route = metro.find_the_least_transfer("M1", "K4")
    if route:
        print("Route with the least transfers:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("M1", "K4")
    if result:
        route, time = result
        print(f"Fastest Route ({time} minutes):", " -> ".join(i.name for i in route))
    
    # Scenario 2: From Batikent to Kecioren
    print("\n2. From Batikent to Kecioren:")
    route = metro.find_the_least_transfer("T1", "T4")
    if route:
        print("Route with the least transfers:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("T1", "T4")
    if result:
        route, time = result
        print(f"Fastest Route ({time} minutes):", " -> ".join(i.name for i in route))
    
    # Scenario 3: From Kecioren to ASTI
    print("\n3. From Kecioren to ASTI:")
    route = metro.find_the_least_transfer("T4", "M1")
    if route:
        print("Route with the least transfers:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("T4", "M1")
    if result:
        route, time = result
        print(f"Fastest Route ({time} minutes):", " -> ".join(i.name for i in route))