#!/usr/bin/python3
"""
rc-tools - matplotlib basic example
===================================

A basic example of plotting on matplotlib.
You can start off with just the import + PLOT DATA + SHOW PLOT.
Other stuff is here just for reference.

---

plt.plot() -> https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html
matplotlib gallery -> https://matplotlib.org/stable/gallery/index.html

backends -> https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.use
default -> TkAgg / Qt5Agg (if PyQt5 installed)

use the move tool:
  - shift+leftclick to move on one axis
  - ctrl+rightclick to zoom in/out

web backend:
# pip install Tornado
plt.switch_backend('WebAgg')
"""
import matplotlib.pyplot as plt

## PLOT DATA ##

vals = [9,8,7,6,9]
plt.plot([0,1,2],[3,4,5])
plt.plot(range(len(vals)), vals, marker='o', linestyle='dashed', label="Cool Numbers")

## PLOT LABELS ##

# Label individual points
for x,y in zip(range(len(vals)), vals):
    plt.annotate(f'{y}', xy=[x,y], textcoords='data')

# Add a legend for the label= plots
plt.legend()

# Label an axis
plt.xlabel('Index')

## QUALITY OF LIFE ##

# Prevent scientific notation for values
plt.ticklabel_format(style='plain')

# Change mouse hover text format (avoid scientific notation)
plt.gca().format_coord = lambda x,y: f"x={x:.2f}, y={y:.2f}"

## SHOW PLOT ##

plt.show()
