import pytest

num_frames = 0
max_frames = 200
x_speed = 60

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

    batje = play.new_box(color="black", x=200)

    ball.start_physics(
        obeys_gravity=False, x_speed=x_speed, friction=0, mass=10, bounciness=1.0
    )
    batje.start_physics(
        obeys_gravity=False, can_move=False, friction=0, mass=10, bounciness=1.0
    )

    @ball.when_touching(batje)
    def detect_collision():
        global num_collisions_decorator
        global method_check_inside_decorator
        num_collisions_decorator += 1
        if ball.is_touching(batje):
            method_check_inside_decorator += 1

    @play.repeat_forever
    def move():
        global num_frames
        num_frames += 1

        if num_frames == max_frames:
            play.stop_program()

    play.start_program()

    if not (num_collisions_decorator == 2 and method_check_inside_decorator == 2):
        pytest.fail(
            f"expected two collisions by the method and the decorator, but found {num_collisions_decorator}, {method_check_inside_decorator}"
        )


if __name__ == "__main__":
    test_ball_movement()
