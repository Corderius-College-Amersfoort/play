import pytest

num_frames = 0
max_frames = 200
x_start = 0

expected = 300
actual = None


def test_async():
    import sys

    sys.path.insert(0, ".")
    import play

    bal = play.new_circle(x=x_start, color="blue", radius=50)
    bal.start_physics(obeys_gravity=False, x_speed=60)

    @play.when_program_starts
    async def start():
        bal.physics.x_speed = 300
        await play.timer(seconds=0.5)
        bal.physics.x_speed = 60

    @play.repeat_forever
    def move():
        global num_frames
        global actual
        num_frames += 1

        if num_frames == max_frames:
            actual = bal.x
            play.stop_program()

    play.start_program()

    if actual <= expected:
        pytest.fail(
            f"expected ball.x to be greater than {expected} but the x value is {actual}"
        )


if __name__ == "__main__":
    test_async()
