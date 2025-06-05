from maze import Window, Point, Line, Cell

def main():
    win = Window(800, 600)
    cell_one = Cell(win)
    cell_one.draw(100, 100, 200, 200)
    cell_two = Cell(win)
    cell_two.draw(300, 300, 400, 400)
    cell_three = Cell(win)
    cell_three.left_wall = False
    cell_three.draw(200, 200, 300, 300)
    cell_one.draw_move(cell_two)
    cell_two.draw_move(cell_three, undo=True)
    win.wait_for_close()

main()