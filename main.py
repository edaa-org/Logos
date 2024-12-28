from pathlib import Path
from typing import NoReturn

from Logo import PyEDAALayersLogo, ColorMode, AllPyEDAALayersLogos
from LayerStack import pyEDAAProjects, pyEDAALevels


def main() -> NoReturn:
	generatedOutputDirectory = Path("work/generated")
	if not generatedOutputDirectory.exists():
		print(f"Directory '{generatedOutputDirectory}' doesn't exist.")
		print(f"PWD: {Path.cwd()}")
		exit(1)

	print("Writing PyEDAALayersLogo ...")
	pyEDAALayersLogo = PyEDAALayersLogo(pyEDAALevels)
	pyEDAALayersLogo.GenerateSVG(generatedOutputDirectory / "edaa-light.svg", ColorMode.LightMode)
	pyEDAALayersLogo.GenerateSVG(generatedOutputDirectory / "edaa-dark.svg", ColorMode.DarkMode)

	backgrounds = (
		"#ffffff",  # white
		"#fcfcfc",  # BTD body
		"#333333",  # BTD sidebar
		"#383e46",
		"#0d1117",  # GitHub dark
		"#000000",  # black
	)
	print("Writing AllPyEDAALayersLogos ...")
	allPyEDAALayersLogos = AllPyEDAALayersLogos(pyEDAALevels)
	allPyEDAALayersLogos.GenerateLogosOnAllBackgroundsSVG(generatedOutputDirectory / "allBackgrounds.svg", backgrounds)


if __name__ == '__main__':
	main()
