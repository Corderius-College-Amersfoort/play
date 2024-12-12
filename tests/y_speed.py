import sys
sys.path.insert(0, '.')
import play
import pytest

radius = 20
y_speed = 6  # even number for testing
num_frames = 0

ball = play.new_circle('black',
                       x=0,
                       y=0,
                       radius=radius)

ball.start_physics(y_speed=y_speed,
                   obeys_gravity=False)


@play.repeat_forever
def always():
    global num_frames
    if num_frames < ((play.globals.HEIGHT/2) - radius):
        if round(ball.y) != num_frames:
            pytest.fail(f'expected ball.y ({ball.y}) to be num of frames ({num_frames})')
    else:
        sys.exit()
    num_frames += 1

play.start_program()
