cd ..
: object attributes
pytest -q --tb=no --disable-warnings tests/objects_attributes/test_circle.py > pytest_stdout 
pytest -q --tb=no --disable-warnings tests/objects_attributes/test_box.py >> pytest_stdout 
: pytest -q --tb=no --disable-warnings tests/objects_attributes/test_text.py >> pytest_stdout 

: physics
pytest -q --tb=no --disable-warnings tests/physics/test_x_movement.py >> pytest_stdout
pytest -q --tb=no --disable-warnings tests/physics/test_y_movement.py >> pytest_stdout
pytest -q --tb=no --disable-warnings tests/physics/test_physics_after_pause_unpause.py >> pytest_stdout
pytest -q --tb=no --disable-warnings tests/physics/test_physics_after_hide_show.py >> pytest_stdout

: physics_collisions
pytest -q --tb=no --disable-warnings tests/physics_collisions/test_steady_x_speed.py >> pytest_stdout
pytest -q --tb=no --disable-warnings tests/physics_collisions/test_when_touching_wall.py >> pytest_stdout
pytest -q --tb=no --disable-warnings tests/physics_collisions/test_when_touching_teleport.py >> pytest_stdout
pytest -q --tb=no --disable-warnings tests/physics_collisions/test_when_stopped_touching.py >> pytest_stdout
pytest -q --tb=no --disable-warnings tests/physics_collisions/test_when_stopped_touching_wall.py >> pytest_stdout