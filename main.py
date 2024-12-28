from pathlib import Path
from typing import Dict, NoReturn

from Logo import PyEDAALayers, ColorMode


def main() -> NoReturn:
	generatedOutputDirectory = Path("work/generated")
	if not generatedOutputDirectory.exists():
		print(f"Directory '{generatedOutputDirectory}' doesn't exist.")
		print(f"PWD: {Path.cwd()}")
		exit(1)

	pyEDAALayersLogo = PyEDAALayers()
	pyEDAALayersLogo.GenerateSVG(generatedOutputDirectory / "edaa-light.svg", ColorMode.LightMode)
	pyEDAALayersLogo.GenerateSVG(generatedOutputDirectory / "edaa-dark.svg", ColorMode.DarkMode)


if __name__ == '__main__':
	main()
