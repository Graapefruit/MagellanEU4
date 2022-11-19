
from MagellanClasses.Controller.Controller import Controller
from random import randint

FAREWELLS = ["drink water", "clean your room", "sleep on time", "stretch", "embargo your rivals", "improve with outraged countries", "do your laundry", "insult your rivals", "turn off your edicts", "floss your teeth"]
if __name__ == "__main__":
	controller = Controller()
	controller.view.startMainLoop()
	print("Don't forget to {}!".format(FAREWELLS[randint(0, len(FAREWELLS)-1)]))