import pytest

num_frames = 0
max_frames = 100

data = []
expected = (
    [0]
    + list(range(1, 25))
    + [25 for _ in range(25)]
    + list(range(25, 50))
    + [50 for _ in range(25)]
)


def test_ball_movement():
    import sys

    sys.path.insert(0, ".")
    import play

    ball = play.new_circle(
        color="gray",
        x=0,
        y=0,
        radius=100,
        border_color="light blue",
        border_width=10,
        transparency=100,
        size=100,
        angle=0,
    )
    ball.start_physics(y_speed=60, obeys_gravity=False)

    data.append(ball.y)

    @play.repeat_forever
    def move():
        global num_frames
        global data

        num_frames += 1

        data.append(round(ball.y))

        print(num_frames)

        if num_frames == 25:
            ball.physics.pause()
        elif num_frames == 50:
            ball.physics.unpause()
        elif num_frames == 75:
            ball.physics.pause()
        elif num_frames == 100:
            ball.physics.unpause()

        if num_frames == max_frames:
            play.stop_program()

    play.start_program()

    print(len(data), len(expected))

    for expected_value, actual_value in zip(expected, data):
        if expected_value != actual_value:
            pytest.fail(
                f"expected ball.y to be {expected_value} but the y value is {actual_value}"
            )


if __name__ == "__main__":
    test_ball_movement()
