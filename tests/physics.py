import pytest

y = 0
screeny = 0
RADIUS = 100


def test_physics(RADIUS):
    import play

    sprite = play.new_circle(color="gray", radius=RADIUS)
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
    print(round((screeny / 2 * -1) + RADIUS))
    # check if the y is within 1% of ((screeny /2 * -1) + size):
    if round(y) != round((screeny / 2 * -1) + RADIUS):
        pytest.fail("The sprite should have fallen to the ground.")


# create a pytest for test_physics

if __name__ == "__main__":
    test_physics(RADIUS)
