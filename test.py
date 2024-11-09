import play


@play.controllers.when_any_axis_moved(0)
def move_left(axis_number):
    print(f"Axis {axis_number} moved to {axis_value}")


play.start_program()