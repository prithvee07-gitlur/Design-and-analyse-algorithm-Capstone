# 📦 Mini-Courier Planner 🚚

### Intelligent Last-Mile Delivery Packing & Route Optimization Engine

[✨ Overview](#-overview) •
[🏗️ Architecture](#%EF%B8%8F-system-architecture) •
[🧠 Algorithms Explained](#-algorithms-explained) •
[📊 Visual Results](#-visual-results--screenshots) •
[🚀 Quick Start](#-quick-start) •
[🎓 Viva Cheatsheet](#-viva--complexity-cheatsheet)

## ✨ Overview

**Mini-Courier Planner** is an algorithmic Python engine that simulates the dispatch brain behind modern logistics and delivery platforms (like Zomato, Swiggy, and Amazon Logistics).

Given a batch of waiting parcels at a central hub, a courier bag with a strict weight limit, and a weighted city road map, the system automatically solves four classic computer science problems in one unified pipeline:

* 🗂️ **Prioritizes** incoming orders by urgency using **Merge Sort**.

* 🎒 **Optimizes Box Filling** to maximize priority value without exceeding capacity using **0/1 Knapsack Dynamic Programming**.

* 🗺️ **Finds Shortest Roads** between every intersection using **Dijkstra's Algorithm**.

* 🧭 **Plans the Delivery Sequence** across all drop-off points and returns to the Hub using **Nearest-Neighbor TSP Approximation**.

* 📈 **Benchmarks Scaling Performance** across Small, Medium, Large, and X-Large datasets and plots a **Matplotlib** comparison chart.

## 🏗️ System Architecture

The entire project is structured as a modular 4-phase algorithmic pipeline inside `courier_planner.py`:

```
flowchart TD
    A["📦 Waiting Parcels & Bag Capacity (Phase 1)"] --> B["🗂️ Merge Sort\nOrder by Priority Score (Phase 2A)"]
    B --> C["🎒 0/1 Knapsack DP\nSelect Optimal Parcel Subset (Phase 2B)"]
    C --> D["🗺️ Dijkstra's Algorithm\nCompute Shortest Road Paths (Phase 3A)"]
    D --> E["🚚 Nearest-Neighbor TSP\nSequence Drop-Offs & Return to Hub (Phase 3B)"]
    E --> F["📈 Multi-Scale Benchmarking\nRuntime Table & Matplotlib Chart (Phase 4)"]

    style A fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff
    style B fill:#1e293b,stroke:#a78bfa,stroke-width:2px,color:#fff
    style C fill:#1e293b,stroke:#34d399,stroke-width:2px,color:#fff
    style D fill:#1e293b,stroke:#fbbf24,stroke-width:2px,color:#fff
    style E fill:#1e293b,stroke:#fb7185,stroke-width:2px,color:#fff
    style F fill:#1e293b,stroke:#60a5fa,stroke-width:2px,color:#fff

```

### 🗺️ Sample City Road Network (`city_graph`)

The delivery network is modeled as an **undirected, positively weighted graph** stored as an **Adjacency List** ($O(V + E)$ space):

```
graph LR
    Hub(("🏢 Hub")) ---|4| A(("📍 A"))
    Hub ---|2| B(("📍 B"))
    Hub ---|5| C(("📍 C"))
    A ---|1| B
    A ---|3| D(("📍 D"))
    B ---|2| C
    B ---|4| D
    C ---|1| D

    style Hub fill:#2563eb,stroke:#fff,stroke-width:2px,color:#fff
    style A fill:#0f766e,stroke:#fff,color:#fff
    style B fill:#0f766e,stroke:#fff,color:#fff
    style C fill:#0f766e,stroke:#fff,color:#fff
    style D fill:#0f766e,stroke:#fff,color:#fff

```

## 🧠 Algorithms Explained

### 1️⃣ Phase 1 — Data Structures (`Parcel` & `city_graph`)

* **`Parcel` Class:** Encapsulates `parcel_id`, `destination`, `weight`, and `priority_score`.

* **Adjacency List (`dict` of `dict`s):** Fast $O(1)$ neighbor lookup and memory-efficient representation for sparse road maps.

| Parcel ID | Destination | Weight (units) | Priority Score | 
| ----- | ----- | ----- | ----- | 
| `P1` | `A` | 3 | 50 | 
| `P2` | `C` | 6 | 40 | 
| `P3` | `D` | 2 | 70 | 
| `P4` | `B` | 5 | 30 | 

> **Bag Capacity Limit:** `MAX_BAG_CAPACITY = 10` units.

### 2️⃣ Phase 2A — Package Prioritization (Merge Sort)

* **Why Merge Sort?** Unlike Quick Sort (which can degrade to $O(N^2)$), Merge Sort guarantees $O(N \log N)$ in best, average, and worst cases and preserves relative order (**stable sort**).

* **How it works:** Recursively divides the parcel list into halves until single elements remain, then merges them back in **descending order of `priority_score`**.

* **Sorted Output:** `P3 (70)` $\rightarrow$ `P1 (50)` $\rightarrow$ `P2 (40)` $\rightarrow$ `P4 (30)`.

### 3️⃣ Phase 2B — Optimal Box Filling (0/1 Knapsack Dynamic Programming)

* **Why Dynamic Programming?** A greedy strategy that picks the highest-priority parcels first might leave awkward leftover space. Because parcels cannot be split in half (`0/1`), Bottom-Up DP guarantees the **exact mathematical optimum**.

* **Recurrence Relation:**

$$
dp[i][w] = \begin{cases} dp[i-1][w] & \text{if } wt_i > w \\ \max\big(dp[i-1][w],\ val_i + dp[i-1][w - wt_i]\big) & \text{if } wt_i \le w \end{cases}
$$

* **Optimal Packing Plan:** Selects **`P3` + `P1` + `P4`** (Weight: **`10 / 10`**, Priority Score: **`150`**). Parcel `P2` is skipped because packing `P3 + P2` only yields a score of `110`.

| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | 
| **None** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 
| **P3** (Wt 2, Pri 70) | 0 | 0 | 70 | 70 | 70 | 70 | 70 | 70 | 70 | 70 | 70 | 
| **P1** (Wt 3, Pri 50) | 0 | 0 | 70 | 70 | 70 | 120 | 120 | 120 | 120 | 120 | 120 | 
| **P2** (Wt 6, Pri 40) | 0 | 0 | 70 | 70 | 70 | 120 | 120 | 120 | 120 | 120 | 120 | 
| **P4** (Wt 5, Pri 30) | 0 | 0 | 70 | 70 | 70 | 120 | 120 | 120 | 120 | 120 | **150** | 

### 4️⃣ Phase 3A — Individual Shortest Paths (Dijkstra's Algorithm)

* **Why Dijkstra?** Road distances are always non-negative. Using Python's binary min-heap (`heapq`), Dijkstra finds the shortest path from any source node to all other intersections in $O((V + E) \log V)$ time.

* **Path Reconstruction:** Maintains a `previous_nodes` dictionary so the exact turn-by-turn road path can be traced back.

| From Hub To | Shortest Distance | Turn-by-Turn Path | 
| ----- | ----- | ----- | 
| `B` | **2 units** | `Hub` $\rightarrow$ `B` | 
| `A` | **3 units** | `Hub` $\rightarrow$ `B` $\rightarrow$ `A` | 
| `C` | **4 units** | `Hub` $\rightarrow$ `B` $\rightarrow$ `C` | 
| `D` | **5 units** | `Hub` $\rightarrow$ `B` $\rightarrow$ `C` $\rightarrow$ `D` | 

### 5️⃣ Phase 3B — Overall Delivery Sequence (Nearest-Neighbor TSP)

* **Why an Approximation?** Exact TSP is **NP-Hard** ($O(K^2 \cdot 2^K)$ with Held-Karp DP), which becomes unusable as stops grow. The **Nearest-Neighbor Heuristic** runs in polynomial time by repeatedly querying Dijkstra from the courier's current position, traveling to the closest unvisited stop, and returning to the Hub once empty.

* **Required Stops:** `D`, `A`, `B`

* **Final Optimized Route:**

  > `Hub` $\rightarrow$ `B` *(drop P4)* $\rightarrow$ `A` *(drop P1)* $\rightarrow$ `D` *(drop P3)* $\rightarrow$ `C` $\rightarrow$ `B` $\rightarrow$ `Hub`

* **Total Distance Traveled:** **`11` units**

## 📊 Visual Results & Screenshots

### 📈 Phase 4: Algorithmic Runtime Scaling Chart

The benchmarking suite automatically generates connected random road networks and parcel datasets across four scales — **Small** (`10p, 10n`), **Medium** (`100p, 30n`), **Large** (`300p, 60n`), and **X-Large** (`600p, 100n`) — and exports the Matplotlib graph below:

### 🖥️ Console Execution Trace

### 🔍 Key Performance Observations

* ⚡ **Merge Sort** stays nearly flat across all scales due to its tight $O(N \log N)$ scaling.

* 🧱 **0/1 Knapsack DP** grows fastest on large inputs because its pseudo-polynomial complexity $O(N \cdot W)$ scales with *both* the number of parcels $N$ and the bag capacity $W$.

* 🛣️ **Dijkstra + Nearest-Neighbor TSP** scales smoothly across $K$ unique delivery stops and $V$ graph nodes, staying fast enough for real-time dispatch.

### 💡 Future Optimization Ideas

1. **1D DP Array Optimization:** Compress Knapsack memory from $O(N \cdot W)$ to $O(W)$ when only the maximum score is required.

2. **All-Pairs Path Caching:** Precompute shortest paths once between delivery stops rather than invoking Dijkstra inside each TSP loop iteration.

3. **2-Opt Local Search:** Post-process the Nearest-Neighbor route by uncrossing intersecting edges to tighten total travel distance.

4. **Multi-Rider VRP:** Extend the engine to coordinate a fleet of couriers with strict delivery time windows.

## 📁 Project Structure

```
Mini-Courier-Planner/
├── 🐍 courier_planner.py       # Complete integrated Python code (Phases 1 to 4)
├── 📈 runtime_comparison.png   # Auto-generated Matplotlib performance chart
├── 🖥️ terminal_output.png      # Console execution screenshot (Phase 5 evidence)
├── 📄 REPORT.md                # Formal Academic Capstone Report & Documentation
└── 📘 README.md                # Visual GitHub Project Overview (this file)

```

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have **Python 3.8+** installed on your machine.

### 2. Clone the Repository

```
git clone https://github.com/<your-username>/Mini-Courier-Planner.git
cd Mini-Courier-Planner

```

### 3. Install Dependencies

```
pip install matplotlib

```

### 4. Run the Application

```
python courier_planner.py

```

Running the script will:

1. Print the sorted parcel list, full 0/1 Knapsack DP table, and optimal packing plan.

2. Print individual Dijkstra shortest paths from `Hub` and the final Nearest-Neighbor TSP delivery route.

3. Execute multi-scale benchmarks, display the runtime table, and save **`runtime_comparison.png`** automatically.

## 🎓 Viva & Complexity Cheatsheet

| Algorithm | Purpose in Project | Time Complexity | Space Complexity | 
| ----- | ----- | ----- | ----- | 
| **Merge Sort** | Sort waiting parcels by priority | $O(N \log N)$ | $O(N)$ | 
| **0/1 Knapsack (DP)** | Choose optimal parcels within capacity $W$ | $O(N \cdot W)$ | $O(N \cdot W)$ | 
| **Dijkstra's Algorithm** | Find shortest path between intersections | $O((V + E) \log V)$ | $O(V)$ | 
| **Nearest-Neighbor TSP** | Order drop-off stops and return to Hub | $O(K \cdot (V + E) \log V)$ | $O(V)$ | 

1. **Why not use Greedy for box filling instead of 0/1 Knapsack DP?**
   Greedy only guarantees an optimal result for *Fractional* Knapsack (where items can be cut into pieces). Real courier parcels are indivisible, so Dynamic Programming is required to guarantee the global optimum.

2. **Why does Dijkstra require non-negative edge weights?**
   Once Dijkstra pops a node from the min-heap, it assumes no shorter path to that node can exist later. Negative edges break this greedy invariant (requiring Bellman-Ford instead).

3. **Why did you use Nearest-Neighbor instead of exact TSP?**
   Exact TSP is NP-Hard and grows exponentially ($O(K^2 \cdot 2^K)$). Nearest-Neighbor runs in polynomial time, making it practical for real-world delivery routing at the cost of a small approximation gap.