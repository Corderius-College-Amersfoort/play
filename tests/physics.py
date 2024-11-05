import pytest
import sys

sys.path.append(".")

y = 0
screeny = 0


def test_physics(size=100):
    import play

    sprite = play.new_circle(color="gray", size=size)
    sprite.start_physics(obeys_gravity=True, bounciness=0, stable=True, friction=0)

    @play.when_program_starts
    async def start():
        global screeny
        screeny = play.screen.height
        print("Starting program")
        # wait for 2 seconds
        await play.timer(seconds=2)
        global y
        y = sprite.y
        play.stop_program()
        await play.timer(seconds=2)

    play.start_program()
    global y
    global screeny
    print(round(y))
    print(round((screeny / 2 * -1) + size))
    # check if the y is within 1% of ((screeny /2 * -1) + size):
    if round(y) != round((screeny / 2 * -1) + size):
        pytest.fail("The sprite should have fallen to the ground.")


# create a pytest for test_physics

if __name__ == "__main__":
    test_physics()
