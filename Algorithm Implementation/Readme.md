# 🤖 Algorithm Implementation in C++

This repository contains implementations of various AI and graph search algorithms written in **C++**. Each algorithm is explained with examples and is suitable for **educational purposes**, learning, or use as components in larger AI-based projects.

---

## 📚 Table of Contents

- [Search Algorithms](#search-algorithms)
- [Game Theory Algorithms](#game-theory-algorithms)
- [Optimization Algorithms](#optimization-algorithms)
- [Usage](#usage)
- [Compilation](#compilation)

---

## 🔍 Search Algorithms

### 1. Breadth-First Search (BFS)

**📄 File:** `breadth_first_search.cpp`

#### 🔧 How It Works:

- Explores nodes **level by level** starting from the source node.
- Uses a **queue (FIFO)** structure to keep track of nodes to be explored.
- **Guarantees** the shortest path in **unweighted** graphs.

#### 💡 Applications:

- Finding shortest path in unweighted graphs.
- Level-order traversal in trees.
- Social networks (e.g., finding shortest connection path).
- Web crawling.
- GPS navigation systems.

#### 📈 Complexity:

- **Time Complexity:** O(V + E)  
  (where V = number of vertices, E = number of edges)
- **Space Complexity:** O(V)  
  (for maintaining the queue and visited array)

#### 🧪 Input & Output Example:

<img width="496" height="195" alt="Image" src="https://github.com/user-attachments/assets/b140e54e-b5ae-43e3-97b4-883a28fcf57c" />



### 2. Depth-First Search (DFS)

**📄 File:** `depth_first_search.cpp`

#### 🔧 How It Works:

- Explores **as far as possible** along each branch before **backtracking**.
- Can be implemented using **stack (LIFO)** or **recursion**.
- **Does not guarantee** the shortest path in graphs.

#### 💡 Applications:

- Topological sorting
- Detecting cycles in a graph
- Solving puzzles (e.g., maze solving)
- Finding connected components
- Pathfinding in 2D/3D game development

#### 📈 Complexity:

- **Time Complexity:** O(V + E)  
  (where V = number of vertices, E = number of edges)
- **Space Complexity:** O(V)  
  (due to recursion stack or explicit stack used during traversal)

#### 🧪 Input & Output Example:

<img width="515" height="236" alt="Image" src="https://github.com/user-attachments/assets/7eb49f08-3742-4cc2-803b-49995b19736c" />



### 3. Depth-Limited Search (DLS)

**📄 File:** `depth_limited_search.cpp`

#### 🔧 How It Works:

- A variation of Depth-First Search with a **predetermined depth limit**.
- Helps avoid **infinite loops** in **infinite or cyclic** state spaces.
- Stops exploring further when the **depth limit** is reached.

#### 💡 Applications:

- Game tree exploration with **limited lookahead**
- Search problems with **resource constraints** (e.g., time or memory)
- Acts as a **building block** for Iterative Deepening Search (IDS)

#### 📈 Complexity:

- **Time Complexity:** O(b^l)  
  (where **b** = branching factor, **l** = depth limit)
- **Space Complexity:** O(l)  
  (since it behaves like DFS and stores nodes up to the limited depth)

#### 🧪 Input & Output Example:

<img width="508" height="266" alt="Image" src="https://github.com/user-attachments/assets/a1f839f0-d918-42f9-98f4-576629125f64" />



### 4. Iterative Deepening Search (IDS)

**📄 File:** `iterative_deepening_search.cpp`

#### 🔧 How It Works:

- Combines the advantages of **Depth-First Search (DFS)** and **Breadth-First Search (BFS)**.
- Performs **Depth-Limited Search** repeatedly, increasing the depth limit with each iteration.
- Continues until the solution is found or the maximum depth is reached.

#### 💡 Applications:

- Game playing where the **optimal move** is needed
- Search problems where the **solution depth is unknown**
- Suitable for **memory-constrained environments** due to DFS-like space usage

#### 📈 Complexity:

- **Time Complexity:** O(b^d)  
  (where **b** = branching factor, **d** = depth of the shallowest solution)
- **Space Complexity:** O(d)  
  (stores only one path at a time like DFS)

#### 🧪 Input & Output Example:

<img width="500" height="342" alt="Image" src="https://github.com/user-attachments/assets/526d4d79-c481-4cad-937a-7504c3e00a21" />



### 5. Best-First Search

**📄 Files:**  
- `best_first_search.cpp`  
- `best_first_search_dry_run.cpp` *(for step-by-step explanation or dry run)*

#### 🔧 How It Works:

- Uses a **heuristic function** to evaluate and prioritize nodes.
- Always explores the node that appears to be the **most promising** based on the heuristic value.
- Maintains a **priority queue** to select nodes with the lowest heuristic cost first.

#### 💡 Applications:

- Route finding with heuristics (e.g., shortest path on maps)
- Puzzle solving (like **8-puzzle**, **15-puzzle**)
- AI-based game playing
- Pathfinding in **robotics** and automated navigation systems

#### 📈 Complexity:

- **Time Complexity:** O(b^m)  
  (where **b** = branching factor, **m** = maximum depth of the search space)
- **Space Complexity:** O(b^m)  
  (due to priority queue storing frontier nodes)

#### 🧪 Input & Output Example:

<img width="498" height="288" alt="Image" src="https://github.com/user-attachments/assets/b866c138-26df-4563-af06-c2213000fecd" />



### 6. A* Search Algorithm

**📄 File:** `a_star.cpp`

#### 🔧 How It Works:

- Combines the **actual cost** from the start node `g(n)` and the **heuristic estimate** to the goal `h(n)`.
- Evaluates each node using the function:  
  **f(n) = g(n) + h(n)**
- Guarantees the **optimal path** if the heuristic is **admissible** (never overestimates the actual cost to the goal).

#### 💡 Applications:

- **GPS navigation** and route planning
- **Pathfinding** in video games and simulation
- **Robot motion planning**
- **Network routing protocols** (e.g., OSPF)
- **Puzzle solving** (e.g., 8-puzzle, sliding puzzles)

#### 📈 Complexity:

- **Time Complexity:** O(b^d) in the worst case  
  (where **b** = branching factor, **d** = depth of the solution)
- **Space Complexity:** O(b^d)  
  (due to storing all generated nodes in memory)

#### 🧪 Input & Output Example:

<img width="567" height="305" alt="Image" src="https://github.com/user-attachments/assets/1cf60eab-e8b3-40ee-aef4-a34c6feeb9d6" />




### 7. Bidirectional Search

**📄 Files:**  
- `bidirectional.cpp`  
- `bidirectional_search_path.cpp` *(to trace the actual path between start and goal)*

#### 🔧 How It Works:

- Performs two simultaneous searches:  
  one **forward** from the start node and one **backward** from the goal node.
- The searches **meet in the middle**, drastically reducing the number of explored nodes.
- Especially effective when both the start and goal nodes are known.

#### 💡 Applications:

- Finding the **shortest path** in large-scale graphs
- **Social network analysis** (e.g., finding degrees of separation)
- **Bioinformatics** (e.g., sequence alignment)
- **Database query optimization**

#### 📈 Complexity:

- **Time Complexity:** O(b<sup>d/2</sup>)  
  (where **b** = branching factor, **d** = distance between start and goal)
- **Space Complexity:** O(b<sup>d/2</sup>)  
  (requires storing nodes from both directions)

#### 🧪 Input & Output Example:

<img width="503" height="272" alt="Image" src="https://github.com/user-attachments/assets/29e8bff9-85f3-4eef-a9de-7454b5f17a84" />



### 8. Beam Search

**📄 File:** `beam_search.cpp`

#### 🔧 How It Works:

- A **limited-width** version of Best-First Search.
- At each level, it keeps only the **top `k` most promising nodes** (where `k` is the beam width).
- **Reduces memory and computation**, but may **miss the optimal solution** — trades **completeness for efficiency**.

#### 💡 Applications:

- **Natural Language Processing (NLP)** (e.g., decoding sequences in models)
- **Speech recognition**
- **Machine translation**
- **Protein folding prediction**
- **Resource-constrained AI systems** (low memory or processing power)

#### 📈 Complexity:

- **Time Complexity:** O(k × d × b)  
  (where **k** = beam width, **d** = depth, **b** = branching factor)
- **Space Complexity:** O(k × d)  
  (stores only `k` nodes per level up to depth `d`)

#### 🧪 Input & Output Example:

<img width="562" height="338" alt="Image" src="https://github.com/user-attachments/assets/101345af-2a54-49fb-a264-0edfe25ecc25" />



## 🎮 Game Theory Algorithms

### 9. Minimax Algorithm

**📄 File:** `minimax.cpp`

#### 🔧 How It Works:

- A decision-making algorithm for **two-player zero-sum games**.
- The **maximizing player** tries to **maximize** the game score.
- The **minimizing player** tries to **minimize** the opponent's score.
- Recursively evaluates the **game tree** to determine the best move.
- Assumes both players play optimally.

#### 💡 Applications:

- **Board games**: Chess, Checkers, Tic-Tac-Toe
- **Game AI**: AI agent decision making
- **Competitive decision-making** systems
- **Economic game theory** models

#### 📈 Complexity:

- **Time Complexity:** O(b^d)  
  (where **b** = branching factor, **d** = depth of the game tree)
- **Space Complexity:** O(d)  
  (depth of the recursion stack)

#### 🧪 Input & Output Example:

<img width="495" height="117" alt="Image" src="https://github.com/user-attachments/assets/b26f2c35-33f0-46d6-a10d-70dd264d202c" />



### 10. Alpha-Beta Pruning

**📄 Files:**  
- `alpha_beta.cpp`  
- `alpha_beta_dry_run.cpp` *(step-by-step execution example)*  
- `minimax_alpha_beta_pruning.cpp` *(Minimax combined with Alpha-Beta Pruning)*

#### 🔧 How It Works:

- An **optimization technique** for the Minimax algorithm.
- **Prunes** branches in the game tree that **cannot influence** the final decision.
- Maintains two variables:
  - **Alpha (α):** best option for the maximizer so far
  - **Beta (β):** best option for the minimizer so far
- **Cuts off** (prunes) a branch when `α ≥ β`.

#### 💡 Applications:

- **Chess engines** and competitive AI
- **Game AI optimization** (reduces unnecessary computation)
- **Machine learning** decision trees (for pruning irrelevant paths)
- **Economic modeling** in adversarial scenarios

#### 📈 Complexity:

- **Time Complexity:**  
  - **Best case:** O(b<sup>d/2</sup>)  
  - **Worst case:** O(b<sup>d</sup>)  
  (where **b** = branching factor, **d** = depth)
- **Space Complexity:** O(d)  
  (due to recursion stack depth)

#### 🧪 Input & Output Example:

<img width="490" height="142" alt="Image" src="https://github.com/user-attachments/assets/b29fcfac-e7ce-418a-a24d-c60955e43a61" />




## ⚙️ Optimization Algorithms

### 11. Hill Climbing

**📄 File:** `hill_climbing.cpp`

#### 🔧 How It Works:

- A **local search algorithm** that iteratively moves to a neighbor with a **higher value**.
- Continues climbing until it reaches a point where **no neighbor is better** — called a **local optimum**.
- It is a **greedy approach** and can get stuck in **local maxima** without finding the global maximum.

#### 💡 Applications:

- General **optimization problems**
- **Machine learning** parameter tuning
- **Traveling Salesman Problem** (local optimization strategies)
- **Neural network** training (optimization of weights)
- **Resource allocation** problems

#### 📈 Complexity:

- **Time Complexity:** O(n × m)  
  (where **n** = number of steps taken, **m** = number of neighbors evaluated per step)
- **Space Complexity:** O(1)  
  (only requires constant extra space)

#### 🧪 Input & Output Example:

<img width="603" height="177" alt="Image" src="https://github.com/user-attachments/assets/2b862e67-7ec2-488f-b4a3-ab23b22e85e4" />



## ▶️ Usage

Each algorithm is implemented as a **standalone C++ program**. To use any algorithm, follow these steps:

1. Choose the appropriate algorithm source file.
2. Compile the program using a C++ compiler.
3. Run the compiled executable with the required input parameters.

---

## 🛠️ Compilation

To compile any algorithm, use the following command:

g++ -o a_star a_star.cpp
g++ -o bfs breadth_first_search.cpp



## 📋 Notes

- All algorithms are implemented for **educational purposes**.
- Some algorithms include **"dry_run"** versions to help visualize step-by-step execution.
- Implementations use only **standard C++ libraries** — no external dependencies.
- Input formats may vary between algorithms; please check the comments inside each source file.

---

## 🤝 Contributing

Contributions are always welcome! You can help by:

- Adding more algorithms.
- Improving existing implementations.
- Adding test cases for better coverage.
- Enhancing documentation and examples.

