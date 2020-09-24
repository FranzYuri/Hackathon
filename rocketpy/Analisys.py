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
    def __init__(self, environment):
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
        #self.rocket = rocket
    """def exportElipsesToKML(self, impact_ellipses, filename, origin_lat, origin_lon):
        """"""Generates a KML file with the ellipses on the impact point.

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
        """"""
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
        kml_file.close()"""
        
    """def Apogee_By_RocketMass(self, lower_bound_mass, upper_bound_mass, numPoints):
        """"""Takes a minimum and a maximum value of mass and calculates the apogee
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
        """"""
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
        return None"""


    def CompareRockets(self, rocket1, rocket2):
        """Takes two different rockets and prints th flight trajectory of both
        of them in the same plot
            
        Parameters
        ----------
        rocket : list
            List of rockets
            
        Return
        ------
        None
        """
        #initial stuff
        flightRocket1 = Flight(rocket1, self.env, inclination=85, heading=0)
        flightRocket2 = Flight(rocket2, self.env, inclination=85, heading=0)

        def plot3dTrajectory(flightRocket1, flightRocket2):

            # Post-process results
            if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()
            if flightRocket2.postProcessed is False:
                flightRocket2.postProcess()

            # Get max and min x and y
            # Rocket 1:
            maxZ0 = max(flightRocket1.z[:, 1] - flightRocket1.env.elevation )
            maxX0 = max(flightRocket1.x[:, 1])
            minX0 = min(flightRocket1.x[:, 1])
            maxY0 = max(flightRocket1.y[:, 1])
            minY0 = min(flightRocket1.y[:, 1])
            maxXY0 = max(maxX0, maxY0)
            minXY0 = min(minX0, minY0)

            # Rocket 12:
            maxZ1 = max(flightRocket2.z[:, 1] - flightRocket2.env.elevation )
            maxX1 = max(flightRocket2.x[:, 1])
            minX1 = min(flightRocket2.x[:, 1])
            maxY1 = max(flightRocket2.y[:, 1])
            minY1 = min(flightRocket2.y[:, 1])
            maxXY1 = max(maxX1, maxY1)
            minXY1 = min(minX1, minY1)
            # Max and min:
            maxZ = max(maxZ0, maxZ1)
            maxXY = max(maxXY0,maxXY1)
            minXY = min(minXY0,minXY1)


            # Create figure
            fig1 = plt.figure(figsize=(9, 9))

            ax1 = plt.subplot(111, projection="3d")
                
            ax1.plot(
                flightRocket1.x[:, 1], flightRocket1.y[:, 1], zs= 0, zdir="z", linestyle="--",
                )
            ax1.plot(flightRocket1.x[:, 1], flightRocket1.z[:, 1] - flightRocket1.env.elevation, zs=minXY, zdir="y", linestyle="--")
            ax1.plot(flightRocket1.y[:, 1], flightRocket1.z[:, 1] - flightRocket1.env.elevation, zs=minXY, zdir="x", linestyle="--")
            ax1.plot(flightRocket1.x[:, 1], flightRocket1.y[:, 1], flightRocket1.z[:, 1] - flightRocket1.env.elevation, linewidth='2',label='Rocket 1')
            ax1.scatter(0, 0, 0)
            ax1.set_xlabel("X - East (m)")
            ax1.set_ylabel("Y - North (m)")
            ax1.set_zlabel("Z - Altitude Above Ground Level (m)")
            ax1.set_title("Flight Trajectory")
            ax1.set_zlim3d([0, maxZ])
            ax1.set_ylim3d([minXY, maxXY])
            ax1.set_xlim3d([minXY, maxXY])
            ax1.view_init(15, 45)

            #ax1 = plt.subplot(111, projection="3d")
            ax1.plot(
                flightRocket2.x[:, 1], flightRocket2.y[:, 1], zs= 0, zdir="z", linestyle="--",
            )
            ax1.plot(
                flightRocket2.x[:, 1], flightRocket2.z[:, 1] - flightRocket2.env.elevation, zs=minXY, zdir="y", linestyle="--"
            )
            ax1.plot(
                flightRocket2.y[:, 1], flightRocket2.z[:, 1] - flightRocket2.env.elevation, zs=minXY, zdir="x", linestyle="--"
            )
            ax1.plot(
                flightRocket2.x[:, 1], flightRocket2.y[:, 1], flightRocket2.z[:, 1] - flightRocket2.env.elevation, linewidth='2',
                label='Rocket 2',color='blue'
                )
            ax1.scatter(0, 0, 0)
            ax1.set_xlabel("X - East (m)")
            ax1.set_ylabel("Y - North (m)")
            ax1.set_zlabel("Z - Altitude Above Ground Level (m)")
            ax1.set_title("Flight Trajectory")
            ax1.set_zlim3d([0, maxZ])
            ax1.set_ylim3d([minXY, maxXY])
            ax1.set_xlim3d([minXY, maxXY])
            ax1.view_init(15, 45)

            ax1.legend()
            plt.show()
            return None

        def plotFlightPathAngleData(flightRocket1, flightRocket2):
            """Prints out Flight path and Rocket Attitude angle graphs available
            about the Flight

            Parameters
            ----------
            None
            
            Return
            ------
            None
            """
            # Post-process results
            if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()
            if flightRocket2.postProcessed is False:
                flightRocket2.postProcess()

            # Get index of time before parachute event
                # Rocket 1:
            if len(flightRocket1.parachuteEvents) > 0:
                eventTime1 = flightRocket1.parachuteEvents[0][0] + flightRocket1.parachuteEvents[0][1].lag
                eventTimeIndex1 = np.nonzero(flightRocket1.x[:, 0] == eventTime1)[0][0]
            else:
                eventTime1 = flightRocket1.tFinal
                eventTimeIndex1 = -1

                # Rocket 2:
            if len(flightRocket2.parachuteEvents) > 0:
                eventTime2 = flightRocket2.parachuteEvents[0][0] + flightRocket2.parachuteEvents[0][1].lag
                eventTimeIndex2 = np.nonzero(flightRocket2.x[:, 0] == eventTime2)[0][0]
            else:
                eventTime2 = flightRocket2.tFinal
                eventTimeIndex2 = -1

            eventTime = max(eventTime1, eventTime2)
            
            # Path, Attitude and Lateral Attitude Angle
            # Angular position plots
            fig5 = plt.figure(figsize=(9, 12))

            ax1 = plt.subplot(311)
            ax1.plot(flightRocket1.pathAngle[:, 0], flightRocket1.pathAngle[:, 1], label="Flight Path Angle")
            ax1.plot(
                flightRocket1.attitudeAngle[:, 0],
                flightRocket1.attitudeAngle[:, 1],
                label="Rocket Attitude Angle",
            )

            ax1.set_xlim(0, eventTime)
            ax1.legend()
            ax1.grid(True)
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Angle (°)")
            ax1.set_title("Flight Path and Attitude Angle - Rocket 1")

            ax2 = plt.subplot(312)
            ax2.plot(flightRocket2.pathAngle[:, 0], flightRocket2.pathAngle[:, 1], label="Flight Path Angle")
            ax2.plot(
                flightRocket2.attitudeAngle[:, 0],
                flightRocket2.attitudeAngle[:, 1],
                label="Rocket Attitude Angle",
            )

            ax2.set_xlim(0, eventTime)
            ax2.legend()
            ax2.grid(True)
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Angle (°)")
            ax2.set_title("Flight Path and Attitude Angle - Rocket 2")

            ax3 = plt.subplot(313)
            ax3.plot(flightRocket1.lateralAttitudeAngle[:, 0], flightRocket1.lateralAttitudeAngle[:, 1], label="Rocket 1")
            ax3.plot(flightRocket2.lateralAttitudeAngle[:, 0], flightRocket2.lateralAttitudeAngle[:, 1], label="Rocket 2")
            ax3.set_xlim(0, eventTime)
            ax3.legend()
            ax3.set_xlabel("Time (s)")
            ax3.set_ylabel("Lateral Attitude Angle (°)")
            ax3.set_title("Lateral Attitude Angle")
            ax3.grid(True)

            plt.subplots_adjust(hspace=0.5)
            plt.show()

            return None

        def plotAttitudeData(flightRocket1, flightRocket2):
            """Prints out all Angular position graphs available about the Flight

            Parameters
            ----------
            None
            
            Return
            ------
            None
            """
            # Post-process results
            if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()
            if flightRocket2.postProcessed is False:
                flightRocket2.postProcess()

            # Get index of time before parachute event
                # Rocket 1:
            if len(flightRocket1.parachuteEvents) > 0:
                eventTime1 = flightRocket1.parachuteEvents[0][0] + flightRocket1.parachuteEvents[0][1].lag
                eventTimeIndex1 = np.nonzero(flightRocket1.x[:, 0] == eventTime1)[0][0]
            else:
                eventTime1 = flightRocket1.tFinal
                eventTimeIndex1 = -1

                # Rocket 2:
            if len(flightRocket2.parachuteEvents) > 0:
                eventTime2 = flightRocket2.parachuteEvents[0][0] + flightRocket2.parachuteEvents[0][1].lag
                eventTimeIndex2 = np.nonzero(flightRocket2.x[:, 0] == eventTime2)[0][0]
            else:
                eventTime2 = flightRocket2.tFinal
                eventTimeIndex2 = -1

            eventTime = max(eventTime1, eventTime2)

            # Angular position plots
            fig3 = plt.figure(figsize=(12, 16))

            ax1 = plt.subplot(421)
            ax1.plot(flightRocket1.e0[:, 0], flightRocket1.e0[:, 1], label="$e_0$")
            ax1.plot(flightRocket1.e1[:, 0], flightRocket1.e1[:, 1], label="$e_1$")
            ax1.plot(flightRocket1.e2[:, 0], flightRocket1.e2[:, 1], label="$e_2$")
            ax1.plot(flightRocket1.e3[:, 0], flightRocket1.e3[:, 1], label="$e_3$")
            ax1.set_xlim(0, eventTime)
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Euler Parameters")
            ax1.set_title("Euler Parameters - Rocket 1")
            ax1.legend()
            ax1.grid(True)

            ax2 = plt.subplot(422)
            ax2.plot(flightRocket2.e0[:, 0], flightRocket2.e0[:, 1], label="$e_0$")
            ax2.plot(flightRocket2.e1[:, 0], flightRocket2.e1[:, 1], label="$e_1$")
            ax2.plot(flightRocket2.e2[:, 0], flightRocket2.e2[:, 1], label="$e_2$")
            ax2.plot(flightRocket2.e3[:, 0], flightRocket2.e3[:, 1], label="$e_3$")
            ax2.set_xlim(0, eventTime)
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Euler Parameters")
            ax2.set_title("Euler Parameters - Rocket 2")
            ax2.legend()
            ax2.grid(True)

            ax3 = plt.subplot(423)
            ax3.plot(flightRocket1.psi[:, 0], flightRocket1.psi[:, 1])
            ax3.set_xlim(0, eventTime)
            ax3.set_xlabel("Time (s)")
            ax3.set_ylabel("ψ (°)")
            ax3.set_title("Euler Precession Angle - Rocket 1")
            ax3.grid(True)

            ax4 = plt.subplot(424)
            ax4.plot(flightRocket2.psi[:, 0], flightRocket2.psi[:, 1])
            ax4.set_xlim(0, eventTime)
            ax4.set_xlabel("Time (s)")
            ax4.set_ylabel("ψ (°)")
            ax4.set_title("Euler Precession Angle - Rocket 2")
            ax4.grid(True)

            ax5 = plt.subplot(425)
            ax5.plot(flightRocket1.theta[:, 0], flightRocket1.theta[:, 1], label="θ - Nutation")
            ax5.set_xlim(0, eventTime)
            ax5.set_xlabel("Time (s)")
            ax5.set_ylabel("θ (°)")
            ax5.set_title("Euler Nutation Angle - Rocket 1")
            ax5.grid(True)

            ax6 = plt.subplot(426)
            ax6.plot(flightRocket2.theta[:, 0], flightRocket2.theta[:, 1], label="θ - Nutation")
            ax6.set_xlim(0, eventTime)
            ax6.set_xlabel("Time (s)")
            ax6.set_ylabel("θ (°)")
            ax6.set_title("Euler Nutation Angle - Rocket 2")
            ax6.grid(True)
            
            ax7 = plt.subplot(427)
            ax7.plot(flightRocket1.phi[:, 0], flightRocket1.phi[:, 1], label="φ - Spin")
            ax7.set_xlim(0, eventTime)
            ax7.set_xlabel("Time (s)")
            ax7.set_ylabel("φ (°)")
            ax7.set_title("Euler Spin Angle - Rocket 1")
            ax7.grid(True)

            ax8 = plt.subplot(428)
            ax8.plot(flightRocket2.phi[:, 0], flightRocket2.phi[:, 1], label="φ - Spin")
            ax8.set_xlim(0, eventTime)
            ax8.set_xlabel("Time (s)")
            ax8.set_ylabel("φ (°)")
            ax8.set_title("Euler Spin Angle - Rocket 2")
            ax8.grid(True)

            plt.subplots_adjust(hspace=0.5)
            plt.show()

            return None

        def plotAngularKinematicsData(flightRocket1, flightRocket2):
            """Prints out all Angular veolcity and acceleration graphs available
            about the Flight

            Parameters
            ----------
            None
            
            Return
            ------
            None
            """
            # Post-process results
            if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()
            if flightRocket2.postProcessed is False:
                flightRocket2.postProcess()

            # Get index of time before parachute event
                # Rocket 1:
            if len(flightRocket1.parachuteEvents) > 0:
                eventTime1 = flightRocket1.parachuteEvents[0][0] + flightRocket1.parachuteEvents[0][1].lag
                eventTimeIndex1 = np.nonzero(flightRocket1.x[:, 0] == eventTime1)[0][0]
            else:
                eventTime1 = flightRocket1.tFinal
                eventTimeIndex1 = -1

                # Rocket 2:
            if len(flightRocket2.parachuteEvents) > 0:
                eventTime2 = flightRocket2.parachuteEvents[0][0] + flightRocket2.parachuteEvents[0][1].lag
                eventTimeIndex2 = np.nonzero(flightRocket2.x[:, 0] == eventTime2)[0][0]
            else:
                eventTime2 = flightRocket2.tFinal
                eventTimeIndex2 = -1

            eventTime = max(eventTime1, eventTime2)
            
            # Angular velocity and acceleration plots
            fig4 = plt.figure(figsize=(16, 12))
            ax1 = plt.subplot(321)
            ax1.plot(flightRocket1.w1[:, 0], flightRocket1.w1[:, 1], color="#ff7f0e")
            ax1.set_xlim(0, eventTime)
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Angular Velocity - ${\omega_1}$ (rad/s)", color="#ff7f0e")
            ax1.set_title(
                "Angular Velocity ${\omega_1}$ | Angular Acceleration ${\\alpha_1}$ - Rocket 1"
            )
            ax1.tick_params("y", colors="#ff7f0e")
            ax1.grid(True)

            ax1up = ax1.twinx()
            ax1up.plot(flightRocket1.alpha1[:, 0], flightRocket1.alpha1[:, 1], color="#1f77b4")
            ax1up.set_ylabel(
                "Angular Acceleration - ${\\alpha_1}$ (rad/s²)", color="#1f77b4"
            )
            ax1up.tick_params("y", colors="#1f77b4")

            ax2 = plt.subplot(322)
            ax2.plot(flightRocket2.w1[:, 0], flightRocket2.w1[:, 1], color="#ff7f0e")
            ax2.set_xlim(0, eventTime)
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Angular Velocity - ${\omega_1}$ (rad/s)", color="#ff7f0e")
            ax2.set_title(
                "Angular Velocity ${\omega_1}$ | Angular Acceleration ${\\alpha_1}$ - Rocket 2"
            )
            ax2.tick_params("y", colors="#ff7f0e")
            ax2.grid(True)

            ax2up = ax2.twinx()
            ax2up.plot(flightRocket2.alpha1[:, 0], flightRocket2.alpha1[:, 1], color="#1f77b4")
            ax2up.set_ylabel(
                "Angular Acceleration - ${\\alpha_1}$ (rad/s²)", color="#1f77b4"
            )
            ax2up.tick_params("y", colors="#1f77b4")

            ax3 = plt.subplot(323)
            ax3.plot(flightRocket1.w2[:, 0], flightRocket1.w2[:, 1], color="#ff7f0e")
            ax3.set_xlim(0, eventTime)
            ax3.set_xlabel("Time (s)")
            ax3.set_ylabel("Angular Velocity - ${\omega_2}$ (rad/s)", color="#ff7f0e")
            ax3.set_title(
                "Angular Velocity ${\omega_2}$ | Angular Acceleration ${\\alpha_2}$ - Rocket 1"
            )
            ax3.tick_params("y", colors="#ff7f0e")
            ax3.grid(True)

            ax3up = ax3.twinx()
            ax3up.plot(flightRocket1.alpha2[:, 0], flightRocket1.alpha2[:, 1], color="#1f77b4")
            ax3up.set_ylabel(
                "Angular Acceleration - ${\\alpha_2}$ (rad/s²)", color="#1f77b4"
            )
            ax3up.tick_params("y", colors="#1f77b4")

            ax4 = plt.subplot(324)
            ax4.plot(flightRocket2.w2[:, 0], flightRocket2.w2[:, 1], color="#ff7f0e")
            ax4.set_xlim(0, eventTime)
            ax4.set_xlabel("Time (s)")
            ax4.set_ylabel("Angular Velocity - ${\omega_2}$ (rad/s)", color="#ff7f0e")
            ax4.set_title(
                "Angular Velocity ${\omega_2}$ | Angular Acceleration ${\\alpha_2}$ - Rocket 2"
            )
            ax4.tick_params("y", colors="#ff7f0e")
            ax4.grid(True)

            ax4up = ax4.twinx()
            ax4up.plot(flightRocket2.alpha2[:, 0], flightRocket2.alpha2[:, 1], color="#1f77b4")
            ax4up.set_ylabel(
                "Angular Acceleration - ${\\alpha_2}$ (rad/s²)", color="#1f77b4"
            )
            ax4up.tick_params("y", colors="#1f77b4")

            ax5 = plt.subplot(325)
            ax5.plot(flightRocket1.w3[:, 0], flightRocket1.w3[:, 1], color="#ff7f0e")
            ax5.set_xlim(0, eventTime)
            ax5.set_xlabel("Time (s)")
            ax5.set_ylabel("Angular Velocity - ${\omega_3}$ (rad/s)", color="#ff7f0e")
            ax5.set_title(
                "Angular Velocity ${\omega_3}$ | Angular Acceleration ${\\alpha_3}$ - Rocket 1"
            )
            ax5.tick_params("y", colors="#ff7f0e")
            ax5.grid(True)

            ax5up = ax5.twinx()
            ax5up.plot(flightRocket1.alpha3[:, 0], flightRocket1.alpha3[:, 1], color="#1f77b4")
            ax5up.set_ylabel(
                "Angular Acceleration - ${\\alpha_3}$ (rad/s²)", color="#1f77b4"
            )
            ax5up.tick_params("y", colors="#1f77b4")

            ax6 = plt.subplot(326)
            ax6.plot(flightRocket2.w3[:, 0], flightRocket2.w3[:, 1], color="#ff7f0e")
            ax6.set_xlim(0, eventTime)
            ax6.set_xlabel("Time (s)")
            ax6.set_ylabel("Angular Velocity - ${\omega_3}$ (rad/s)", color="#ff7f0e")
            ax6.set_title(
                "Angular Velocity ${\omega_3}$ | Angular Acceleration ${\\alpha_3}$ - Rocket 2"
            )
            ax6.tick_params("y", colors="#ff7f0e")
            ax6.grid(True)

            ax6up = ax6.twinx()
            ax6up.plot(flightRocket2.alpha3[:, 0], flightRocket2.alpha3[:, 1], color="#1f77b4")
            ax6up.set_ylabel(
                "Angular Acceleration - ${\\alpha_3}$ (rad/s²)", color="#1f77b4"
            )
            ax6up.tick_params("y", colors="#1f77b4")

            plt.subplots_adjust(wspace=0.5,hspace=0.4)
            plt.show()

            return None

        def plotTrajectoryForceData(flightRocket1, flightRocket2):
            """Prints out all Forces and Moments graphs available about the Flight

            Parameters
            ----------
            None
            
            Return
            ------
            None
            """
            # Post-process results
            if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()
            if flightRocket2.postProcessed is False:
                flightRocket2.postProcess()

            # Get index of out of rail time
            outOfRailTimeIndexs1 = np.nonzero(flightRocket1.x[:, 0] == flightRocket1.outOfRailTime)
            outOfRailTimeIndex1 = -1 if len(outOfRailTimeIndexs1) == 0 else outOfRailTimeIndexs1[0][0]

            outOfRailTimeIndexs2 = np.nonzero(flightRocket2.x[:, 0] == flightRocket2.outOfRailTime)
            outOfRailTimeIndex2 = -1 if len(outOfRailTimeIndexs2) == 0 else outOfRailTimeIndexs2[0][0]

            # Get index of time before parachute event
                # Rocket 1:
            if len(flightRocket1.parachuteEvents) > 0:
                eventTime1 = flightRocket1.parachuteEvents[0][0] + flightRocket1.parachuteEvents[0][1].lag
                eventTimeIndex1 = np.nonzero(flightRocket1.x[:, 0] == eventTime1)[0][0]
            else:
                eventTime1 = flightRocket1.tFinal
                eventTimeIndex1 = -1

                # Rocket 2:
            if len(flightRocket2.parachuteEvents) > 0:
                eventTime2 = flightRocket2.parachuteEvents[0][0] + flightRocket2.parachuteEvents[0][1].lag
                eventTimeIndex2 = np.nonzero(flightRocket2.x[:, 0] == eventTime2)[0][0]
            else:
                eventTime2 = flightRocket2.tFinal
                eventTimeIndex2 = -1

            eventTime = max(eventTime1, eventTime2)
            
            # Rail Button Forces
            fig6 = plt.figure(figsize=(10, 8))

            ax1 = plt.subplot(221)
            ax1.plot(
                flightRocket1.railButton1NormalForce[:outOfRailTimeIndex1, 0],
                flightRocket1.railButton1NormalForce[:outOfRailTimeIndex1, 1],
                label="Upper Rail Button",
            )
            ax1.plot(
                flightRocket1.railButton2NormalForce[:outOfRailTimeIndex1, 0],
                flightRocket1.railButton2NormalForce[:outOfRailTimeIndex1, 1],
                label="Lower Rail Button",
            )
            ax1.set_xlim(0, flightRocket1.outOfRailTime)
            ax1.legend()
            ax1.grid(True)
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Normal Force (N)")
            ax1.set_title("Rail Buttons Normal Force - Rocket 1")

            ax2 = plt.subplot(222)
            ax2.plot(
                flightRocket2.railButton1NormalForce[:outOfRailTimeIndex2, 0],
                flightRocket2.railButton1NormalForce[:outOfRailTimeIndex2, 1],
                label="Upper Rail Button",
            )
            ax2.plot(
                flightRocket2.railButton2NormalForce[:outOfRailTimeIndex2, 0],
                flightRocket2.railButton2NormalForce[:outOfRailTimeIndex2, 1],
                label="Lower Rail Button",
            )
            ax2.set_xlim(0, flightRocket2.outOfRailTime)
            ax2.legend()
            ax2.grid(flightRocket2)
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Normal Force (N)")
            ax2.set_title("Rail Buttons Normal Force - Rocket 2")

            ax3 = plt.subplot(223)
            ax3.plot(
                flightRocket1.railButton1ShearForce[:outOfRailTimeIndex1, 0],
                flightRocket1.railButton1ShearForce[:outOfRailTimeIndex1, 1],
                label="Upper Rail Button",
            )
            ax3.plot(
                flightRocket1.railButton2ShearForce[:outOfRailTimeIndex1, 0],
                flightRocket1.railButton2ShearForce[:outOfRailTimeIndex1, 1],
                label="Lower Rail Button",
            )
            ax3.set_xlim(0, flightRocket1.outOfRailTime)
            ax3.legend()
            ax3.grid(True)
            ax3.set_xlabel("Time (s)")
            ax3.set_ylabel("Shear Force (N)")
            ax3.set_title("Rail Buttons Shear Force - Rocket 1")

            ax4 = plt.subplot(224)
            ax4.plot(
                flightRocket2.railButton1ShearForce[:outOfRailTimeIndex2, 0],
                flightRocket2.railButton1ShearForce[:outOfRailTimeIndex2, 1],
                label="Upper Rail Button",
            )
            ax4.plot(
                flightRocket2.railButton2ShearForce[:outOfRailTimeIndex2, 0],
                flightRocket2.railButton2ShearForce[:outOfRailTimeIndex2, 1],
                label="Lower Rail Button",
            )
            ax4.set_xlim(0, flightRocket2.outOfRailTime)
            ax4.legend()
            ax4.grid(True)
            ax4.set_xlabel("Time (s)")
            ax4.set_ylabel("Shear Force (N)")
            ax4.set_title("Rail Buttons Shear Force - Rocket 2")

            plt.subplots_adjust(hspace=0.5)
            plt.show()

            # Aerodynamic force and moment plots
            fig7 = plt.figure(figsize=(16, 12))

            ax1 = plt.subplot(421)
            ax1.plot(flightRocket1.aerodynamicLift[:eventTimeIndex1, 0], flightRocket1.aerodynamicLift[:eventTimeIndex1, 1], label='Resultant')
            ax1.plot(flightRocket1.R1[:eventTimeIndex1, 0], flightRocket1.R1[:eventTimeIndex1, 1], label='R1')
            ax1.plot(flightRocket1.R2[:eventTimeIndex1, 0], flightRocket1.R2[:eventTimeIndex1, 1], label='R2')
            ax1.set_xlim(0, eventTime)
            ax1.legend()
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Lift Force (N)")
            ax1.set_title("Aerodynamic Lift Resultant Force - Rocket 1")
            ax1.grid()

            ax2 = plt.subplot(422)
            ax2.plot(flightRocket2.aerodynamicLift[:eventTimeIndex2, 0], flightRocket2.aerodynamicLift[:eventTimeIndex2, 1], label='Resultant')
            ax2.plot(flightRocket2.R1[:eventTimeIndex2, 0], flightRocket2.R1[:eventTimeIndex2, 1], label='R1')
            ax2.plot(flightRocket2.R2[:eventTimeIndex2, 0], flightRocket2.R2[:eventTimeIndex2, 1], label='R2')
            ax2.set_xlim(0, eventTime)
            ax2.legend()
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Lift Force (N)")
            ax2.set_title("Aerodynamic Lift Resultant Force - Rocket 2")
            ax2.grid()

            ax3 = plt.subplot(423)
            ax3.plot(flightRocket1.aerodynamicDrag[:eventTimeIndex1, 0], flightRocket1.aerodynamicDrag[:eventTimeIndex1, 1])
            ax3.set_xlim(0, eventTime)
            ax3.set_xlabel("Time (s)")
            ax3.set_ylabel("Drag Force (N)")
            ax3.set_title("Aerodynamic Drag Force - Rocket 1")
            ax3.grid()

            ax4 = plt.subplot(424)
            ax4.plot(flightRocket2.aerodynamicDrag[:eventTimeIndex2, 0], flightRocket2.aerodynamicDrag[:eventTimeIndex2, 1])
            ax4.set_xlim(0, eventTime)
            ax4.set_xlabel("Time (s)")
            ax4.set_ylabel("Drag Force (N)")
            ax4.set_title("Aerodynamic Drag Force - Rocket 2")
            ax4.grid()

            ax5 = plt.subplot(425)
            ax5.plot(
                flightRocket1.aerodynamicBendingMoment[:eventTimeIndex1, 0],
                flightRocket1.aerodynamicBendingMoment[:eventTimeIndex1, 1],
                label='Resultant',
            )
            ax5.plot(flightRocket1.M1[:eventTimeIndex1, 0], flightRocket1.M1[:eventTimeIndex1, 1], label='M1')
            ax5.plot(flightRocket1.M2[:eventTimeIndex1, 0], flightRocket1.M2[:eventTimeIndex1, 1], label='M2')
            ax5.set_xlim(0, eventTime)
            ax5.legend()
            ax5.set_xlabel("Time (s)")
            ax5.set_ylabel("Bending Moment (N m)")
            ax5.set_title("Aerodynamic Bending Resultant Moment - Rocket 1")
            ax5.grid()

            ax6 = plt.subplot(426)
            ax6.plot(
                flightRocket2.aerodynamicBendingMoment[:eventTimeIndex2, 0],
                flightRocket2.aerodynamicBendingMoment[:eventTimeIndex2, 1],
                label='Resultant',
            )
            ax6.plot(flightRocket2.M1[:eventTimeIndex2, 0], flightRocket2.M1[:eventTimeIndex2, 1], label='M1')
            ax6.plot(flightRocket2.M2[:eventTimeIndex2, 0], flightRocket2.M2[:eventTimeIndex2, 1], label='M2')
            ax6.set_xlim(0, eventTime)
            ax6.legend()
            ax6.set_xlabel("Time (s)")
            ax6.set_ylabel("Bending Moment (N m)")
            ax6.set_title("Aerodynamic Bending Resultant Moment - Rocket 2")
            ax6.grid()

            ax7 = plt.subplot(427)
            ax7.plot(flightRocket1.aerodynamicSpinMoment[:eventTimeIndex1, 0], flightRocket1.aerodynamicSpinMoment[:eventTimeIndex1, 1])
            ax7.set_xlim(0, eventTime)
            ax7.set_xlabel("Time (s)")
            ax7.set_ylabel("Spin Moment (N m)")
            ax7.set_title("Aerodynamic Spin Moment - Rocket 1")
            ax7.grid()
            
            ax8 = plt.subplot(428)
            ax8.plot(flightRocket2.aerodynamicSpinMoment[:eventTimeIndex2, 0], flightRocket1.aerodynamicSpinMoment[:eventTimeIndex2, 1])
            ax8.set_xlim(0, eventTime)
            ax8.set_xlabel("Time (s)")
            ax8.set_ylabel("Spin Moment (N m)")
            ax8.set_title("Aerodynamic Spin Moment - Rocket 2")
            ax8.grid()

            plt.subplots_adjust(hspace=0.5)
            plt.show()

            return None
        
        def plotEnergyData(flightRocket1, flightRocket2):
            """Prints out all Energy components graphs available about the Flight

            Returns
            -------
            None
            """
            # Post-process results
            if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()
            if flightRocket2.postProcessed is False:
                flightRocket2.postProcess()

            # Get index of out of rail time
            outOfRailTimeIndexs1 = np.nonzero(flightRocket1.x[:, 0] == flightRocket1.outOfRailTime)
            outOfRailTimeIndex1 = -1 if len(outOfRailTimeIndexs1) == 0 else outOfRailTimeIndexs1[0][0]

            outOfRailTimeIndexs2 = np.nonzero(flightRocket2.x[:, 0] == flightRocket2.outOfRailTime)
            outOfRailTimeIndex2 = -1 if len(outOfRailTimeIndexs2) == 0 else outOfRailTimeIndexs2[0][0]

            # Get index of time before parachute event
                # Rocket 1:
            if len(flightRocket1.parachuteEvents) > 0:
                eventTime1 = flightRocket1.parachuteEvents[0][0] + flightRocket1.parachuteEvents[0][1].lag
                eventTimeIndex1 = np.nonzero(flightRocket1.x[:, 0] == eventTime1)[0][0]
            else:
                eventTime1 = flightRocket1.tFinal
                eventTimeIndex1 = -1

                # Rocket 2:
            if len(flightRocket2.parachuteEvents) > 0:
                eventTime2 = flightRocket2.parachuteEvents[0][0] + flightRocket2.parachuteEvents[0][1].lag
                eventTimeIndex2 = np.nonzero(flightRocket2.x[:, 0] == eventTime2)[0][0]
            else:
                eventTime2 = flightRocket2.tFinal
                eventTimeIndex2 = -1

            eventTime = max(eventTime1, eventTime2)
            
            fig8 = plt.figure(figsize=(12, 16))

            ax1 = plt.subplot(421)
            ax1.plot(
                flightRocket1.kineticEnergy[:, 0], flightRocket1.kineticEnergy[:, 1], label="Kinetic Energy"
            )
            ax1.plot(
                flightRocket1.rotationalEnergy[:, 0],
                flightRocket1.rotationalEnergy[:, 1],
                label="Rotational Energy",
            )
            ax1.plot(
                flightRocket1.translationalEnergy[:, 0],
                flightRocket1.translationalEnergy[:, 1],
                label="Translational Energy",
            )
            ax1.set_xlim(0, flightRocket1.apogeeTime)
            ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax1.set_title("Kinetic Energy Components - Rocket 1")
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Energy (J)")
            
            ax1.legend()
            ax1.grid()

            ax2 = plt.subplot(422)
            ax2.plot(
                flightRocket2.kineticEnergy[:, 0], flightRocket2.kineticEnergy[:, 1], label="Kinetic Energy"
            )
            ax2.plot(
                flightRocket2.rotationalEnergy[:, 0],
                flightRocket2.rotationalEnergy[:, 1],
                label="Rotational Energy",
            )
            ax2.plot(
                flightRocket2.translationalEnergy[:, 0],
                flightRocket2.translationalEnergy[:, 1],
                label="Translational Energy",
            )
            ax2.set_xlim(0, flightRocket2.apogeeTime)
            ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax2.set_title("Kinetic Energy Components - Rocket 2")
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Energy (J)")
            
            ax2.legend()
            ax2.grid()

            ax3 = plt.subplot(423)
            ax3.plot(flightRocket1.totalEnergy[:, 0], flightRocket1.totalEnergy[:, 1], label="Total Energy")
            ax3.plot(
                flightRocket1.kineticEnergy[:, 0], flightRocket1.kineticEnergy[:, 1], label="Kinetic Energy"
            )
            ax3.plot(
                flightRocket1.potentialEnergy[:, 0],
                flightRocket1.potentialEnergy[:, 1],
                label="Potential Energy",
            )
            ax3.set_xlim(0, flightRocket1.apogeeTime)
            ax3.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax3.set_title("Total Mechanical Energy Components - Rocket 1")
            ax3.set_xlabel("Time (s)")
            ax3.set_ylabel("Energy (J)")
            ax3.legend()
            ax3.grid()

            ax4 = plt.subplot(424)
            ax4.plot(flightRocket2.totalEnergy[:, 0], flightRocket2.totalEnergy[:, 1], label="Total Energy")
            ax4.plot(
                flightRocket2.kineticEnergy[:, 0], flightRocket2.kineticEnergy[:, 1], label="Kinetic Energy"
            )
            ax4.plot(
                flightRocket2.potentialEnergy[:, 0],
                flightRocket2.potentialEnergy[:, 1],
                label="Potential Energy",
            )
            ax4.set_xlim(0, flightRocket2.apogeeTime)
            ax4.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax4.set_title("Total Mechanical Energy Components - Rocket 2")
            ax4.set_xlabel("Time (s)")
            ax4.set_ylabel("Energy (J)")
            ax4.legend()
            ax4.grid()

            ax5 = plt.subplot(425)
            ax5.plot(flightRocket1.thrustPower[:, 0], flightRocket1.thrustPower[:, 1], label="|Thrust Power|")
            ax5.set_xlim(0, flightRocket1.rocket.motor.burnOutTime)
            ax5.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax5.set_title("Thrust Absolute Power - Rocket 1")
            ax5.set_xlabel("Time (s)")
            ax5.set_ylabel("Power (W)")
            ax5.legend()
            ax5.grid()

            ax6 = plt.subplot(426)
            ax6.plot(flightRocket2.thrustPower[:, 0], flightRocket2.thrustPower[:, 1], label="|Thrust Power|")
            ax6.set_xlim(0, flightRocket2.rocket.motor.burnOutTime)
            ax6.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax6.set_title("Thrust Absolute Power - Rocket 2")
            ax6.set_xlabel("Time (s)")
            ax6.set_ylabel("Power (W)")
            ax6.legend()
            ax6.grid()

            ax7 = plt.subplot(427)
            ax7.plot(flightRocket1.dragPower[:, 0], -flightRocket1.dragPower[:, 1], label="|Drag Power|")
            ax7.set_xlim(0, flightRocket1.apogeeTime)
            ax7.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax7.set_title("Drag Absolute Power - Rocket 1")
            ax7.set_xlabel("Time (s)")
            ax7.set_ylabel("Power (W)")
            ax7.legend()
            ax7.grid()

            ax8 = plt.subplot(428)
            ax8.plot(flightRocket2.dragPower[:, 0], -flightRocket2.dragPower[:, 1], label="|Drag Power|")
            ax8.set_xlim(0, flightRocket2.apogeeTime)
            ax8.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax8.set_title("Drag Absolute Power - Rocket 2")
            ax8.set_xlabel("Time (s)")
            ax8.set_ylabel("Power (W)")
            ax8.legend()
            ax8.grid()

            plt.subplots_adjust(wspace=0.3, hspace=0.5)
            plt.show()

            return None

        def plotFluidMechanicsData(flightRocket1, flightRocket2):
            """Prints out a summary of the Fluid Mechanics graphs available about 
            the Flight

            Parameters
            ----------
            None
            
            Return
            ------
            None
            """
            # Post-process results
            if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()
            if flightRocket2.postProcessed is False:
                flightRocket2.postProcess()

            # Get index of out of rail time
            outOfRailTimeIndexs1 = np.nonzero(flightRocket1.x[:, 0] == flightRocket1.outOfRailTime)
            outOfRailTimeIndex1 = -1 if len(outOfRailTimeIndexs1) == 0 else outOfRailTimeIndexs1[0][0]

            outOfRailTimeIndexs2 = np.nonzero(flightRocket2.x[:, 0] == flightRocket2.outOfRailTime)
            outOfRailTimeIndex2 = -1 if len(outOfRailTimeIndexs2) == 0 else outOfRailTimeIndexs2[0][0]

            
            # Trajectory Fluid Mechanics Plots
            fig10 = plt.figure(figsize=(12, 16))

            ax1 = plt.subplot(421)
            ax1.plot(flightRocket1.MachNumber[:, 0], flightRocket1.MachNumber[:, 1])
            ax1.set_xlim(0, flightRocket1.tFinal)
            ax1.set_title("Mach Number - Rocket 1")
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Mach Number")
            ax1.grid()

            ax2 = plt.subplot(422)
            ax2.plot(flightRocket2.MachNumber[:, 0], flightRocket2.MachNumber[:, 1])
            ax2.set_xlim(0, flightRocket2.tFinal)
            ax2.set_title("Mach Number - Rocket 2")
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Mach Number")
            ax2.grid()

            ax3 = plt.subplot(423)
            ax3.plot(flightRocket1.ReynoldsNumber[:, 0], flightRocket1.ReynoldsNumber[:, 1])
            ax3.set_xlim(0, flightRocket1.tFinal)
            ax3.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax3.set_title("Reynolds Number - Rocket 1")
            ax3.set_xlabel("Time (s)")
            ax3.set_ylabel("Reynolds Number")
            ax3.grid()

            ax4 = plt.subplot(424)
            ax4.plot(flightRocket2.ReynoldsNumber[:, 0], flightRocket2.ReynoldsNumber[:, 1])
            ax4.set_xlim(0, flightRocket2.tFinal)
            ax4.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax4.set_title("Reynolds Number - Rocket 2")
            ax4.set_xlabel("Time (s)")
            ax4.set_ylabel("Reynolds Number")
            ax4.grid()

            ax5 = plt.subplot(425)
            ax5.plot(
                flightRocket1.dynamicPressure[:, 0],
                flightRocket1.dynamicPressure[:, 1],
                label="Dynamic Pressure",
            )
            ax5.plot(
                flightRocket1.totalPressure[:, 0], flightRocket1.totalPressure[:, 1], label="Total Pressure"
            )
            ax5.plot(flightRocket1.pressure[:, 0], flightRocket1.pressure[:, 1], label="Static Pressure")
            ax5.set_xlim(0, flightRocket1.tFinal)
            ax5.legend()
            ax5.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax5.set_title("Total and Dynamic Pressure - Rocket 1")
            ax5.set_xlabel("Time (s)")
            ax5.set_ylabel("Pressure (Pa)")
            ax5.grid()

            ax6 = plt.subplot(426)
            ax6.plot(
                flightRocket2.dynamicPressure[:, 0],
                flightRocket2.dynamicPressure[:, 1],
                label="Dynamic Pressure",
            )
            ax6.plot(
                flightRocket2.totalPressure[:, 0], flightRocket2.totalPressure[:, 1], label="Total Pressure"
            )
            ax6.plot(flightRocket2.pressure[:, 0], flightRocket2.pressure[:, 1], label="Static Pressure")
            ax6.set_xlim(0, flightRocket2.tFinal)
            ax6.legend()
            ax6.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            ax6.set_title("Total and Dynamic Pressure - Rocket 2")
            ax6.set_xlabel("Time (s)")
            ax6.set_ylabel("Pressure (Pa)")
            ax6.grid()

            ax7 = plt.subplot(427)
            ax7.plot(flightRocket1.angleOfAttack[:, 0], flightRocket1.angleOfAttack[:, 1])
            ax7.set_xlim(flightRocket1.outOfRailTime, 10*flightRocket1.outOfRailTime)
            ax7.set_ylim(0, flightRocket1.angleOfAttack(flightRocket1.outOfRailTime))
            ax7.set_title("Angle of Attack - Rocket 1")
            ax7.set_xlabel("Time (s)")
            ax7.set_ylabel("Angle of Attack (°)")
            ax7.grid()

            ax8 = plt.subplot(428)
            ax8.plot(flightRocket2.angleOfAttack[:, 0], flightRocket2.angleOfAttack[:, 1])
            ax8.set_xlim(flightRocket2.outOfRailTime, 10*flightRocket2.outOfRailTime)
            ax8.set_ylim(0, flightRocket2.angleOfAttack(flightRocket2.outOfRailTime))
            ax8.set_title("Angle of Attack - Rocket 2")
            ax8.set_xlabel("Time (s)")
            ax8.set_ylabel("Angle of Attack (°)")
            ax8.grid()

            plt.subplots_adjust(wspace=0.3, hspace=0.5)
            plt.show()

            return None
        
        def plotStabilityAndControlData(flightRocket1, flightRocket2):
            """Prints out Rocket Stability and Control parameters graphs available 
            about the Flight

            Parameters
            ----------
            None
            
            Return
            ------
            None
            """
            # Post-process results
            if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()
            if flightRocket2.postProcessed is False:
                flightRocket2.postProcess()
            
            fig9 = plt.figure(figsize=(9, 12))

            ax1 = plt.subplot(221)
            ax1.plot(flightRocket1.staticMargin[:, 0], flightRocket1.staticMargin[:, 1])
            ax1.set_xlim(0, flightRocket1.staticMargin[:, 0][-1])
            ax1.set_title("Static Margin - Rocket 1")
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Static Margin (c)")
            ax1.grid()

            ax2 = plt.subplot(222)
            ax2.plot(flightRocket2.staticMargin[:, 0], flightRocket2.staticMargin[:, 1])
            ax2.set_xlim(0, flightRocket2.staticMargin[:, 0][-1])
            ax2.set_title("Static Margin - Rocket 2")
            ax2.set_xlabel("Time (s)")
            ax2.set_ylabel("Static Margin (c)")
            ax2.grid()

            ax3 = plt.subplot(223)
            maxAttitude = max(flightRocket1.attitudeFrequencyResponse[:, 1])
            maxAttitude = maxAttitude if maxAttitude != 0 else 1
            ax3.plot(
                flightRocket1.attitudeFrequencyResponse[:, 0],
                flightRocket1.attitudeFrequencyResponse[:, 1] / maxAttitude,
                label="Attitude Angle",
            )
            maxOmega1 = max(flightRocket1.omega1FrequencyResponse[:, 1])
            maxOmega1 = maxOmega1 if maxOmega1 != 0 else 1
            ax3.plot(
                flightRocket1.omega1FrequencyResponse[:, 0],
                flightRocket1.omega1FrequencyResponse[:, 1] / maxOmega1,
                label="$\omega_1$",
            )
            maxOmega2 = max(flightRocket1.omega2FrequencyResponse[:, 1])
            maxOmega2 = maxOmega2 if maxOmega2 != 0 else 1
            ax3.plot(
                flightRocket1.omega2FrequencyResponse[:, 0],
                flightRocket1.omega2FrequencyResponse[:, 1] / maxOmega2,
                label="$\omega_2$",
            )
            maxOmega3 = max(flightRocket1.omega3FrequencyResponse[:, 1])
            maxOmega3 = maxOmega3 if maxOmega3 != 0 else 1
            ax3.plot(
                flightRocket1.omega3FrequencyResponse[:, 0],
                flightRocket1.omega3FrequencyResponse[:, 1] / maxOmega3,
                label="$\omega_3$",
            )
            ax3.set_title("Frequency Response - Rocket 1")
            ax3.set_xlabel("Frequency (Hz)")
            ax3.set_ylabel("Amplitude Magnitude Normalized")
            ax3.set_xlim(0, 5)
            ax3.legend()
            ax3.grid()

            ax4 = plt.subplot(224)
            maxAttitude = max(flightRocket2.attitudeFrequencyResponse[:, 1])
            maxAttitude = maxAttitude if maxAttitude != 0 else 1
            ax4.plot(
                flightRocket2.attitudeFrequencyResponse[:, 0],
                flightRocket2.attitudeFrequencyResponse[:, 1] / maxAttitude,
                label="Attitude Angle",
            )
            maxOmega1 = max(flightRocket2.omega1FrequencyResponse[:, 1])
            maxOmega1 = maxOmega1 if maxOmega1 != 0 else 1
            ax4.plot(
                flightRocket2.omega1FrequencyResponse[:, 0],
                flightRocket2.omega1FrequencyResponse[:, 1] / maxOmega1,
                label="$\omega_1$",
            )
            maxOmega2 = max(flightRocket2.omega2FrequencyResponse[:, 1])
            maxOmega2 = maxOmega2 if maxOmega2 != 0 else 1
            ax4.plot(
                flightRocket2.omega2FrequencyResponse[:, 0],
                flightRocket2.omega2FrequencyResponse[:, 1] / maxOmega2,
                label="$\omega_2$",
            )
            maxOmega3 = max(flightRocket2.omega3FrequencyResponse[:, 1])
            maxOmega3 = maxOmega3 if maxOmega3 != 0 else 1
            ax4.plot(
                flightRocket2.omega3FrequencyResponse[:, 0],
                flightRocket2.omega3FrequencyResponse[:, 1] / maxOmega3,
                label="$\omega_3$",
            )
            ax4.set_title("Frequency Response - Rocket 2")
            ax4.set_xlabel("Frequency (Hz)")
            ax4.set_ylabel("Amplitude Magnitude Normalized")
            ax4.set_xlim(0, 5)
            ax4.legend()
            ax4.grid()

            plt.subplots_adjust(wspace=0.2, hspace=0.5)
            plt.show()

            return None

        def info(flight1,flight2):
            """Prints out a summary of the data available about the Flight.

            Parameters
            ----------
            None
            
            Return
            ------
            None
            """
            # Post-process results
            if flight1.postProcessed is False:
                flight1.postProcess()

            if flight2.postProcessed is False:
                flight2.postProcess()

            # Get index of out of rail time
                # Rocket 1
            outOfRailTimeIndexs1 = np.nonzero(flight1.x[:, 0] == flight1.outOfRailTime)
            outOfRailTimeIndex1 = (
                -1 if len(outOfRailTimeIndexs1) == 0 else outOfRailTimeIndexs1[0][0]
            )
                # Rocket 2
            outOfRailTimeIndexs2 = np.nonzero(flight2.x[:, 0] == flight2.outOfRailTime)
            outOfRailTimeIndex2 = (
                -1 if len(outOfRailTimeIndexs2) == 0 else outOfRailTimeIndexs2[0][0]
            )

            # Get index of time before parachute event

                # Rocket 1:
            if len(flight1.parachuteEvents) > 0:
                eventTime1 = flight1.parachuteEvents[0][0] + flight1.parachuteEvents[0][1].lag
                eventTimeIndex1 = np.nonzero(flight1.x[:, 0] == eventTime1)[0][0]
            else:
                eventTime1 = flight1.tFinal
                eventTimeIndex1 = -1
            
                # Rocket 2:
            if len(flight2.parachuteEvents) > 0:
                eventTime2 = flight2.parachuteEvents[0][0] + flight2.parachuteEvents[0][1].lag
                eventTimeIndex2 = np.nonzero(flight2.x[:, 0] == eventTime2)[0][0]
            else:
                eventTime2 = flight2.tFinal
                eventTimeIndex2 = -1

            # Print surface wind conditions

                # Rocket 1:
            print("Surface Wind Conditions - Rocket 1" + "     |     Surface Wind Conditions - Rocket 2\n")
            print("Frontal Surface Wind Speed: {:.2f} m/s".format(flight1.frontalSurfaceWind) + "         Frontal Surface Wind Speed: {:.2f} m/s".format(flight2.frontalSurfaceWind))
            print("Lateral Surface Wind Speed: {:.2f} m/s".format(flight1.lateralSurfaceWind) + "        Lateral Surface Wind Speed: {:.2f} m/s".format(flight2.lateralSurfaceWind))

                # Rocket 2
            #print("Surface Wind Conditions - Rocket 2\n")
            #print("Frontal Surface Wind Speed: {:.2f} m/s".format(flight2.frontalSurfaceWind))
            #print("Lateral Surface Wind Speed: {:.2f} m/s".format(flight2.lateralSurfaceWind))

            # Print of rail conditions

                # Rocket 1
            print("\n\nRail Departure State - Rocket 1" + "       |       Rail Departure State - Rocket 2\n")
            print(
                "Rail Departure Time: {:.3f} s".format(flight1.outOfRailTime) + 18*" " +
                "Rail Departure Time: {:.3f} s".format(flight2.outOfRailTime))
            print(
                "Rail Departure Velocity: {:.3f} m/s".format(flight1.outOfRailVelocity) + 11*" " +
                "Rail Departure Velocity: {:.3f} m/s".format(flight2.outOfRailVelocity)
                 )
            print(
                "Rail Departure Static Margin: {:.3f} c".format(
                    flight1.staticMargin(flight1.outOfRailTime)
                ) + 9*" " + "Rail Departure Static Margin: {:.3f} c".format(
                    flight2.staticMargin(flight1.outOfRailTime)
                )
            )
            print(
                "Rail Departure Angle of Attack: {:.3f}°".format(
                    flight1.angleOfAttack(flight1.outOfRailTime)
                ) + 8*" " + "Rail Departure Angle of Attack: {:.3f}°".format(
                    flight2.angleOfAttack(flight1.outOfRailTime)
                )
            )
            print(
                "Rail Departure Thrust-Weight Ratio: {:.3f}".format(
                flight1.rocket.thrustToWeight(flight1.outOfRailTime)) + 4*" "
                + "Rail Departure Thrust-Weight Ratio: {:.3f}".format(
                flight2.rocket.thrustToWeight(flight2.outOfRailTime)
                )
            )
            print(
                "Rail Departure Reynolds Number: {:.3e}".format(
                    flight1.ReynoldsNumber(flight1.outOfRailTime)) + 5*" "
                    + "Rail Departure Reynolds Number: {:.3e}".format(
                    flight2.ReynoldsNumber(flight2.outOfRailTime)
                )
            )

                # Rocket 2:
            #print("\n Rail Departure State - Rocket 2\n")
            #print("Rail Departure Time: {:.3f} s".format(flight2.outOfRailTime))
            #print("Rail Departure Velocity: {:.3f} m/s".format(flight2.outOfRailVelocity))
            #print(
            #    "Rail Departure Static Margin: {:.3f} c".format(
            #        flight2.staticMargin(flight1.outOfRailTime)
            #    )
            #)
            #print(
            #    "Rail Departure Angle of Attack: {:.3f}°".format(
            #        flight2.angleOfAttack(flight1.outOfRailTime)
            #    )
            #)
            #print(
            #    "Rail Departure Thrust-Weight Ratio: {:.3f}".format(
            #    flight2.rocket.thrustToWeight(flight2.outOfRailTime)
            #    )
            #)
            #print(
            #    "Rail Departure Reynolds Number: {:.3e}".format(
            #        flight2.ReynoldsNumber(flight2.outOfRailTime)
            #    )
            #)


            # Print burnOut conditions

                # Rocket 1:
            print("\n\nBurnOut State - Rocket 1\n")
            print("BurnOut time: {:.3f} s".format(flight1.rocket.motor.burnOutTime))
            print(
                "Altitude at burnOut: {:.3f} m (AGL)".format(
                flight1.z( flight1.rocket.motor.burnOutTime ) - flight1.env.elevation
                ) 
            )
            print("Rocket velocity at burnOut: {:.3f} m/s".format(
                flight1.speed( flight1.rocket.motor.burnOutTime )
                ) 
            )
            print(
                "Freestream velocity at burnOut: {:.3f} m/s".format(
                    (flight1.streamVelocityX( flight1.rocket.motor.burnOutTime )**2 + 
                    flight1.streamVelocityY( flight1.rocket.motor.burnOutTime )**2 + 
                    flight1.streamVelocityZ( flight1.rocket.motor.burnOutTime )**2)**0.5
                )
            )
            print(
                "Mach Number at burnOut: {:.3f}".format(
                    flight1.MachNumber( flight1.rocket.motor.burnOutTime))
            )
            print("Kinetic energy at burnOut: {:.3e} J".format(
                flight1.kineticEnergy(flight1.rocket.motor.burnOutTime)
                )
            )

                # Rocket 2:
            print("\nBurnOut State - Rocket 2\n")
            print("BurnOut time: {:.3f} s".format(flight2.rocket.motor.burnOutTime))
            print(
                "Altitude at burnOut: {:.3f} m (AGL)".format(
                flight2.z( flight2.rocket.motor.burnOutTime ) - flight2.env.elevation
                ) 
            )
            print("Rocket velocity at burnOut: {:.3f} m/s".format(
                flight2.speed( flight2.rocket.motor.burnOutTime )
                ) 
            )
            print(
                "Freestream velocity at burnOut: {:.3f} m/s".format(
                    (flight2.streamVelocityX( flight2.rocket.motor.burnOutTime )**2 + 
                    flight2.streamVelocityY( flight2.rocket.motor.burnOutTime )**2 + 
                    flight2.streamVelocityZ( flight2.rocket.motor.burnOutTime )**2)**0.5
                )
            )
            print(
                "Mach Number at burnOut: {:.3f}".format(
                    flight2.MachNumber( flight2.rocket.motor.burnOutTime))
            )
            print("Kinetic energy at burnOut: {:.3e} J".format(
                flight2.kineticEnergy( flight2.rocket.motor.burnOutTime)
                )
            )


            # Print apogee conditions

                # Rocket 1
            print("\n\nApogee - Rocket 1\n")
            print(
                "Apogee Altitude: {:.3f} m (ASL) | {:.3f} m (AGL)".format(
                    flight1.apogee, flight1.apogee - flight1.env.elevation
                )
            )
            print("Apogee Time: {:.3f} s".format(flight1.apogeeTime))
            print("Apogee Freestream Speed: {:.3f} m/s".format(flight1.apogeeFreestreamSpeed))

                # Rocket 2
            print("\nApogee - Rocket 2\n")
            print(
                "Apogee Altitude: {:.3f} m (ASL) | {:.3f} m (AGL)".format(
                    flight2.apogee, flight2.apogee - flight2.env.elevation
                )
            )
            print("Apogee Time: {:.3f} s".format(flight2.apogeeTime))
            print("Apogee Freestream Speed: {:.3f} m/s".format(flight2.apogeeFreestreamSpeed))


            # Print events registered

                # Rocket 1:
            print("\n\nEvents - Rocket 1\n")
            if len(flight1.parachuteEvents) == 0:
                print("No Parachute Events Were Triggered.")
            for event in flight1.parachuteEvents:
                triggerTime = event[0]
                parachute = event[1]
                openTime = triggerTime + parachute.lag
                velocity = flight1.freestreamSpeed(openTime)
                altitude = flight1.z(openTime)
                name = parachute.name.title()
                print(name + " Ejection Triggered at: {:.3f} s".format(triggerTime))
                print(name + " Parachute Inflated at: {:.3f} s".format(openTime))
                print(
                    name
                    + " Parachute Inflated with Freestream Speed of: {:.3f} m/s".format(
                        velocity
                    )
                )
                print(name + " Parachute Inflated at Height of: {:.3f} m (AGL)".format(altitude - flight1.env.elevation))

                # Rocket 2:
            print("\nEvents - Rocket 2\n")
            if len(flight2.parachuteEvents) == 0:
                print("No Parachute Events Were Triggered.")
            for event in flight2.parachuteEvents:
                triggerTime = event[0]
                parachute = event[1]
                openTime = triggerTime + parachute.lag
                velocity = flight2.freestreamSpeed(openTime)
                altitude = flight2.z(openTime)
                name = parachute.name.title()
                print(name + " Ejection Triggered at: {:.3f} s".format(triggerTime))
                print(name + " Parachute Inflated at: {:.3f} s".format(openTime))
                print(
                    name
                    + " Parachute Inflated with Freestream Speed of: {:.3f} m/s".format(
                        velocity
                    )
                )
                print(name + " Parachute Inflated at Height of: {:.3f} m (AGL)".format(altitude - self.env.elevation))

            # Print impact conditions

                # Rocket 1
            if len(flight1.impactState) != 0:
                print("\n\nImpact - Rocket 1\n")
                print("X Impact: {:.3f} m".format(flight1.xImpact))
                print("Y Impact: {:.3f} m".format(flight1.yImpact))
                print("Time of Impact: {:.3f} s".format(flight1.tFinal))
                print("Velocity at Impact: {:.3f} m/s".format(flight1.impactVelocity))
            elif flight1.terminateOnApogee is False:
                print("\n\nEnd of Simulation - Rocket 2\n")
                print("Time: {:.3f} s".format(flight1.solution[-1][0]))
                print("Altitude: {:.3f} m".format(flight1.solution[-1][3]))
            
                # Rocket 2
            if len(flight2.impactState) != 0:
                print("\nImpact - Rocket 2\n")
                print("X Impact: {:.3f} m".format(flight2.xImpact))
                print("Y Impact: {:.3f} m".format(flight2.yImpact))
                print("Time of Impact: {:.3f} s".format(flight2.tFinal))
                print("Velocity at Impact: {:.3f} m/s".format(flight2.impactVelocity))
            elif flight2.terminateOnApogee is False:
                print("\nEnd of Simulation - Rocket 2\n")
                print("Time: {:.3f} s".format(flight2.solution[-1][0]))
                print("Altitude: {:.3f} m".format(flight2.solution[-1][3]))


            # Print maximum values

                # Rocket 1
            print("\n\nMaximum Values - Rocket 1\n")
            print(
                "Maximum Speed: {:.3f} m/s at {:.2f} s".format(
                    flight1.maxSpeed, flight1.maxSpeedTime
                )
            )
            print(
                "Maximum Mach Number: {:.3f} Mach at {:.2f} s".format(
                    flight1.maxMachNumber, flight1.maxMachNumberTime
                )
            )
            print(
                "Maximum Reynolds Number: {:.3e} at {:.2f} s".format(
                    flight1.maxReynoldsNumber, flight1.maxReynoldsNumberTime
                )
            )
            print(
                "Maximum Dynamic Pressure: {:.3e} Pa at {:.2f} s".format(
                    flight1.maxDynamicPressure, flight1.maxDynamicPressureTime
                )
            )
            print(
                "Maximum Acceleration: {:.3f} m/s² at {:.2f} s".format(
                    flight1.maxAcceleration, flight1.maxAccelerationTime
                )
            )
            print(
                "Maximum Gs: {:.3f} g at {:.2f} s".format(
                    flight1.maxAcceleration / flight1.env.g, flight1.maxAccelerationTime
                )
            )
            print(
                "Maximum Upper Rail Button Normal Force: {:.3f} N".format(
                    flight1.maxRailButton1NormalForce
                )
            )
            print(
                "Maximum Upper Rail Button Shear Force: {:.3f} N".format(
                    flight1.maxRailButton1ShearForce
                )
            )
            print(
                "Maximum Lower Rail Button Normal Force: {:.3f} N".format(
                    flight1.maxRailButton2NormalForce
                )
            )
            print(
                "Maximum Lower Rail Button Shear Force: {:.3f} N".format(
                    flight1.maxRailButton2ShearForce
                )
            )

                # Rocket 2
            print("\n\nMaximum Values - Rocket 2\n")
            print(
                "Maximum Speed: {:.3f} m/s at {:.2f} s".format(
                    flight2.maxSpeed, flight2.maxSpeedTime
                )
            )
            print(
                "Maximum Mach Number: {:.3f} Mach at {:.2f} s".format(
                    flight2.maxMachNumber, flight2.maxMachNumberTime
                )
            )
            print(
                "Maximum Reynolds Number: {:.3e} at {:.2f} s".format(
                    flight2.maxReynoldsNumber, flight2.maxReynoldsNumberTime
                )
            )
            print(
                "Maximum Dynamic Pressure: {:.3e} Pa at {:.2f} s".format(
                    flight2.maxDynamicPressure, flight2.maxDynamicPressureTime
                )
            )
            print(
                "Maximum Acceleration: {:.3f} m/s² at {:.2f} s".format(
                    flight2.maxAcceleration, flight2.maxAccelerationTime
                )
            )
            print(
                "Maximum Gs: {:.3f} g at {:.2f} s".format(
                    flight2.maxAcceleration / flight2.env.g, flight2.maxAccelerationTime
                )
            )
            print(
                "Maximum Upper Rail Button Normal Force: {:.3f} N".format(
                    flight2.maxRailButton1NormalForce
                )
            )
            print(
                "Maximum Upper Rail Button Shear Force: {:.3f} N".format(
                    flight2.maxRailButton1ShearForce
                )
            )
            print(
                "Maximum Lower Rail Button Normal Force: {:.3f} N".format(
                    flight2.maxRailButton2NormalForce
                )
            )
            print(
                "Maximum Lower Rail Button Shear Force: {:.3f} N".format(
                    flight2.maxRailButton2ShearForce
                )
            )

            return None

        # Post-process results
        if flightRocket1.postProcessed is False:
                flightRocket1.postProcess()

        if flightRocket2.postProcessed is False:
            flightRocket2.postProcess()

        #Print initial conditions
        print("Initial Conditions - Rocket 1\n")
        flightRocket1.printInitialConditionsData()

        print("\nInitial Conditions - Rocket 2\n")
        flightRocket1.printInitialConditionsData()

        # Print launch rail orientation
        print("\n\nLaunch Rail Orientation - Rocket 1\n")
        print("Launch Rail Inclination: {:.2f}°".format(flightRocket1.inclination))
        print("Launch Rail Heading: {:.2f}°".format(flightRocket1.heading))

        print("\nLaunch Rail Orientation - Rocket 2\n")
        print("Launch Rail Inclination: {:.2f}°".format(flightRocket2.inclination))
        print("Launch Rail Heading: {:.2f}°\n\n".format(flightRocket2.heading))

        # Print a summary of data about the flight
        info(flightRocket1, flightRocket2)

        print("\n\nNumerical Integration Information - Rocket 1\n")
        flightRocket1.printNumericalIntegrationSettings()

        print("\nNumerical Integration Information  - Rocket 2\n")
        flightRocket2.printNumericalIntegrationSettings()

        print("\n\nTrajectory 3d Plot\n")
        plot3dTrajectory(flightRocket1, flightRocket2)

        print("\n\nTrajectory Kinematic Plots\n")
        print("Rocket 1:")
        flightRocket1.plotLinearKinematicsData()

        print("\nRocket 2:")
        flightRocket2.plotLinearKinematicsData()

        print("\n\nAngular Position Plots\n")
        plotFlightPathAngleData(flightRocket1, flightRocket2)

        print("\n\nPath, Attitude and Lateral Attitude Angle plots\n")
        plotAttitudeData(flightRocket1, flightRocket2)

        print("\n\nTrajectory Angular Velocity and Acceleration Plots\n")
        plotAngularKinematicsData(flightRocket1, flightRocket2)

        print("\n\nTrajectory Force Plots\n")
        plotTrajectoryForceData(flightRocket1, flightRocket2)

        print("\n\nTrajectory Energy Plots\n")
        plotEnergyData(flightRocket1, flightRocket2)

        print("\n\nTrajectory Fluid Mechanics Plots\n")
        plotFluidMechanicsData(flightRocket1, flightRocket2)

        print("\n\nTrajectory Stability and Control Plots\n")
        plotStabilityAndControlData(flightRocket1, flightRocket2)


        return None




    def plotProBrunão(self, rocketList):
        """receives a list of rockets and does a thing"""

        flightList = []
        for rocket in rocketList:
            flightRocket = Flight(rocket, self.env, inclination=85, heading=0)
            flightList.append(flightRocket)
            
        def plotAngularKinematicsData(flightList):
                """Prints out all Angular veolcity and acceleration graphs available
                about the Flight

                Parameters
                ----------
                None
                
                Return
                ------
                None
                """
                # Post-process results
                for flight in flightList:
                    if flight.postProcessed is False:
                        flight.postProcess()

                # Get index of time before parachute event

                eventTimeList = []
                for flight in flightList:
                    if len(flight.parachuteEvents) > 0:
                        eventTime = flight.parachuteEvents[0][0] + flight.parachuteEvents[0][1].lag
                        eventTimeIndex = np.nonzero(flight.x[:, 0] == eventTime)[0][0]
                    else:
                        eventTime = flight.tFinal
                        eventTimeIndex = -1
                    eventTimeList.append(eventTime)
                
                eventTime = max(eventTimeList)
                
                # Angular velocity and acceleration plots
                fig4 = plt.figure(figsize=(12, 9))

                ax5 = plt.subplot(111)
                a = 1
                for flight in flightList:
                    a += 1
                    ax5.plot(flight.w3[:, 0], flight.w3[:, 1], label='Rocket %d'%(a))
                ax5.set_xlim(0, eventTime)
                ax5.set_xlabel("Time (s)")
                ax5.set_ylabel("Angular Velocity - ${\omega_3}$ (rad/s)", color="#ff7f0e")
                ax5.set_title(
                    "Angular Velocity ${\omega_3}$ | Angular Acceleration ${\\alpha_3}$"
                )
                ax5.tick_params("y", colors="#ff7f0e")
                ax5.grid(True)

                ax5up = ax5.twinx()
                a = 1
                for flight in flightList:
                    a += 1
                    ax5up.plot(flight.alpha3[:, 0], flight.alpha3[:, 1], label='Rocket %d'%(a))
                ax5up.set_ylabel(
                    "Angular Acceleration - ${\\alpha_3}$ (rad/s²)", color="#1f77b4"
                )
                ax5up.tick_params("y", colors="#1f77b4")

                ax5.legend()
                ax5up.legend()
                plt.show()

                return None
        plotAngularKinematicsData(flightList)
        return None