import pytest

num_frames = 0
max_frames = 1000
x_speed = 60
data_x_speed = []
data_y = []


def test_ball_movement():
    import sys

    sys.path.insert(0, ".")
    import play

    ball = play.new_circle(
        color="gray", x=0, y=0, radius=10, border_color="light blue", size=100, angle=0
    )
    ball.start_physics(
        x_speed=x_speed, obeys_gravity=False, mass=10, bounciness=1, friction=0
    )

    @play.repeat_forever
    def move():
        global num_frames
        global data_x_speed
        global data_y

        num_frames += 1

        data_x_speed.append(ball.physics.x_speed)
        data_y.append(ball.y)

        if num_frames == max_frames:
            play.stop_program()

    play.start_program()

    for actual_value in data_y:
        if actual_value != 0:
            pytest.fail(f"expected y {actual_value} to be 0")


if __name__ == "__main__":
    test_ball_movement()
