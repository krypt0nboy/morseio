from engine import Engine

engine = Engine()
engine.load_morse_lib()
encoded = engine.encode("I'm a morse code message.")
engine.play(encoded)
