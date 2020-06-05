"""

use svg write for much of this

as per terminal environment


"""
from pathlib import Path
from yaml import safe_load

THISDIR = str(Path(__file__).resolve().parent)


def rgbToHex(rgb):
	""" convert rgb tuple to hex """
	return "#{0:02x}{1:02x}{2:02x}".format(rgb[0], rgb[1], rgb[2])


def ansiTrueToRgb(ansiTrue):
	""" convert ansi truecolour to hex rgb """
	rgb = ansiTrue.replace("\033[", "").replace("38;2;", "").replace("48;2;",
	"").replace("m", "").split(";")
	return rgbToHex((int(rgb[0]), int(rgb[1]), int(rgb[2])))


def ansi256ToRGB(ansi256, theme=THISDIR + "/onedark.yml"):
	"""  convert ansi 256 to hex rgb """
	# 0-7, 8-15
	switch = int(
	ansi256.replace("\033[", "").replace("38;5;", "").replace("48;5;",
	"").replace("m", ""))
	ansi16Map = {
	0: "base01", 1: "base08", 2: "base0B", 3: "base09", 4: "base0D", 5: "base0E",
	6: "base0C", 7: "base06", 8: "base02", 9: "base12", 10: "base14",
	11: "base13", 12: "base16", 13: "base17", 14: "base15", 15: "base07"}
	if switch < 16:
		return ansi16ToRGB("\033[{}m".format(switch), ansi16Map, theme)
	# 6^3
	if switch < 232:
		switch -= 16
		red = switch // 36
		switch -= red * 36
		green = switch // 6
		switch -= green * 6
		blue = switch
		return rgbToHex((red * 51, green * 51, blue * 51))
	# 232-255
	switch -= 232
	return rgbToHex((switch * 11, switch * 11, switch * 11))


def ansi16ToRGB(ansi16, ansi16Map=None, theme=THISDIR + "/onedark.yml"):
	"""  convert ansi 16 to hex rgb """
	cCode = int(ansi16.replace("\033[", "").replace("m", ""))
	if 39 < cCode < 48 or 99 < cCode < 108:
		cCode -= 10
	ansi16Map = ansi16Map if ansi16Map is not None else {
	30: "base01", 31: "base08", 32: "base0B", 33: "base09", 34: "base0D",
	35: "base0E", 36: "base0C", 37: "base06", 90: "base02", 91: "base12",
	92: "base14", 93: "base13", 94: "base16", 95: "base17", 96: "base15",
	97: "base07"}
	return "#" + safe_load(open(theme))[ansi16Map[cCode]]


def ansiColourToRGB(ansiColour, theme=THISDIR + "/onedark.yml"):
	""" convert an ansi colour to a hex colour

	Args:
		ansiColour (string): ansi colour

	Returns:
		string: hex code

	"""
	# 38;5
	if ansiColour.startswith("\033[38;5"):
		return ansi256ToRGB(ansiColour, theme)
	# 48;5
	if ansiColour.startswith("\033[48;5"):
		return ansi256ToRGB(ansiColour, theme)
	# 38;2
	if ansiColour.startswith("\033[38;2"):
		return ansiTrueToRgb(ansiColour)
	# 48;2
	if ansiColour.startswith("\033[48;2"):
		return ansiTrueToRgb(ansiColour)
	# 30 - 37
	if ansiColour.startswith("\033[3"):
		return ansi16ToRGB(ansiColour, theme=theme)
	# 90 - 97
	if ansiColour.startswith("\033[9"):
		return ansi16ToRGB(ansiColour, theme=theme)
	# 40 - 47
	if ansiColour.startswith("\033[4"):
		return ansi16ToRGB(ansiColour, theme=theme)
	# 100 - 107
	if ansiColour.startswith("\033[10"):
		return ansi16ToRGB(ansiColour, theme=theme)
	return "#" + safe_load(open(theme))["base05"] # fail on fg colour


def findLen(string):
	""" find the length of a string and take into account that emojis are double
	width """
	counter = 0
	for i in string:
		if ord(i) > 10000: # emoji is double width
			counter += 1
		counter += 1
	return counter