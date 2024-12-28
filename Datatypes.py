from typing import TypeVar, Union, Generic, Any, Self, Tuple

from pyTooling.Decorators import export

Coordinate = TypeVar("Coordinate", bound=Union[int, float])


@export
class Point(Generic[Coordinate]):
	x: Coordinate
	y: Coordinate

	def __init__(self, x: Coordinate, y: Coordinate) -> None:
		if not isinstance(x, (int, float)):
			raise TypeError()
		if not isinstance(y, (int, float)):
			raise TypeError()

		self.x = x
		self.y = y

	def Copy(self) -> Self:
		return self.__class__(self.x, self.y)

	def ToTuple(self) -> Tuple[Coordinate, Coordinate]:
		return self.x, self.y

	def __add__(self, other: Any) -> "Point[Coordinate]":
		if isinstance(other, Offset):
			return Point(
				self.x + other.xOffset,
				self.y + other.yOffset
			)
		else:
			raise TypeError()

	def __iadd__(self, other: Any) -> Self:
		if isinstance(other, Offset):
			self.x += other.xOffset
			self.y += other.yOffset
		else:
			raise TypeError()

		return self

	def __sub__(self, other: Any) -> Union["Offset[Coordinate]", "Point[Coordinate]"]:
		if isinstance(other, Point):
			return Offset(
				self.x - other.x,
				self.y - other.y
			)
		elif isinstance(other, Offset):
			return Point(
				self.x - other.xOffset,
				self.y - other.yOffset
			)
		else:
			raise TypeError()

	def __isub__(self, other: Any) -> Self:
		if isinstance(other, Offset):
			self.x -= other.xOffset
			self.y -= other.yOffset
		else:
			raise TypeError()

		return self

	def __repr__(self) -> str:
		return f"Point({self.x}, {self.y})"

	def __str__(self) -> str:
		return f"({self.x}, {self.y})"


@export
class Origin(Point[Coordinate]):
	def __init__(self) -> None:
		super().__init__(0, 0)

	def Copy(self) -> Self:
		raise RuntimeError()


@export
class Offset(Generic[Coordinate]):
	xOffset: Coordinate
	yOffset: Coordinate

	def __init__(self, xOffset: Coordinate, yOffset: Coordinate) -> None:
		if not isinstance(xOffset, (int, float)):
			raise TypeError()
		if not isinstance(yOffset, (int, float)):
			raise TypeError()

		self.xOffset = xOffset
		self.yOffset = yOffset

	def Copy(self) -> Self:
		return self.__class__(self.xOffset, self.yOffset)

	def ToTuple(self) -> Tuple[Coordinate, Coordinate]:
		return self.xOffset, self.yOffset

	def __add__(self, other: Any) -> "Offset[Coordinate]":
		if isinstance(other, Offset):
			return Offset(
				self.xOffset + other.xOffset,
				self.yOffset + other.yOffset
			)
		else:
			raise TypeError()

	def __iadd__(self, other: Any) -> Self:
		if isinstance(other, Offset):
			self.xOffset += other.xOffset
			self.yOffset += other.yOffset
		else:
			raise TypeError()

		return self

	def __sub__(self, other: Any) -> "Offset[Coordinate]":
		if isinstance(other, Offset):
			return Offset(
				self.xOffset - other.xOffset,
				self.yOffset - other.yOffset
			)
		else:
			raise TypeError()

	def __isub__(self, other: Any) -> Self:
		if isinstance(other, Offset):
			self.xOffset -= other.xOffset
			self.yOffset -= other.yOffset
		else:
			raise TypeError()

		return self

	def __repr__(self) -> str:
		return f"Offset({self.xOffset}, {self.yOffset})"

	def __str__(self) -> str:
		return f"({self.xOffset}, {self.yOffset})"


@export
class Size:
	width: Coordinate
	height: Coordinate

	def __init__(self, width: Coordinate, height: Coordinate) -> None:
		if not isinstance(width, (int, float)):
			raise TypeError()
		if not isinstance(height, (int, float)):
			raise TypeError()

		self.width = width
		self.height = height

	def Copy(self) -> Self:
		return self.__class__(self.width, self.height)

	def ToTuple(self) -> Tuple[Coordinate, Coordinate]:
		return self.width, self.height

	def __repr__(self) -> str:
		return f"Size({self.width}, {self.height})"

	def __str__(self) -> str:
		return f"({self.width}, {self.height})"


@export
class Segment(Generic[Coordinate]):
	start: Point[Coordinate]
	end: Point[Coordinate]

	def __init__(self, start: Point[Coordinate], end: Point[Coordinate], copyPoints: bool = True) -> None:
		self.start = start.Copy() if copyPoints else start
		self.end = end.Copy() if copyPoints else end


@export
class Line(Segment[Coordinate]):
	def ToOffset(self) -> Offset[Coordinate]:
		return self.end - self.start

	def ToTuple(self) -> Tuple[Tuple[Coordinate, Coordinate], Tuple[Coordinate, Coordinate]]:
		return self.start.ToTuple(), self.end.ToTuple()

	def __repr__(self) -> str:
		return f"Line({self.start}, {self.end})"

	def __str__(self) -> str:
		return f"({self.start} → {self.end})"
