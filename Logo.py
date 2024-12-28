from enum import Enum
from pathlib import Path
from typing import Optional as Nullable, Tuple, Dict

from pyTooling.Decorators import export
from pyTooling.MetaClasses import abstractmethod
from svgwrite import Drawing

from Datatypes import Offset, Size


@export
class ColorMode(Enum):
	LightMode = 0
	DarkMode = 1


@export
class ColorTuple:
	dark: str
	light: str

	def __init__(self, dark: str, light: str) -> None:
		self.dark = dark
		self.light = light


@export
class Logo:
	@abstractmethod
	def GenerateSVG(self, file: Path, colorMode: ColorMode) -> None:
		pass



@export
class PyEDAALayers(Logo):
	colors: Dict[ColorMode, Tuple[ColorTuple, ...]]

	def __init__(self):
		self.colors = {
			ColorMode.LightMode: (# dark, light on light
				ColorTuple("#c62828", "#ef5350"),  # Red
				ColorTuple("#8e24aa", "#ba68c8"),  # Purple
				ColorTuple("#0277bd", "#29b6f6"),  # Light Blue
				ColorTuple("#558b2f", "#9ccc65"),  # Light Green
				ColorTuple("#ff8f00", "#ffca28"),  # Amber
				ColorTuple("#37474f", "#78909c")   # Blue Grey
			),
			ColorMode.DarkMode: (# dark, light on light
				ColorTuple("#c62828", "#ef5350"),
				ColorTuple("#8e24aa", "#ba68c8"),
				ColorTuple("#0277bd", "#29b6f6"),
				ColorTuple("#558b2f", "#9ccc65"),
				ColorTuple("#ff8f00", "#ffca28"),
				ColorTuple("#78909c", "#b0bec5")
			)
		}

	def _drawRectangles(self, dwg, shades: Tuple[ColorTuple, ...], offset: Nullable[Offset] = None, unit: int = 50):
		"""
		Draw the default multi-coloured EDA² logo without strokes.

		:param dwg:
		:param colors: Tuple of 6 colors. One per layer.
		:param shades: Tuple of 2 shades.
		:param offset:
		:param unit:
		:return:
		"""
		if offset is None:
			offset = Offset(0, 0)

		rectSize = Size(2 * unit, unit)

		for levelIndex, colors in enumerate(shades):
			firstRectOffset = offset + Offset(2 * unit, levelIndex * unit)
			secondRectOffset = offset + Offset(4 * unit * (levelIndex % 2), levelIndex * unit)

			dwg.add(
				dwg.rect(
					insert=firstRectOffset.ToTuple(),
					size=rectSize.ToTuple(),
					fill=colors.dark,
				)
			)
			dwg.add(
				dwg.rect(
					insert=secondRectOffset.ToTuple(),
					size=rectSize.ToTuple(),
					fill=colors.light,
				)
			)

	def GenerateSVG(self, file: Path, colorMode: ColorMode) -> None:
		"""
		Generate and save the default logo to file 'edaa.svg'
		"""
		dwg = Drawing(str(file), (300, 300), debug=True)
		self._drawRectangles(dwg, self.colors[colorMode])
		dwg.save(pretty=True)
