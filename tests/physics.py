import play

sprite = play.new_circle(color='gray', size=80)
sprite.start_physics(obeys_gravity=True, bounciness=0,stable=True, friction=0)

play.start_program()