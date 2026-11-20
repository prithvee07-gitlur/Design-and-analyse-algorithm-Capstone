import heapq
import random

class Parcel:
    def __init__(self, parcel_id, destination, weight, priority_score):
        self.parcel_id = parcel_id
        self.destination = destination
        self.weight = weight               
        self.priority_score = priority_score 
        
    def __repr__(self):
        return f"Parcel({self.parcel_id}, Dest: {self.destination}, Wt: {self.weight}, Pri: {self.priority_score})"

city_graph = {
    'Hub': {'A': 4, 'B': 2, 'C': 5},
    'A': {'Hub': 4, 'B': 1, 'D': 3},
    'B': {'Hub': 2, 'A': 1, 'C': 2, 'D': 4},
    'C': {'Hub': 5, 'B': 2, 'D': 1},
    'D': {'A': 3, 'B': 4, 'C': 1}
}

waiting_parcels = [
    Parcel(parcel_id="P1", destination="A", weight=3, priority_score=50),
    Parcel(parcel_id="P2", destination="C", weight=6, priority_score=40),
    Parcel(parcel_id="P3", destination="D", weight=2, priority_score=70),
    Parcel(parcel_id="P4", destination="B", weight=5, priority_score=30)
]

MAX_BAG_CAPACITY = 10

# --- PHASE 2: PACKAGE PRIORITIZATION AND BOX FILLING ---

# 1. The Sorting Algorithm (Merge Sort)
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
    # Sorting in DESCENDING order (highest priority score first)
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

# 2. Dynamic Programming: 0/1 Knapsack
def knapsack_box_filling(parcels, capacity):
    n = len(parcels)
    # Create a DP table filled with 0s. 
    # Rows = parcels, Cols = capacity from 0 to MAX_BAG_CAPACITY
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Build the DP table bottom-up
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            weight = parcels[i-1].weight
            value = parcels[i-1].priority_score
            
            if weight <= w:
                # Max of (including the parcel) vs (excluding the parcel)
                dp[i][w] = max(value + dp[i-1][w-weight], dp[i-1][w])
            else:
                # Parcel is too heavy for the current capacity, exclude it
                dp[i][w] = dp[i-1][w]
                
    # Traceback to find exactly which parcels were packed
    packed_parcels = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            packed_parcels.append(parcels[i-1])
            w -= parcels[i-1].weight
            
    return dp[n][capacity], packed_parcels

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    print("--- PHASE 2: Prioritization & Box Filling ---")
    
    # 1. Sort the parcels
    sorted_parcels = merge_sort_parcels(waiting_parcels)
    print("Sorted Parcels by Priority:")
    for p in sorted_parcels:
        print(f"  {p}")
        
    # 2. Apply DP Knapsack
    max_priority, packed = knapsack_box_filling(sorted_parcels, MAX_BAG_CAPACITY)
    print(f"\nOptimal Packing Plan (Max Capacity: {MAX_BAG_CAPACITY}):")
    print(f"Total Priority Score Achieved: {max_priority}")
    print("Parcels to Load:")
    for p in packed:
        print(f"  {p}")
