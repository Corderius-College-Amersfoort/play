import pytest

num_frames = 0
max_frames = 100
x_speed = 60

x_data = []


def test_ball_movement():
    import sys

    sys.path.insert(0, ".")
    import play

    ball = play.new_circle(color="gray", radius=10)
    ball.start_physics(
        obeys_gravity=False, bounciness=0, stable=False, friction=1, x_speed=x_speed
    )

    x_data.append(ball.x)

    @play.repeat_forever
    def move():
        global num_frames
        global x_data

        num_frames += 1

        x_data.append(ball.x)

        if num_frames == max_frames:
            play.stop_program()

    play.start_program()

    for index, x_position in enumerate(x_data):
        expected_value = round(x_position)
        actual_value = index
        print(expected_value, actual_value)
        if expected_value != actual_value:
            pytest.fail(
                f"expected ball.x to be {expected_value}, but it is {actual_value}"
            )


if __name__ == "__main__":
    test_ball_movement()
