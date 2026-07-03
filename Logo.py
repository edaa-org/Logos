from enum import Enum
from pathlib import Path
from typing import Optional as Nullable, Tuple, Dict

from pyTooling.Decorators import export
from pyTooling.MetaClasses import abstractmethod
from svgwrite import Drawing

from Datatypes import Offset, Size
from LayerStack import Project, ColorMode, ColorTuple, LevelStack


@export
class Logo:
	@abstractmethod
	def GenerateSVG(self, file: Path, colorMode: ColorMode) -> None:
		pass



@export
class PyEDAALayersLogo(Logo):
	_levelStack: LevelStack

	def __init__(self, levelStack: LevelStack) -> None:
		self._levelStack = levelStack

	def _drawRectangles(self, dwg, shades: Tuple[ColorTuple, ...], offset: Nullable[Offset[int]] = None, unit: int = 50):
		"""
		Draw the default multi-coloured EDA² logo without strokes.

		:param dwg:
		:param shades: Tuple of 6 double-shades.
		:param offset:
		:param unit:
		:returns:      undocumented
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

	def _drawHighlighted(self, dwg, row, shades: Tuple[ColorTuple, ...], offset: Nullable[Offset[int]] = None, unit: int = 50):
		"""
		Draw the per-project one-highlighted-layer EDAA logo, with strokes matching the dark colour of the tuple.
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
					fill="#ffffff" if levelIndex != row else colors.dark,
					fill_opacity=0.0 if levelIndex != row else 1.0,
					stroke=colors.dark,
					stroke_width="4px"
				)
			)
			dwg.add(
				dwg.rect(
					insert=secondRectOffset.ToTuple(),
					size=rectSize.ToTuple(),
					fill="#ffffff" if levelIndex != row else colors.light,
					fill_opacity=0.0 if levelIndex != row else 1.0,
					stroke=colors.light,
					stroke_width="4px"
				)
			)

	def GenerateSVG(self, file: Path, colorMode: ColorMode) -> None:
		"""
		Generate and save the default logo to file 'edaa.svg'
		"""
		drawingSize = Size(300, 300)
		dwg = Drawing(str(file), drawingSize.ToTuple(), debug=True)

		shades = tuple(level[colorMode] for level in self._levelStack)
		self._drawRectangles(dwg, shades)

		dwg.save(pretty=True)


class AllPyEDAALayersLogos(PyEDAALayersLogo):
	def __init__(self, levelStack: LevelStack) -> None:
		super().__init__(levelStack)

	def _drawPerColor(self, dwg, offset: Nullable[Offset[int]] = None):
		"""
		Draw all the per-project EDAA logos, both all-coloured and one-highlighted-layer variants, on all background test colours.
		"""
		if offset is None:
			offset = Offset(0, 0)

		colors = tuple(level.Colors[ColorMode.LightMode] for level in self._levelStack)

		# Single color, two shades
		for idx, col in enumerate(colors):
			self._drawRectangles(
				dwg,
				shades=tuple([col] * len(colors)),
				offset=offset + Offset(200 * idx, 0),
				unit=20
			)

		# Highlight color, two shades
		for idx, col in enumerate(colors):
			self._drawHighlighted(
				dwg,
				row=idx,
				shades=tuple([col] * len(colors)),
				offset=offset + Offset(200 * idx, 150),
				unit=20
			)

		# Highlight color, two shades
		for idx in range(len(colors)):
			self._drawHighlighted(
				dwg,
				row=idx,
				shades=colors,
				offset=offset + Offset(200 * idx, 300),
				unit=20
			)

	def GenerateLogosOnAllBackgroundsSVG(self, file: Path, backgrounds: Tuple[str]):
		"""
		Generate and save the backgrounds and per-project logo demo to 'backgrounds.svg'.
		"""
		shiftOffset = Offset(25, 25)
		backgroundSize = Size(1170, 3 * 150 + shiftOffset.yOffset * 2)

		drawingSize = Size(backgroundSize.width, backgroundSize.height * len(backgrounds))
		dwg = Drawing(str(file), drawingSize.ToTuple(), debug=True)


		for idx, background in enumerate(backgrounds):
			backgroundOffset = Offset(0, idx * backgroundSize.height)

			dwg.add(
				dwg.rect(
					insert=backgroundOffset.ToTuple(),
					size=backgroundSize.ToTuple(),
					fill=background
				)
			)

			self._drawPerColor(dwg, offset=backgroundOffset + shiftOffset)

		dwg.save(pretty=True)

class PyEDAAProjectBanner(PyEDAALayersLogo):
	def _drawProjectBanner(self, dwg, project: Project, colorMode: ColorMode, offset: Nullable[Offset[int]] = None, unit: int = 50):
		"""
		Draw a project banner (logo and text).
		"""
		if offset is None:
			offset = Offset(0, 0)

		def web_font_embedded(dwg, text, color, offset: Offset[int]):
			dwg.embed_google_web_font(name="Teko", uri='http://fonts.googleapis.com/css?family=Teko')
			# @import url(http://fonts.googleapis.com/css?family=Teko);
			dwg.embed_stylesheet("""
	        .TekoFont {
	            font-family: "Teko";
	            font-size: 260pt;
	        }
	        """)
			# This should work stand alone and embedded in a website!
			dwg.add(dwg.g(class_="TekoFont", )).add(dwg.text(text, insert=offset.ToTuple(), fill=color))

		# _draw(dwg, [COLORS[project[2]]]*6, shades, offset)
		self._drawHighlighted(
			dwg,
			row=project.Layer.LevelIndex.LevelIndex,
			shades=tuple([project.Layer.Level[colorMode]] * 6),
			offset=offset,
			unit=unit
		)

		textOffset = offset + Offset(360, 235)
		web_font_embedded(
			dwg,
			text=project.Prefix,
			color=project.Layer.Level[ColorMode.LightMode].dark,
			offset=textOffset
		)
		plen = len(project.Prefix)
		lmargin = 248 if plen == 2 else 820 if plen == 7 else 1040
		web_font_embedded(
			dwg,
			text=project.Main,
			color=project.Layer.Level[ColorMode.LightMode].light,
			offset=textOffset + Offset(lmargin, 0)
		)

	def GenerateProjectBanner(self, file: Path, project: Project, isDarkBackground: bool = False):
		"""
		Generate and save a project banner to a file.

		The size of the canvas matches the size of the logo only.
		Hence, the file needs to be post-processed.
		"""
		shiftOffset = Offset(2, 2)
		drawingSize = Size(300 + shiftOffset.xOffset * 2, 300 + shiftOffset.xOffset * 2)
		dwg = Drawing(str(file), drawingSize.ToTuple(), debug=True)
		self._drawProjectBanner(
			dwg,
			project=project,
			colorMode = ColorMode.DarkMode if isDarkBackground else ColorMode.LightMode,
			offset=shiftOffset
		)
		dwg.save(pretty=True)
