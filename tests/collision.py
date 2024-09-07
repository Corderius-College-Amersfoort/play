import random
import time

import pytest

failed = False


def test_collision():
    for _ in range(5000):
        global failed
        failed = False
        size = random.randint(0, 400)
        time.sleep(0.01)
        x = random.randint(0, 400)
        import play

        circle1 = play.new_circle(color='gray', radius=size)
        circle2 = play.new_circle(color='gray', radius=size, x=x)

        async def stop():
            play.stop_program()
            await play.timer(seconds=0.1)

        @play.when_program_starts
        async def start():
            # check if the two circles are colliding
            # should be colliding
            global failed
            if (size * 2) >= x:
                if not circle1.is_touching(circle2):
                    failed = True
            else:
                if circle1.is_touching(circle2):
                    failed = True
            await stop()

        play.start_program()
        if failed:
            if (size * 2) >= x:
                pytest.fail("The two circles should be colliding. X: " + str(x) + " Size: " + str(size))
            else:
                pytest.fail("The two circles should not be colliding. X: " + str(x) + " Size: " + str(size))


if __name__ == "__main__":
    test_collision()
