from maze import Window, Maze
def main():
    win = Window(800, 600)
    maze = Maze(0, 0, 12, 16, 50, 50, win)
    win.wait_for_close()

main()