## TetrisNNA-GA

This repository contains a **genetic algorithm (GA)** implementation combined with a **neural network-based AI** to play the classic game of Tetris. The system evolves neural network models over generations to improve their performance, using parallel processing for efficiency.

### Features
- **Genetic Algorithm:** Optimizes neural network weights over multiple generations.
- **Parallel Execution:** Simultaneous Tetris AI instances to speed up training.
- **Customizable Parameters:** Fine-tune the genetic algorithm and neural network parameters for better results.
- **Visual Demonstration:** Watch multiple Tetris AIs running simultaneously.

---

### How It Works
1. **Population Initialization:** A population of neural network models is generated randomly.
2. **Fitness Evaluation:** Each model plays Tetris, and its performance is scored.
3. **Selection and Mutation:** The best-performing models are selected, and new models are created by mutating their weights.
4. **Parallel Execution:** Tetris games are run in parallel to accelerate fitness evaluation.
5. **Generational Evolution:** The process repeats for a specified number of generations to optimize performance.

---
#### Features Calculated by the AI
The following features are calculated for evaluating Tetris states:
1. **Aggregate Height:** Sum of the heights of all columns.
2. **Number of Holes:** Total empty spaces below blocks.
3. **Bumpiness:** Difference in heights between consecutive columns.
4. **Number of Pits:** Columns with zero blocks.
5. **Maximum Well Depth:** Depth of the deepest well (a column surrounded by higher columns).
6. **Columns with Holes:** Number of columns containing at least one hole.
7. **Row Transitions:** Number of horizontal transitions between empty and filled cells.
8. **Column Transitions:** Number of vertical transitions between empty and filled cells.
9. **Height Variance:** Variance in column heights.
10. **Highest Peak:** The maximum height among all columns.
11. **Minimum Height:** The minimum height among all columns.
12. **Density:** Ratio of holes to total blocks.
13. **Cleared Lines:** Number of rows cleared in a given move.
---

### Setup and Requirements
1. Clone the repository:
   ```bash
   git clone https://github.com/GonzaloFuentes1/TetrisNNA-GA.git
   cd TetrisNNA-GA
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the main script:
   ```bash
   python main.py
   ```

---

### Configurable Parameters
Here are some of the parameters you can configure in the script:

| Parameter                  | Default Value | Description                                                                 |
|----------------------------|---------------|-----------------------------------------------------------------------------|
| **`GENERATIONS`**          | 50            | Number of generations for the genetic algorithm.                           |
| **`GENERATIONS_SIZE`**     | 10            | Number of models in each generation.                                       |
| **`input_size`**           | 13            | Number of input features for the neural network.                           |
| **`output_size`**          | 1             | Number of output features for the neural network.                          |
| **`weights_init_min`**     | -1            | Minimum value for initializing neural network weights.                     |
| **`weights_init_max`**     | 1             | Maximum value for initializing neural network weights.                     |
| **`n_cores`**              | 12            | Number of CPU cores to use for parallel execution.                         |

Modify these values directly in the code to customize the behavior of the simulation.

---

### Demo
Here’s how the parallel execution of multiple Tetris AIs looks in action:

![Tetris AI Execution](demo.gif)

---

### Contributing
Feel free to submit issues or pull requests if you have suggestions for improvements or new features.

---

### License
This project is licensed under the MIT License. See the `LICENSE` file for details.
