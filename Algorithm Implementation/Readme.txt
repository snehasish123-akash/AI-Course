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






