"""
Metro Route Optimization System
===============================
This module provides a simulation for finding optimal metro routes using:
- Breadth-First Search (BFS) for least transfers
- A* Algorithm (Dijkstra's variation) for fastest routes

Author: Özgün Kasapoglu
"""

from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Station:
    """Represents a metro station with connections to other stations.
    
    Attributes:
        idx (str): Unique identifier for the station
        name (str): Human-readable station name
        line (str): Metro line name
        neighbors (List[Tuple[Station, int]]): Connected stations with travel times
    """
    def __init__(self, idx: str, name: str, line: str):
        """Initialize a metro station."""
        self.idx = idx
        self.name = name
        self.line = line
        self.neighbors: List[Tuple['Station', int]] = []

    def add_neighbors(self, station: 'Station', time: int):
        """Add a bidirectional connection to another station with travel time."""
        self.neighbors.append((station, time))

class MetroNetwork:
    """Represents the complete metro network with route finding capabilities."""
    def __init__(self):
        """Initialize an empty metro network."""
        self.stations: Dict[str, Station] = {}
        self.lines: Dict[str, List[Station]] = defaultdict(list)

    def add_station(self, idx: str, name: str, line: str) -> None:
        """Add a new station to the network.
        
        Args:
            idx: Unique station identifier
            name: Display name of the station
            line: Metro line name
        """
        if idx not in self.stations:  # Prevent duplicate stations
            station = Station(idx, name, line)
            self.stations[idx] = station
            self.lines[line].append(station)

    def add_connection(self, station1_id: str, station2_id: str, time: int) -> None:
        """Create a bidirectional connection between two stations.
        
        Args:
            station1_id: ID of first station
            station2_id: ID of second station
            time: Travel time in minutes
        """
        station1 = self.stations[station1_id]
        station2 = self.stations[station2_id]
        station1.add_neighbors(station2, time)
        station2.add_neighbors(station1, time)
    
    def find_the_least_transfer(self, start_id: str, target_id: str) -> Optional[List[Station]]:
        """Find route with minimum transfers using BFS algorithm.
        
        Args:
            start_id: Starting station ID
            target_id: Destination station ID
            
        Returns:
            List of stations in path order or None if no path exists
        """
        # Validate station existence
        if start_id not in self.stations or target_id not in self.stations:
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]

        # BFS initialization with (current station, path)
        queue = deque()
        queue.append((start, [start]))
        visited = set()
        visited.add(start.idx)

        while queue:
            current_station, path = queue.popleft()
            
            # Early exit if target found
            if current_station.idx == target.idx:
                return path

            # Explore all neighboring stations
            for neighbor, _ in current_station.neighbors:
                if neighbor.idx not in visited:
                    visited.add(neighbor.idx)
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))

        return None

    def find_fastest_route(self, start_id: str, target_id: str) -> Optional[Tuple[List[Station], int]]:
        """Find fastest route using Dijkstra's algorithm variation.
        
        Args:
            start_id: Starting station ID
            target_id: Destination station ID
            
        Returns:
            Tuple containing (path, total_time) or None if no path exists
        """
        # Validate station existence
        if start_id not in self.stations or target_id not in self.stations:
            return None

        start = self.stations[start_id]
        target = self.stations[target_id]

        # Priority queue: (total_time, station_id, current_station, path)
        heap = []
        heapq.heappush(heap, (0, start.idx, start, [start]))
        best_times = {start.idx: 0}  # Track best known times to stations

        while heap:
            current_time, _, current_station, path = heapq.heappop(heap)

            # Return when target is reached
            if current_station.idx == target.idx:
                return (path, current_time)

            # Skip if better path already exists
            if current_time > best_times.get(current_station.idx, float('inf')):
                continue

            # Explore all neighbors
            for neighbor, time in current_station.neighbors:
                new_time = current_time + time
                # Update if new path is better than known paths
                if neighbor.idx not in best_times or new_time < best_times[neighbor.idx]:
                    best_times[neighbor.idx] = new_time
                    new_path = path + [neighbor]
                    heapq.heappush(heap, (new_time, neighbor.idx, neighbor, new_path))

        return None

# Example Usage ----------------------------------------------------------------
if __name__ == "__main__":
    """Main execution block with sample metro network and test scenarios."""
    metro = MetroNetwork()
    
    # ===== Station Setup =====
    # Red Line Stations
    metro.add_station("K1", "Kizilay", "Red Line")  # Transfer point
    metro.add_station("K2", "Ulus", "Red Line")
    metro.add_station("K3", "Demetevler", "Red Line")  # Transfer point
    metro.add_station("K4", "OSB", "Red Line")
    
    # Blue Line Stations
    metro.add_station("M1", "ASTI", "Blue Line")
    metro.add_station("M2", "Kizilay", "Blue Line")  # Transfer point
    metro.add_station("M3", "Sihhiye", "Blue Line")
    metro.add_station("M4", "Gar", "Blue Line")  # Transfer point
    
    # Orange Line Stations
    metro.add_station("T1", "Batıkent", "Orange Line")
    metro.add_station("T2", "Demetevler", "Orange Line")  # Transfer point
    metro.add_station("T3", "Gar", "Orange Line")  # Transfer point
    metro.add_station("T4", "Kecioren", "Orange Line")
    
    # ===== Connection Setup =====
    # Intra-line connections
    metro.add_connection("K1", "K2", 4)  # Red Line
    metro.add_connection("K2", "K3", 6)
    metro.add_connection("K3", "K4", 8)
    
    metro.add_connection("M1", "M2", 5)  # Blue Line
    metro.add_connection("M2", "M3", 3)
    metro.add_connection("M3", "M4", 4)
    
    metro.add_connection("T1", "T2", 7)  # Orange Line
    metro.add_connection("T2", "T3", 9)
    metro.add_connection("T3", "T4", 5)
    
    # Inter-line transfers
    metro.add_connection("K1", "M2", 2)  # Kizilay transfer
    metro.add_connection("K3", "T2", 3)  # Demetevler transfer
    metro.add_connection("M4", "T3", 2)  # Gar transfer
    
    # ===== Test Execution =====
    print("\n=== Test Scenarios ===")
    
    # Scenario 1: Cross-line journey with a transfer
    print("\n1. From ASTI to OSB:")
    route = metro.find_the_least_transfer("M1", "K4")
    if route:
        print("Route with the least transfers:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("M1", "K4")
    if result:
        route, time = result
        print(f"Fastest Route ({time} minutes):", " -> ".join(i.name for i in route))
    
    # Scenario 2: Single-line journey
    print("\n2. From Batikent to Kecioren:")
    route = metro.find_the_least_transfer("T1", "T4")
    if route:
        print("Route with the least transfers:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("T1", "T4")
    if result:
        route, time = result
        print(f"Fastest Route ({time} minutes):", " -> ".join(i.name for i in route))
    
    # Scenario 3: Journey with multiple transfers
    print("\n3. From Kecioren to ASTI:")
    route = metro.find_the_least_transfer("T4", "M1")
    if route:
        print("Route with the least transfers:", " -> ".join(i.name for i in route))
    
    result = metro.find_fastest_route("T4", "M1")
    if result:
        route, time = result
        print(f"Fastest Route ({time} minutes):", " -> ".join(i.name for i in route))
