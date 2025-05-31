from resources import Window, Point, Line, Cell, Maze

def main():
    win = Window(800, 600)
    

    # p1 = Point(10, 20)
    # p2 = Point(100, 20)
    # p3 = Point(200, 300)
    # l1 = Line(p1, p2)
    # l2 = Line(p2, p3)
    # l3 = Line(p3, p1)
    # win.draw_line(l1, "red")
    # win.draw_line(l2, "green")
    # win.draw_line(l3, "blue")

    # c1 = Cell(win)
    # c2 = Cell(win)
    # c3 = Cell(win)
    # c1.draw(0, 0, 100, 100)
    # c2.draw(100, 0, 200, 100)
    # c3.draw(0, 100, 100, 200)
    # c1.draw_move(c2)
    # c1.draw_move(c2, undo=True)
    # c1.draw_move(c3)

    maze = Maze(40, 40, 13, 18, 40, 40, win)

    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()

