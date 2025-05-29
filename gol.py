import tkinter as tk

GRID_SIZE = 100        # 100x100 grid
CELL_SIZE = 20        # Each cell is 20x20 pixels

ld = {}
simulation_running = False  # Is the simulation active?
paused = False              # Is the simulation paused?
generation = 0              # Current generation


# Count number of living neighbouring cells
def getNoLive(y, x):
    neighbours = []
    # Check for neighbours depending on whether the cell is on the edge
    if (x-1)>=0:
        neighbours.append((y, x-1))
    if x != 99:
        neighbours.append((y, x+1))
    if (y-1)>=0:
        neighbours.append((y-1, x))
    if y != 99:
        neighbours.append((y+1, x))
    if y != 99 and x != 99:
        neighbours.append((y+1, x+1))
    if (y-1)>=0 and (x-1)>=0:
        neighbours.append((y-1, x-1))
    if (y-1)>=0 and x != 99:
        neighbours.append((y-1, x+1))
    if y != 99 and (x-1)>=0:
        neighbours.append((y+1, x-1))
    
    # Adding all living neighbouring cells to a list and returning the length of the list 
    live_ns = [n for n in neighbours if grid[n[0]][n[1]] == 1]
    return len(live_ns)


# Determine whether a cell should live or die
def judge(y, x):
    if grid[y][x] == 1:
        if getNoLive(y, x) == 2 or getNoLive(y, x) == 3:
            ld[(y, x)] = 'L'
        else:
            ld[(y, x)] = 'D'
    elif grid[y][x] == 0:
        if getNoLive(y, x) == 3:
            ld[(y, x)] = 'L'
        else:
            ld[(y, x)] = 'D'


# Change the state of the grid to the next generation
def evolve(grid):
    for row in range(GRID_SIZE):
        for item in range(GRID_SIZE):
            y, x = row, item
            judge(y, x)
    for row in range(GRID_SIZE):
        for item in range(GRID_SIZE):
            y, x = row, item
            if ld[(y, x)] == 'L':
                grid[y][x] = 1
            elif ld[(y, x)] == 'D':
                grid[y][x] = 0


grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # 0 = dead, 1 = alive


def draw_grid():
    canvas.delete("all")
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = "black" if grid[y][x] == 1 else "white"
            canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=color, outline="gray"
            )


def toggle_cell(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        grid[y][x] = 1 - grid[y][x]  # Toggle 0 <-> 1
        draw_grid()


def run_simulation():
    global generation
    
    if simulation_running and not paused:
        evolve(grid)
        draw_grid()
        generation += 1
        generation_label.config(text=f"Generation: {generation}")
        root.after(500, run_simulation)  # 500ms delay between generations

        
def start_simulation():
    global simulation_running, paused
    if not simulation_running:
        simulation_running = True
        paused = False
        run_simulation()

def pause_simulation():
    global paused
    if simulation_running:
        paused = not paused
        if not paused:
            run_simulation()

        # Update pause button text
        pause_text.set("Pause" if not paused else "Resume")
    

def reset_grid():
    global grid, generation, simulation_running, paused
    
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    generation = 0
    simulation_running = False
    paused = False
    draw_grid()
    generation_label.config(text="Generation: 0")
    pause_text.set("Pause")


# Tkinter setup
root = tk.Tk()
root.title("Conway's Game of Life")

# Button frame (top of the window)
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Start and Reset buttons inside the frame
start_button = tk.Button(button_frame, text="Start", command=start_simulation)
start_button.pack(side="left", padx=5)

pause_text = tk.StringVar()
pause_text.set("Pause")

pause_button = tk.Button(button_frame, text="Pause", command=pause_simulation)
pause_button.pack(side="left", padx=5)

reset_button = tk.Button(button_frame, text="Reset", command=reset_grid)
reset_button.pack(side="left", padx=5)

generation_label = tk.Label(button_frame, text="Generation: 0")
generation_label.pack(side="left", padx=10)


canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE)
canvas.pack()

    
canvas.bind("<Button-1>", toggle_cell) 


draw_grid()

root.mainloop()

