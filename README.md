# EDA² Logos

All logos of EDA² can be created in a GitHub Action pipeline using Inkscape and other tools to produce SVG and PNG
images.

**How does it work?**
1. Draw logos with a Python script and emit SVG files.
2. Convert SVG images to PNG images
3. Optimize SVG images using svgo.

## Color Palette


## Dependencies

* Application
  * Inkscape
* Python
  * svgwrite (Jan 2021: maintenance end; Mar. 2022: only bugfixes; Aug. 2024: archived)
* NodeJS/NPM:
  * svgo - SVG Optimizer
