import sys
sys.path.insert(0, '.')
import play
import pytest

radius = 20
x_speed = 6  # even number for testing
num_collisions = 0

ball = play.new_circle('black',
                       x=0,
                       y=0,
                       radius=radius)

ball.start_physics(x_speed=x_speed,
                   obeys_gravity=False)


box = play.new_box(color='black',
                   x=300,
                   y=0,
                   width=30,
                   height=300,
                   border_color="black",
                   border_width=10)

@play.repeat_forever
def check():
    if ball.x < 0:
        if num_collisions != 1:
            pytest.fail(f'num_collisions ({num_collisions}) should be one')
        sys.exit()

@ball.when_touching(box)
def collision():
    global num_collisions
    num_collisions += 1
    ball.x = 0
    ball.physics.x_speed = -10

play.start_program()