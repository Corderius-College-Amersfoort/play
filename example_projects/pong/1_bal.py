"""
Welkom!

We gaan samen het spel Pong bouwen (https://nl.wikipedia.org/wiki/Pong)

Hiervoor gaan we Python play (https://github.com/replit/play) gebruiken.

Stap 1:
Laten we eerst een bal in het scherm zetten.
De code hiervoor is al gegeven.

Stap 2:
- Open de "Shell" (als je het niet kunt vinden, klik het plusje naast "Console" en zoek naar "Shell")
- typ "python 1_bal.py" en druk Enter
- als het goed is, zie je een cirkel

Stap 3:
Het is nu een zwarte bal met een lichtblauwe rand en hij is vrij groot.
Ik denk dat jij dit beter kan.
Kun je het aanpassen (https://github.com/replit/play#playnew_circle):
a. maak de bal kleiner
b. maak de bal 1 kleur
c. zet de bal op x=100, x=-100. waar is dat op het scherm?
"""
import play

ball = play.new_circle(color='black',
                       x=0,
                       y=0,
                       radius=100,
                       border_color="light blue",
                       border_width=10,
                       transparency=100)

ball.x = 50

play.start_program()
