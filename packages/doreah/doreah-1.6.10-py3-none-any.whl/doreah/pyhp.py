from ._internal import DoreahConfig

config = DoreahConfig("pyhp",
	interpret=str,
	version=2
)


if config["version"] == 1:
	print("Using PYHP version 1")
	from .pyhp1 import *
elif config["version"] == 2:
	print("Using PYHP version 2")
	from .pyhp2 import *
elif config["version"] == 3:
	print("Using PYHP version 3")
	from .pyhp3 import *
