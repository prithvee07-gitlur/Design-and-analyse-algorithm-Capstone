"""
Mini-Courier Planner
Combines Merge Sort, 0/1 Knapsack DP, Dijkstra's Algorithm,
Nearest-Neighbor TSP, and runtime benchmarking.
"""

import heapq
import random
import time
import matplotlib.pyplot as plt


# --- Data Models & Sample Inputs ---

class Parcel:
    def __init__(self, parcel_id, destination, weight, priority_score):
        self.parcel_id = parcel_id
        self.destination = destination
        self.weight = weight
        self.priority_score = priority_score

    def __repr__(self):
        return (
            f"Parcel({self.parcel_id}, Dest: {self.destination}, "
            f"Wt: {self.weight}, Pri: {self.priority_score})"
        )


city_graph = {
    'Hub': {'A': 4, 'B': 2, 'C': 5},
    'A': {'Hub': 4, 'B': 1, 'D': 3},
    'B': {'Hub': 2, 'A': 1, 'C': 2, 'D': 4},
    'C': {'Hub': 5, 'B': 2, 'D': 1},
    'D': {'A': 3, 'B': 4, 'C': 1},
}

waiting_parcels = [
    Parcel("P1", "A", 3, 50),
    Parcel("P2", "C", 6, 40),
    Parcel("P3", "D", 2, 70),
    Parcel("P4", "B", 5, 30),
]

MAX_BAG_CAPACITY = 10


# --- Sorting (Merge Sort) ---

def merge_sort_parcels(parcels):
    if len(parcels) <= 1:
        return parcels

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])
    return merge(left, right)


def merge(left, right):
    sorted_list = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i].priority_score >= right[j].priority_score:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list


# --- Box Filling (0/1 Knapsack DP) ---

def knapsack_box_filling(parcels, capacity):
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1].weight
        value = parcels[i - 1].priority_score
        for w in range(1, capacity + 1):
            if weight <= w:
                dp[i][w] = max(value + dp[i - 1][w - weight], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    packed_parcels = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            packed_parcels.append(parcels[i - 1])
            w -= parcels[i - 1].weight

    packed_parcels.reverse()
    return dp[n][capacity], packed_parcels, dp


# --- Routing (Dijkstra & Nearest-Neighbor TSP) ---

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_dist > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            dist = current_dist + weight
            if dist < distances[neighbor]:
                distances[neighbor] = dist
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (dist, neighbor))

    return distances, previous_nodes


def get_shortest_path(previous_nodes, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()
    return path


def nearest_neighbor_tsp(graph, start_hub, parcels_to_deliver):
    unvisited = {p.destination for p in parcels_to_deliver}
    unvisited.discard(start_hub)

    current_location = start_hub
    overall_route = [start_hub]
    total_distance = 0

    while unvisited:
        distances, previous_nodes = dijkstra(graph, current_location)
        next_stop = min(unvisited, key=lambda dest: distances[dest])

        path_to_next = get_shortest_path(previous_nodes, next_stop)
        overall_route.extend(path_to_next[1:])
        total_distance += distances[next_stop]

        current_location = next_stop
        unvisited.remove(next_stop)

    if current_location != start_hub:
        distances, previous_nodes = dijkstra(graph, current_location)
        return_path = get_shortest_path(previous_nodes, start_hub)
        overall_route.extend(return_path[1:])
        total_distance += distances[start_hub]

    return overall_route, total_distance


# --- Performance Benchmarking ---

def generate_test_data(num_parcels, num_nodes, seed=42):
    random.seed(seed)
    nodes = ['Hub'] + [f'N{i}' for i in range(1, num_nodes)]
    graph = {node: {} for node in nodes}

    for i in range(1, num_nodes):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]
        dist = random.randint(1, 15)
        graph[u][v] = dist
        graph[v][u] = dist

    for _ in range(num_nodes * 2):
        u, v = random.sample(nodes, 2)
        dist = random.randint(1, 20)
        graph[u][v] = dist
        graph[v][u] = dist

    destinations = nodes[1:]
    parcels = [
        Parcel(
            f"T{i + 1}",
            random.choice(destinations),
            random.randint(1, 10),
            random.randint(10, 100),
        )
        for i in range(num_parcels)
    ]
    return graph, parcels


