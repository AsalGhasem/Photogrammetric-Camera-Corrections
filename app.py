from flask import Flask, render_template, request
request
from math import *
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        # getting the input coordinates
        xg = float(request.form['xg'])
        yg = float(request.form['yg'])

        # correction of the mismatch between the geometric center & the physcial center
        dx = 0.002
        dy = -0.005

        xp = xg - dx
        yp = yg - dy

        r = sqrt((pow(xp,2)) + (pow(yp,2))) # mm 

        # lens distortion
        spacing = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]) # mm
        L0 = np.array([0, 1, 1, 2, 1, 2, 2, 1, -1, -2, -2, -3, 0, 1, 1]) # micron
        L0 = np.multiply(L0, pow(0.1,6)) # mm

        A = np.array([[rVal, pow(rVal,3), pow(rVal,5), pow(rVal,7)] for rVal in spacing])

        xCap, residuals, rank, singularValues = np.linalg.lstsq(A, L0, rcond=None)
        K0, K1, K2, K3 = xCap

        delta_r_lens = (K0*r) + (K1*(pow(r,3))) + (K2*(pow(r,5))) + (K3*(pow(r,7)))

        delta_x = delta_r_lens * (xp / r)
        delta_y = delta_r_lens * (yp / r) 

        xLensDistortion = xp - delta_x
        yLensDistortion = yp - delta_y

        # refraction correction
        Z0 = 0.5 # km
        Z = 2.5 # km
        c = 152.844 # mm 
        k = 0.00241 * ((Z0 / ((pow(Z0,2)) - (6*Z0) + 250)) - ((pow(Z,2)) / (Z0 * (pow(Z,2) - (6*Z) + 250))))
        delta_r_refrac = k * r * (1 + (pow(r,2) / pow(c,2)))

        delta_x = delta_r_refrac * (xLensDistortion / r) 
        delta_y = delta_r_refrac * (yLensDistortion / r) 

        xRefraction = xLensDistortion - delta_x
        yRefraction = yLensDistortion - delta_y

        # spherical aberration
        H = 2.5 # km
        R = 6400 # km
        delta_r_spherical = (H * pow(r,3)) / (2 * R * pow(c,2)) # mm

        delta_x = delta_r_spherical * (xRefraction / r) 
        delta_y = delta_r_spherical * (yRefraction / r) 

        xSpherical = xRefraction + delta_x
        ySpherical = yRefraction + delta_y

        # pack everything for the template
        results = {
            'xp': xp,
            'yp': yp,
            'r': r,
            'delta_r_lens': delta_r_lens,
            'xLensDistortion': xLensDistortion,
            'yLensDistortion': yLensDistortion,
            'delta_r_refrac': delta_r_refrac,
            'xRefraction': xRefraction,
            'yRefraction': yRefraction,
            'delta_r_spherical': delta_r_spherical,
            'xSpherical': xSpherical,
            'ySpherical': ySpherical,
        }

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)