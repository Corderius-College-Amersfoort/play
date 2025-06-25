import pytest

num_frames = 0
max_frames = 200
x_speed = 300

method_check_inside_decorator = 0
num_collisions_decorator = 0


def test_ball_movement():
    import sys

    sys.path.insert(0, ".")
    import play

    ball = play.new_circle(
        color="black",
        x=0,
        y=0,
        radius=20,
    )

    ball.start_physics(
        obeys_gravity=False, x_speed=x_speed, friction=0, mass=10, bounciness=1.0
    )

    @ball.when_touching_wall
    def detect_collision():
        global num_collisions_decorator
        global method_check_inside_decorator
        num_collisions_decorator += 1
        if ball.is_touching_wall():
            method_check_inside_decorator += 1

    @play.repeat_forever
    def move():
        global num_frames
        num_frames += 1

        if num_frames == max_frames:
            play.stop_program()

    play.start_program()

    if not (num_collisions_decorator == 1 and method_check_inside_decorator == 1):
        pytest.fail(
            f"expected one collision by the method and the decorator, but found, {num_collisions_decorator}, {method_check_inside_decorator}"
        )


if __name__ == "__main__":
    test_ball_movement()
