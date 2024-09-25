import play

cat = play.new_text('=^.^=')

@play.when_key_pressed('up', 'down', 'left', 'right', 'w', 'a', 's', 'd')
def do(key):
    if key == 'up' or key == 'w':
        cat.y += 15
    if key == 'down' or key == 's':
        cat.y -= 15
    if key == 'right' or key == 'd':
        cat.x += 15
    if key == 'left' or key == 'a':
        cat.x -= 15


play.start_program()