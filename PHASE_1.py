class Parcel:
    def __init__(self, parcel_id, destination, weight, priority_score):
        self.parcel_id = parcel_id
        self.destination = destination
        self.weight = weight               # Used as the "weight" for the Knapsack algorithm
        self.priority_score = priority_score # Used as the "value" for the Knapsack algorithm
        
    def __repr__(self):
        return f"Parcel({self.parcel_id}, Dest: {self.destination}, Wt: {self.weight}, Pri: {self.priority_score})"

# The City Map (Graph)
# The keys are locations. The inner dictionaries show connected locations and the distance to them.
city_graph = {
    'Hub': {'A': 4, 'B': 2, 'C': 5},
    'A': {'Hub': 4, 'B': 1, 'D': 3},
    'B': {'Hub': 2, 'A': 1, 'C': 2, 'D': 4},
    'C': {'Hub': 5, 'B': 2, 'D': 1},
    'D': {'A': 3, 'B': 4, 'C': 1}
}

# The parcels currently sitting at the Hub waiting to be delivered
waiting_parcels = [
    Parcel(parcel_id="P1", destination="A", weight=3, priority_score=50),
    Parcel(parcel_id="P2", destination="C", weight=6, priority_score=40),
    Parcel(parcel_id="P3", destination="D", weight=2, priority_score=70),
    Parcel(parcel_id="P4", destination="B", weight=5, priority_score=30)
]

# The delivery bag has a maximum weight limit
MAX_BAG_CAPACITY = 10