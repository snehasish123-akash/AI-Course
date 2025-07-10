# 🎮 Connect Four – Human vs AI

This is a Python-based Connect Four game where you can play against an intelligent AI opponent. The AI uses the **Minimax Algorithm with Alpha-Beta Pruning** to choose the best moves.

---


## 🛠️ Required Libraries / Software

Before running the game, make sure you have the following installed:

### ✅ Python

- Recommended: **Python 3.x**
- You can download it from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### ✅ Install Required Python Libraries

Open your terminal or command prompt and run:    **pip install pygame numpy**

## ▶️ How to Run the Game

Make sure you have Python installed on your computer. Then follow these steps:

1️⃣ **Clone or Download** this repository  
2️⃣ Run the game using: Vs Studio application 


## 🎮 How to Play the Game

- The game board is a **7x6 grid**.
- You play as the **Red Player (Human)** and always go randomly.
- Click on a **column** to drop your red piece into that column.
- The **AI (Yellow)** will respond with its move automatically.
- The first player to connect **four in a row** (horizontally, vertically, or diagonally) **wins**!
- The game continues until there is a **winner** or the board is **full (draw)**.

---

## 🖼️ Game Screenshots

<img width="701" height="730" alt="Image" src="https://github.com/user-attachments/assets/f7bc3db4-0cbb-46c5-b0ec-3dd8f911d48c" />


## 🧠 Algorithm Used

The AI decision-making is powered by the **Minimax Algorithm** with **Alpha-Beta Pruning** for optimal performance.

---

### 🧩 Minimax Algorithm

- Explores all possible future moves.
- Evaluates each position to select the move that **minimizes the opponent's chance of winning**.
- Simulates human-like strategic thinking.

---

### ✂️ Alpha-Beta Pruning

- Enhances Minimax by **eliminating unnecessary branches** in the game tree.
- **Reduces computation time** without affecting the final decision.
- Allows the AI to search deeper in less time.

---

### 📊 Difficulty & Performance

- The AI difficulty can be controlled using the **search depth** parameter.
- Higher depth = **smarter AI**, but requires **more computation time**.


