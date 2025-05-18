import pytest

sprite_to_expected = {
    "new_text": {
        "words" : "hello, world!",
        "x" : 100,
        "y" : 0,
        "font" : "default",
        "font_size" : 50,
        "color" : "yellow",
        "transparency" : 100,
        "size" : 10,
        "angle" : 0
    }
}


@pytest.mark.parametrize("sprite_items", list(sprite_to_expected.items()))
def test_sprite_attributes(sprite_items):
    import sys 
    sys.path.insert(0, '.')
    import play
    print(play.__path__)

    sprite_type, expected_values = sprite_items

    method = getattr(play, sprite_type)
    sprite = method(**expected_values)

    global num_frames
    global max_frames
    global data
    num_frames = 0
    max_frames = 100
    data = {}

        
    @play.repeat_forever
    def move():
        global num_frames
        global max_frames

        num_frames += 1

        if num_frames == max_frames:
            for key in expected_values:
                set_value = getattr(sprite, key)
                data[key] = set_value
            play.stop_program()
   
    play.start_program()

    for key in expected_values:
        if key == 'transparency':
            pass
        expected_value = expected_values[key]
        actual_value = data[key]
        print(key, expected_value, actual_value)
        if expected_value != actual_value:
            assert expected_value == actual_value, f'expected {expected_value} to be {actual_value}'
    
if __name__ == "__main__":
    test_sprite_attributes()

