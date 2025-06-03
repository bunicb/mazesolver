from maze import Window, Point, Line

def main():
    win = Window(800, 600)
    point_one = Point(50, 50)
    point_two = Point(200, 300)
    test_line = Line(point_one, point_two)
    point_three = Point(250, 50)
    point_four = Point(10, 100)
    test_line2 = Line(point_three, point_four)
    win.draw_line(test_line, "red")
    win.draw_line(test_line2, "blue")
    win.wait_for_close()

main()