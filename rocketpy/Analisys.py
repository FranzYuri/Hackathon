# -*- coding: utf-8 -*-

__author__ = "Projeto Jupiter"
__copyright__ = "Copyright 20XX, Projeto Jupiter"
__license__ = "MIT"

import math
import matplotlib.pyplot as plt
import numpy as np
from rocketpy import Environment, Function, Flight, Rocket

class Analisys:
    """Uses other classes to make analisys of the chosen rocket.

    Attributes
    ----------
    Other classes:
        Analisys.env : Environment
            Environment object describing rail length, elevation, gravity and
            weather condition. See Environment class for more details.
        Analisys.rocket : Rocket
            Rocket class describing rocket. See Rocket class for more
            details.
        Analisys.flight : Flight
            Flight object keeping all flight information. See Flight class for
            more information.
    """
    def __init__(self, environment, rocket):
        """Make analisys calculations.

        Parameters
        ----------
        environment : Environment
            Environment to run simulation on. See help(Environment) for
            more information.
        rocket : Rocket
            Rocket to simulate. See help(Rocket) for more information.
        flight : Flight
            Object to simulate rocket's flight.
        
        """
        self.env = environment
        self.rocket = rocket
    def exportElipsesToKML(self, impact_ellipses, filename, origin_lat, origin_lon):
        """Generates a KML file with the ellipses on the impact point.

        Parameters
        ----------
        impact_ellipses : matplolib.patches.Ellipse
            Contains ellipse details for the plot. 
        filename : String
            Name to the KML exported file.
        origin_lat : float
            Latitute degrees of the Ellipse center.
        origin_lon : float
            Longitudeorigin_lat : float
            Latitute degrees of the Ellipse center. degrees of the Ellipse center.
        """
        outputs = []

        for impactEll in impact_ellipses:
            # Get ellipse path points
            points = impactEll.get_verts()
            plt.figure()
            plt.plot(points[:, 0], points[:, 1])

            # Convert path points to latlon
            ## Define constants
            R = 6371e3 # Earth radius in m
            lat_lon_points = []
            for point in points:
                x = point[0]
                y = point[1]
                # Convert to distance and bearing
                d = -(x**2 + y**2)**0.5
                brng  = math.atan2(x, y)
                # Convert to lat lon
                lat1 = math.radians(origin_lat) # Origin lat point converted to radians
                lon1 = math.radians(origin_lon) # Origin long point converted to radians
                lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
                    math.cos(lat1)*math.sin(d/R)*math.cos(brng))
                lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                            math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
                lat2 = math.degrees(lat2)
                lon2 = math.degrees(lon2)
                lat_lon_points += [[lat2, lon2]]

            # Export string
            string_output = ''
            for point in lat_lon_points:
                string_output += f'{point[1]},{point[0]},0 '
            outputs.append(string_output)


        plt.show()

        kml = f'''<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
        <Document>
            <name>{filename}.kml</name>
            <Style id="inline">
                <LineStyle>
                    <color>ff0000ff</color>
                    <width>2</width>
                </LineStyle>
            </Style>
            <Style id="inline0">
                <LineStyle>
                    <color>ff0000ff</color>
                    <width>2</width>
                </LineStyle>
            </Style>
            <StyleMap id="inline1">
                <Pair>
                    <key>normal</key>
                    <styleUrl>#inline</styleUrl>
                </Pair>
                <Pair>
                    <key>highlight</key>
                    <styleUrl>#inline0</styleUrl>
                </Pair>
            </StyleMap>
            <Placemark>
                <name>Elípse de Segurança 1</name>
                <styleUrl>#inline1</styleUrl>
                <LineString>
                    <tessellate>1</tessellate>
                    <coordinates>
        {outputs[0]}
                    </coordinates>
                </LineString>
            </Placemark>
            <Placemark>
                <name>Elípse de Segurança 2</name>
                <styleUrl>#inline1</styleUrl>
                <LineString>
                    <tessellate>1</tessellate>
                    <coordinates>
        {outputs[1]}
                    </coordinates>
                </LineString>
            </Placemark>
            <Placemark>
                <name>Elípse de Segurança 3</name>
                <styleUrl>#inline1</styleUrl>
                <LineString>
                    <tessellate>1</tessellate>
                    <coordinates>
        {outputs[2]}
                    </coordinates>
                </LineString>
            </Placemark>
        </Document>
        </kml>
        '''

        kml_file = open(filename+".kml", "w")
        kml_file.write(kml)
        kml_file.close()
        
    def Apogee_By_RocketMass(self, lower_bound_mass, upper_bound_mass, numPoints
    ):
        """Takes a minimum and a maximum value of mass and calculates the apogee
        for various values in beetwen. It then creates and prints a graph where
        the masses are shown in the x axis and the apogees in the y axis.

        The calculation for the apogee considers virtual masses of the rocket 
        without propellant and it does not impact the center of mass or the 
        moments of inertia. Environment wind effects are always deativated to 
        avoid distortions caused by flight instability.
        
        Parameters
        ----------
        mass_small : float
            smallest value of mass of which the apogee will be calculated
        mass_big : float
            biggest value of mass of which the apogee will be calculated
        numPoints : int
            number of points tha will be ploted
        
        Return
        ------
        None
        """
        originalMass = self.rocket.mass 
        def apogee(mass):
            mass_total = mass
            mass_propellant = self.rocket.motor.propellantInitialMass
            mass_unloaded = mass_total - mass_propellant
            self.rocket.mass = mass_unloaded

            #creates a copy of the provided environment to Anlisys object and 
            #deactivates wind effects
            env2 = self.env
            env2.setAtmosphericModel("StandardAtmosphere")
            TF = Flight(self.rocket,
                        env2,
                        inclination=90,
                        heading=90,
                        initialSolution=None,
                        terminateOnApogee=True,
                        maxTime=600,
                        maxTimeStep=np.inf,
                        minTimeStep=0,
                        rtol=1e-6,
                        atol=6 * [1e-3] + 4 * [1e-6] + 3 * [1e-3],
                        timeOvershoot=True,
                        verbose=False,
                        )
            return TF.apogee - env2.elevation
        apogeebymass = Function(apogee, inputs="Mass (kg) - with propellant", outputs="Estimated Apogee AGL (m)")
        apogeebymass.plot(lower_bound_mass, upper_bound_mass, int(numPoints))
        self.rocket.mass = originalMass
        return None
    