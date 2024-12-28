from enum import Enum
from typing import Dict, Iterable, Iterator

from pyTooling.Decorators import export, readonly


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
class Level:
	_name: str
	_levelIndex: int
	_colors: Dict[ColorMode, ColorTuple]

	def __init__(self, name: str, color: Dict[ColorMode, ColorTuple]) -> None:
		self._name = name
		self._levelIndex = 0
		self._colors = color

	def __getitem__(self, item: ColorMode) -> ColorTuple:
		return self._colors[item]

	@readonly
	def Name(self) -> str:
		return self._name

	@readonly
	def LevelIndex(self) -> int:
		return self._levelIndex

	@readonly
	def Colors(self) -> Dict[ColorMode, ColorTuple]:
		return self._colors


@export
class LevelStack:
	_levelsByIndex: Dict[int, Level]
	_levelsByName: Dict[str, Level]

	def __init__(self, levels: Iterable[Level]) -> None:
		self._levelsByIndex = {}
		self._levelsByName = {}

		for index, level in enumerate(levels):
			level._levelIndex = index

			self._levelsByIndex[index] = level
			self._levelsByName[level._name] = level

	def __getitem__(self, item: int | str) -> Level:
		try:
			return self._levelsByName[item]
		except KeyError:
			return self._levelsByIndex[item]

	def __iter__(self) -> Iterator[Level]:
		return iter(self._levelsByIndex.values())


pyEDAALevels = LevelStack((
		# on light bg:        dark,      light         on dark bg:                  dark,      light
		Level("red",    {ColorMode.LightMode: ColorTuple("#c62828", "#ef5350"), ColorMode.DarkMode: ColorTuple("#c62828", "#ef5350")}),  # Red
		Level("purple", {ColorMode.LightMode: ColorTuple("#8e24aa", "#ba68c8"), ColorMode.DarkMode: ColorTuple("#8e24aa", "#ba68c8")}),  # Purple
		Level("blue",   {ColorMode.LightMode: ColorTuple("#0277bd", "#29b6f6"), ColorMode.DarkMode: ColorTuple("#0277bd", "#29b6f6")}),  # Light Blue
		Level("green",  {ColorMode.LightMode: ColorTuple("#558b2f", "#9ccc65"), ColorMode.DarkMode: ColorTuple("#558b2f", "#9ccc65")}),  # Light Green
		Level("yellow", {ColorMode.LightMode: ColorTuple("#ff8f00", "#ffca28"), ColorMode.DarkMode: ColorTuple("#ff8f00", "#ffca28")}),  # Amber
		Level("gray",   {ColorMode.LightMode: ColorTuple("#37474f", "#78909c"), ColorMode.DarkMode: ColorTuple("#78909c", "#b0bec5")}),  # Blue Grey
	)
)

@export
class Layer:
	_name: str
	_layerIndex: int
	_level: Level

	def __init__(self, name: str, level: Level) -> None:
		self._name = name
		self._layerIndex = 0
		self._level = level

	@readonly
	def Name(self) -> str:
		return self._name

	@readonly
	def LayerIndex(self) -> int:
		return self._layerIndex

	@readonly
	def Level(self) -> Level:
		return self._level


@export
class LayerStack:
	_layersByIndex: Dict[int, Layer]
	_layersByName: Dict[str, Layer]

	def __init__(self, layers: Iterable[Layer]) -> None:
		self._layersByIndex = {}
		self._layersByName = {}

		for index, layer in enumerate(layers, start=-1):
			layer._layerIndex = index

			self._layersByIndex[index] = layer
			self._layersByName[layer._name] = layer

	def __getitem__(self, item: int | str) -> Layer:
		try:
			return self._layersByName[item]
		except KeyError:
			return self._layersByIndex[item]

	def __iter__(self) -> Iterator[Layer]:
		return iter(self._layersByIndex.values())


pyEDAALayers = LayerStack((
		Layer("Tools", pyEDAALevels[0]),
		Layer("Installation", pyEDAALevels[0]),
		Layer("CLI", pyEDAALevels[1]),
		Layer("EDA", pyEDAALevels[1]),
		Layer("Workflow", pyEDAALevels[2]),
		Layer("Language", pyEDAALevels[3]),
		Layer("Data", pyEDAALevels[3]),
		Layer("Project", pyEDAALevels[4]),
		Layer("Configuration", pyEDAALevels[4]),
		Layer("Web", pyEDAALevels[5]),
		Layer("GUI", pyEDAALevels[5])
	)
)


@export
class Project:
	_prefix: str
	_prefixSeperator: str
	_main: str
	_layer: Layer

	def __init__(self, prefix: str, prefixSeperator: str, main: str, layer: Layer) -> None:
		self._prefix = prefix
		self._prefixSeperator = prefixSeperator
		self._main = main
		self._layer = layer

	@readonly
	def Prefix(self) -> str:
		return self._prefix

	@readonly
	def Main(self) -> str:
		return self._main

	@readonly
	def ProjectName(self) -> str:
		return f"{self._prefix}{self._prefixSeperator}{self._main}"

	@readonly
	def Layer(self) -> Layer:
		return self._layer

	def __str__(self) -> str:
		return f"{self._prefix}{self._prefixSeperator}{self._main}"


@export
class ProjectDictionary:
	_projects: Dict[str, Project]

	def __init__(self, projects: Iterable[Project]) -> None:
		self._projects = {}

		for project in projects:
			self._projects[project.ProjectName] = project


pyEDAAProjects = ProjectDictionary((
		Project("py", "", "VHDLModel", pyEDAALayers[5]),
		Project("py", "", "SVModel",   pyEDAALayers[5]),
	)
)
