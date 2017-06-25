import zad3pannagabriella as gaba

assert not gaba.Resolver("Kristen", "Bell", "Kraina lodu").resolve() == gaba.ExitStatus.NOT_FOUND
assert gaba.Resolver("Johnny", "Depp", "Charlie").resolve() == gaba.ExitStatus.FOUND
assert gaba.Resolver("Jola", "Rutowicz", "Charlie").resolve() == gaba.ExitStatus.NOT_FOUND
assert not gaba.Resolver("Anna", "Wesołowska", "Sędzia").resolve() \
           == gaba.ExitStatus.FOUND_ACTOR_WITH_THAT_LAST_NAME
assert gaba.Resolver("Sacha", "Cohen", "Dyktator").resolve() == gaba.ExitStatus.FOUND
assert gaba.Resolver("Charlie", "Chaplin", "Dyktator").resolve() \
       == gaba.ExitStatus.FOUND_ACTOR_WITH_THAT_LAST_NAME
assert gaba.Resolver("Abelard", "Giza", "Wożonko").resolve() == gaba.ExitStatus.FOUND
assert gaba.Resolver("Jarosław", "Kaczyński", "O dwóch takich co ukradli księżyc").resolve() == gaba.ExitStatus.FOUND
assert gaba.Resolver("Sylvester", "Stallone", "Ranczo").resolve() == gaba.ExitStatus.NOT_FOUND
assert gaba.Resolver("Sylvester", "Stallone", "Rambo").resolve() == gaba.ExitStatus.FOUND
assert gaba.Resolver("Sylvestro", "Stallone", "Rambo").resolve() \
       == gaba.ExitStatus.FOUND_ACTOR_WITH_THAT_LAST_NAME
