import play

score = 0
tekst_links = play.new_text(
    words=str(score),  # str zorgt ervoor dat de score een tekst wordt
    x=0,
    y=0,
)


@play.when_key_pressed("up")
def qq(key):
    global score
    score += 1
    tekst_links.words = str(score)


play.start_program()
