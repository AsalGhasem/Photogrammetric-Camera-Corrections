# Photogrammetric Camera Corrections

A Flask-based web application for calculating and applying common photogrammetric corrections to image coordinates.

The application takes measured image coordinates as input and applies a sequence of corrections for **principal point offset, lens distortion, atmospheric refraction, and spherical aberration**. The corrected coordinates and intermediate results are then displayed through a web interface.

## Overview

The application follows a sequential correction workflow:

1. Principal point correction
2. Radial lens distortion correction
3. Atmospheric refraction correction
4. Spherical aberration correction

The calculations are implemented in Python using NumPy and standard mathematical operations, with Flask providing the web interface.

## Corrections

### 1. Principal Point Correction

The input image coordinates `(xg, yg)` are corrected for the offset between the geometric and physical centers of the image.

```text
xp = xg - dx
yp = yg - dy
```

The corrected coordinates are then used to calculate the radial distance from the principal point:

```text
r = √(xp² + yp²)
```

The implementation uses fixed offsets for `dx` and `dy`.

### 2. Lens Distortion

Radial lens distortion coefficients are estimated using a least-squares polynomial fit.

The calibration data consists of radial distances and measured distortion values. A polynomial design matrix is constructed using odd powers of the radial distance:

```text
r, r³, r⁵, r⁷
```

The coefficients are obtained using NumPy's least-squares solver:

```python
np.linalg.lstsq()
```

The resulting coefficients are then used to calculate the radial lens distortion correction and its corresponding `x` and `y` components.

### 3. Atmospheric Refraction

A refraction correction is calculated based on the radial image distance, camera constant, and elevation parameters.

The resulting radial correction is resolved into `x` and `y` components and applied to the coordinates obtained after lens distortion correction.

### 4. Spherical Aberration

The final correction accounts for spherical aberration using the image radius, flying height, Earth radius, and camera constant.

The radial correction is converted into `x` and `y` components and applied to the previously corrected coordinates.

## Output

The application returns both intermediate and final results, including:

* Corrected coordinates after principal point correction
* Radial image distance
* Lens distortion correction
* Coordinates after lens distortion correction
* Atmospheric refraction correction
* Coordinates after refraction correction
* Spherical aberration correction
* Final corrected coordinates

## Tech Stack

* **Python**
* **Flask** — web application and request handling
* **NumPy** — numerical computation and least-squares estimation
* **HTML/CSS** — web interface

## Project Structure

```text
photogrammetric-camera-corrections/
│
├── app.py
├── templates/
│   └── index.html
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/photogrammetric-camera-corrections.git
cd photogrammetric-camera-corrections
```

### 2. Install the dependencies

```bash
pip install flask numpy
```

### 3. Run the application

```bash
python app.py
```

The Flask application runs in debug mode and serves the calculation interface through the browser.