def run_benchmarks():
    configs = [
        ("Small\n(10p, 10n)", 10, 25, 10),
        ("Medium\n(100p, 30n)", 100, 100, 30),
        ("Large\n(300p, 60n)", 300, 250, 60),
        ("X-Large\n(600p, 100n)", 600, 400, 100),
    ]

    labels, sort_times, knap_times, route_times = [], [], [], []

    print("\n--- Runtime Benchmark ---")
    print(f"{'Dataset':<20} | {'Merge Sort (ms)':<16} | {'Knapsack (ms)':<14} | {'Dijkstra+TSP (ms)':<17}")
    print("-" * 76)

    for label, n_parcels, cap, n_nodes in configs:
        graph, parcels = generate_test_data(n_parcels, n_nodes)

        t0 = time.perf_counter()
        sorted_p = merge_sort_parcels(parcels)
        t_sort = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        _, packed_p, _ = knapsack_box_filling(sorted_p, cap)
        t_knap = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        nearest_neighbor_tsp(graph, 'Hub', packed_p)
        t_route = (time.perf_counter() - t0) * 1000

        labels.append(label)
        sort_times.append(t_sort)
        knap_times.append(t_knap)
        route_times.append(t_route)

        print(f"{label.replace(chr(10), ' '):<20} | {t_sort:<16.3f} | {t_knap:<14.3f} | {t_route:<17.3f}")

    plt.figure(figsize=(9, 5))
    plt.plot(labels, sort_times, marker='o', linewidth=2, label='Merge Sort O(N log N)')
    plt.plot(labels, knap_times, marker='s', linewidth=2, label='0/1 Knapsack DP O(N * W)')
    plt.plot(labels, route_times, marker='^', linewidth=2, label='Dijkstra + TSP O(K*(V+E) log V)')
    plt.title('Mini-Courier Planner: Runtime Comparison')
    plt.xlabel('Dataset Scale (Parcels, Nodes)')
    plt.ylabel('Execution Time (ms)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig('runtime_comparison.png', dpi=150)
    print("\nChart saved as 'runtime_comparison.png'")
    plt.show()


# --- Main Execution ---

if __name__ == "__main__":
    sorted_parcels = merge_sort_parcels(waiting_parcels)
    max_priority, packed, dp_table = knapsack_box_filling(sorted_parcels, MAX_BAG_CAPACITY)

    print("--- Sorted Parcels ---")
    for p in sorted_parcels:
        print(f"  {p}")

    print(f"\n--- DP Table (Capacity 0..{MAX_BAG_CAPACITY}) ---")
    header = "Item | " + " ".join(f"{w:>3}" for w in range(MAX_BAG_CAPACITY + 1))
    print(header)
    print("-" * len(header))
    for i, row in enumerate(dp_table):
        label = "None" if i == 0 else f"{sorted_parcels[i - 1].parcel_id:<4}"
        print(f"{label} | " + " ".join(f"{val:>3}" for val in row))

    total_wt = sum(p.weight for p in packed)
    print(f"\n--- Packing Plan ({total_wt}/{MAX_BAG_CAPACITY} weight | Score: {max_priority}) ---")
    for p in packed:
        print(f"  {p}")

    print("\n--- Shortest Paths from Hub ---")
    hub_dists, hub_prev = dijkstra(city_graph, 'Hub')
    for node in sorted(city_graph):
        if node != 'Hub':
            path = get_shortest_path(hub_prev, node)
            print(f"  Hub -> {node}: {hub_dists[node]} units | {' -> '.join(path)}")

    final_route, total_dist = nearest_neighbor_tsp(city_graph, 'Hub', packed)
    print(f"\n--- Delivery Route ---")
    print(f"  Stops    : {[p.destination for p in packed]}")
    print(f"  Sequence : {' -> '.join(final_route)}")
    print(f"  Distance : {total_dist} units")

    run_benchmarks()