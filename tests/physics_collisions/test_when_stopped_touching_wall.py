import pytest

num_frames = 0
max_frames = 400
x_speed = 60

num_collisions = 0
expected_num_collisions = 1


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

    @play.repeat_forever
    def move():
        global num_frames

        num_frames += 1

        if num_frames == max_frames:
            play.stop_program()

    @ball.when_stopped_touching_wall
    def detect_collision():
        global num_collisions
        num_collisions += 1

    play.start_program()

    if num_collisions != expected_num_collisions:
        pytest.fail(f"expected exactly one collision event, but found {num_collisions}")


if __name__ == "__main__":
    test_ball_movement()
