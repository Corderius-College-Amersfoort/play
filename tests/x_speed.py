import sys
sys.path.insert(0, '.')
import play
import pytest

radius = 20
x_speed = 6  # even number for testing
num_frames = 0

ball = play.new_circle('black',
                       x=0,
                       y=0,
                       radius=radius)

ball.start_physics(x_speed=x_speed,
                   obeys_gravity=False)


@play.repeat_forever
def always():
    global num_frames
    if num_frames < ((play.globals.WIDTH/2) - radius):
        if round(ball.x) != num_frames:
            pytest.fail(f'expected ball.x ({ball.x}) to be num of frames ({num_frames})')
    else:
        sys.exit()
    num_frames += 1

play.start_program()
