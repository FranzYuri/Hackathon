# -*- coding: utf-8 -*-

__author__ = "Projeto Jupiter"
__copyright__ = "Copyright 20XX, Projeto Jupiter"
__license__ = "MIT"

import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import normal, uniform, choice
from datetime import datetime
import glob
from imageio import imread
from matplotlib.patches import Ellipse
from rocketpy import Environment, Function, Flight, Rocket, SolidMotor

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
        self.lat = 0
        self.lon = 0
        self.impact_ellipses = None

    def exportElipsesToKML(self, filename):
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

        for impactEll in self.impact_ellipses:
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
                lat1 = math.radians(self.lat) # Origin lat point converted to radians
                lon1 = math.radians(self.lon) # Origin long point converted to radians
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
        
    def Apogee_By_RocketMass(self, lower_bound_mass, upper_bound_mass, numPoints):
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
                
    def dispertion(self, iterationsNumber, analysis_parameters, rocketname, filename, thrustSource, main=False, drogue=False, sysRec=False, maxTime=600):
        """Hey! I'll document this later"""
        
        def ellipses():
            # Retrieve dispersion data por apogee and impact XY position
            apogeeX = np.array(dispersion_results['apogeeX'])
            apogeeY = np.array(dispersion_results['apogeeY'])
            impactX = np.array(dispersion_results['impactX'])
            impactY = np.array(dispersion_results['impactY'])

            # Define function to calculate eigen values
            def eigsorted(cov):
                vals, vecs = np.linalg.eigh(cov)
                order = vals.argsort()[::-1]
                return vals[order], vecs[:,order]
            
            # Create plot figure
            plt.figure(num=None, figsize=(12, 9), dpi=150, facecolor='w', edgecolor='k')
            ax = plt.subplot(111)

            # Calculate error ellipses for impact
            impactCov = np.cov(impactX, impactY)
            impactVals, impactVecs = eigsorted(impactCov)
            impactTheta = np.degrees(np.arctan2(*impactVecs[:,0][::-1]))
            impactW, impactH = 2 * np.sqrt(impactVals)

            # Draw error ellipses for impact
            impact_ellipses = []
            for j in [1, 2, 3]:
                impactEll = Ellipse(xy=(np.mean(impactX), np.mean(impactY)),
                            width=impactW*j, height=impactH*j,
                            angle=impactTheta, color='black')
                impactEll.set_facecolor((1, 0, 0, 0.2))
                impact_ellipses.append(impactEll)
                ax.add_artist(impactEll)

            # Calculate error ellipses for apogee
            apogeeCov = np.cov(apogeeX, apogeeY)
            apogeeVals, apogeeVecs = eigsorted(apogeeCov)
            apogeeTheta = np.degrees(np.arctan2(*apogeeVecs[:,0][::-1]))
            apogeeW, apogeeH = 2 * np.sqrt(apogeeVals)

            # Draw error ellipses for apogee
            for j in [1, 2, 3]:
                apogeeEll = Ellipse(xy=(np.mean(apogeeX), np.mean(apogeeY)),
                            width=apogeeW*j, height=apogeeH*j,
                            angle=apogeeTheta, color='black')
                apogeeEll.set_facecolor((0, 0, 1, 0.2))
                # ax.add_artist(apogeeEll)
                

            # Draw apogee points
            # plt.scatter(apogeeX, apogeeY, s=1)
                
            # Draw impact points
            plt.scatter(impactX, impactY, s=1)

            # Draw launch point
            plt.scatter(0, 0, s=10, color='black')

            #Add title and labels to plot
            ax.set_title('Elipses de 1σ, 2σ e 3σ do Ponto de Impacto - Pandia DROGUE H10')
            ax.set_ylabel('Norte (m)')
            ax.set_xlabel('Leste (m)')

            # Add background image to plot
            #-------------------------------------------------------------------
            #-------------------------------------------------------------------
            #-------------------------------------------------------------------
            #-------------------------------------------------------------------
            # MEXER AQUI PARA TRANSLADAR A IMAGEM EM RELAÇÃO A ORIGEM!!!!!!!!!!!
            dx = 0 # Translação Leste Oeste
            dy = 0 # Translação Norte Sul
            #-------------------------------------------------------------------
            #-------------------------------------------------------------------
            #-------------------------------------------------------------------
            #-------------------------------------------------------------------

            # Calculate probability of rocket being out of 3-sigma error ellipse for impact
            cos_angle = np.cos(np.radians(180.-impactTheta))
            sin_angle = np.sin(np.radians(180.-impactTheta))

            xc = impactX - np.mean(impactX)
            yc = impactY - np.mean(impactY)

            xct = xc * cos_angle - yc * sin_angle
            yct = xc * sin_angle + yc * cos_angle 

            n=3
            rad_cc = (xct**2/(n*impactW/2.)**2) + (yct**2/(n*impactH/2.)**2)

            colors_array = []
            count = 0

            for r in rad_cc:
                if r <= 1.:
                    # point in ellipse
                    colors_array.append('red')
                    count+=1
                else:
                    # point not in ellipse
                    colors_array.append('blue')
                    
            print("Probability of Impact out of Error Ellipses: " + "{:.3f}".format(100 - 100*count/len(impactX)) + " %")
            #plt.savefig (str(filename)+ '.png')
            plt.show()
                    

        def flight_settings(analysis_parameters, iterationsNumber):
            i = 0
            while i < iterationsNumber:
                # Generate a flight setting
                flight_setting = {}
                for parameter_key, parameter_value in analysis_parameters.items():
                    if type(parameter_value) is tuple:
                        flight_setting[parameter_key] =  normal(*parameter_value)
                    else:
                        flight_setting[parameter_key] =  choice(parameter_value)
                # Update counter
                i += 1
                # Yield a flight setting
                yield flight_setting

        dispersion_error_file = open(str(filename)+'.' + str(rocketname) + '.txt', 'a')
        dispersion_input_file = open(str(filename)+'.' + str(rocketname) + '_disp_in.txt', 'a')
        dispersion_output_file = open(str(filename)+'.' + str(rocketname) + '_disp_out.txt', 'a')

        def export_flight_data(flight_setting, flight_data):
            # Generate flight results
            flight_result = {"outOfRailTime": flight_data.outOfRailTime,
                        "outOfRailVelocity": flight_data.outOfRailVelocity,
                                "apogeeTime": flight_data.apogeeTime,
                            "apogeeAltitude": flight_data.apogee - Env.elevation,
                                "apogeeX": flight_data.apogeeX,
                                "apogeeY": flight_data.apogeeY,
                                "impactTime": flight_data.tFinal,
                                "impactX": flight_data.xImpact,
                                "impactY": flight_data.yImpact,
                            "impactVelocity": flight_data.impactVelocity,
                    "initialStaticMargin": flight_data.rocket.staticMargin(0),
                    "outOfRailStaticMargin": flight_data.rocket.staticMargin(TestFlight.outOfRailTime),
                        "finalStaticMargin": flight_data.rocket.staticMargin(TestFlight.rocket.motor.burnOutTime),
                            "numberOfEvents": len(flight_data.parachuteEvents)}
            
            # Calculate maximum reached velocity
            sol = np.array(flight_data.solution)
            flight_data.vx = Function(sol[:, [0, 4]], 'Time (s)', 'Vx (m/s)', 'linear', extrapolation="natural")
            flight_data.vy = Function(sol[:, [0, 5]], 'Time (s)', 'Vy (m/s)', 'linear', extrapolation="natural")
            flight_data.vz = Function(sol[:, [0, 6]], 'Time (s)', 'Vz (m/s)', 'linear', extrapolation="natural")
            flight_data.v = (flight_data.vx**2 + flight_data.vy**2 + flight_data.vz**2)**0.5
            flight_data.maxVel = np.amax(flight_data.v.source[:, 1])
            flight_result['maxVelocity'] = flight_data.maxVel
            
            # Take care of parachute results
            if len(flight_data.parachuteEvents) > 0:
                flight_result['drogueTriggerTime'] = flight_data.parachuteEvents[0][0]
                flight_result['drogueInflatedTime'] = flight_data.parachuteEvents[0][0] + flight_data.parachuteEvents[0][1].lag
                flight_result['drogueInflatedVelocity'] = flight_data.v(flight_data.parachuteEvents[0][0] + flight_data.parachuteEvents[0][1].lag)
            else:
                flight_result['drogueTriggerTime'] = 0
                flight_result['drogueInflatedTime'] = 0
                flight_result['drogueInflatedVelocity'] = 0
            
            # Write flight setting and results to file
            dispersion_input_file.write(str(flight_setting) + '\n')
            dispersion_input_file.flush()
            dispersion_output_file.write(str(flight_result) + '\n')
            dispersion_output_file.flush()
            #os.fsync(dispersion_output_file)

        def export_flight_error(flight_setting):
            dispersion_error_file.write(str(flight_setting) + '\n')
            dispersion_error_file.flush()


        # Initialize counter and timer
        i = 0
        initial_time = datetime.now()

        Env = Environment(railLength= self.env.rL,     
                        gravity = self.env.g,
                        date=self.env.date,  
                        latitude = self.env.lat, 
                        longitude = self.env.lon)
        #Env.setAtmosphericModel(type='Ensemble', file='GEFS')
        Env.setElevation(self.env.elevation)
        Env.maxExpectedHeight = self.env.maxExpectedHeight

        # Iterate over flight settings
        for setting in flight_settings(analysis_parameters, iterationsNumber):
            # Print current iteration
            i += 1
            print("Curent iteration: ", i, " | Average Time per Iteration: {:2.6f} s".format((datetime.now() - initial_time).seconds/i))
            
            # Create environment
            #self.env.selectEnsembleMember(i%21)
            Env.railLength = setting['railLength']
            Env.windVelocityX = Env.windVelocityX*setting['windX']
            Env.windVelocityY = Env.windVelocityY*setting['windY']

            # Create motor
            Motor =  SolidMotor(thrustSource = thrustSource,
                        burnOut=self.rocket.motor.burnOutTime,
                        reshapeThrustCurve=(setting['burnOut'], setting['impulse']),
                        nozzleRadius=setting['nozzleRadius'],
                        throatRadius=setting['throatRadius'],
                        grainNumber=self.rocket.motor.grainNumber,
                        grainSeparation=setting['grainSeparation'],
                        grainDensity=setting['grainDensity'],
                        grainOuterRadius=setting['grainOuterRadius'],
                        grainInitialInnerRadius=setting['grainInitialInnerRadius'],
                        grainInitialHeight=setting['grainInitialHeight'],
                        interpolationMethod='linear')
            
            # Create rocket
            rocketModel = Rocket(motor=Motor,
                            radius=setting['radius'],
                            mass=setting['m_aero'] + setting['m_se'] + setting['m_rec'] + setting['m_prop'],
                            inertiaI=setting['inertiaI'],
                            inertiaZ=setting['inertiaZ'],
                            distanceRocketNozzle=setting['distanceRocketNozzle'],
                            distanceRocketPropellant=setting['distanceRocketPropellant'],
                            powerOffDrag=self.rocket.powerOffDrag,
                            powerOnDrag=self.rocket.powerOnDrag)
            
            # Edit rocket drag
            rocketModel.powerOffDrag *= setting["powerOffDrag"]
            rocketModel.powerOnDrag *= setting["powerOnDrag"]
            
            # Add rocket nose, fins and tail
            NoseCone = rocketModel.addNose(length=setting['noseLength'], kind='vonKarman', distanceToCM=setting['noseDistanceToCM'])
            FinSet = rocketModel.addFins(n=3, rootChord=setting['finRootChord'], tipChord=setting['finTipChord'], span=setting['finSpan'], distanceToCM=setting['finDistanceToCM'])
            
            #Posição_CM_descarregado = rocketModel.CMToNosecone  
            rocketModel.railButtons = self.rocket.railButtons

            # Add parachute
            if drogue:
                for parachute in self.rocket.parachutes:
                    if parachute.name == 'Drogue' or  parachute.name == 'drogue': 
                        Drogue = rocketModel.addParachute('Drogue',
                                                            CdS=setting['CdSDrogue'],
                                                            trigger=parachute.trigger, 
                                                            samplingRate=105,
                                                            lag=setting['lag_rec'] + setting['lag_se'],
                                                            noise=(0, 8.3, 0.5))

            if main:
                for parachute in self.rocket.parachutes:
                    if parachute.name == 'Main' or  parachute.name == 'main': 
                        Main = rocketModel.addParachute('Main',
                                                        CdS=setting['CdSMain'],
                                                        trigger=parachute.trigger, 
                                                        samplingRate=105,
                                                        noise=(0, 8.3, 0.5),
                                                        lag=setting['lag_rec'] + setting['lag_se'])
           
            if sysRec:
                # Prepare parachutes
                sisRecDrogue.reset()
                sisRecDrogue.enable()
                sisRecMain.reset()
                sisRecMain.enable()

            if setting['CdSDrogue'] > 0 and setting['CdSMain'] > 0 and setting['lag_rec'] + setting['lag_se'] > 0:
                try:
                    # Simulate flight
                    TestFlight = Flight(rocket=rocketModel, environment=Env, inclination=setting['inclination'], heading=setting['heading'], maxTime=maxTime)
                    
                    #TestFlight.info()
                    # Export flight results
                    export_flight_data(setting, TestFlight)
                except IndexError:
                    # Export flight errors
                    export_flight_error(flight_setting)
            else:
                print('ERROR! Negative values not allowed for CdSDrogue, CdSMain and lag_rec+lag_se in ', flight_setting)


        # Initialize variable to store all results
        dispersion_general_results = []

        dispersion_results = {"outOfRailTime": [],
                        "outOfRailVelocity": [],
                                "apogeeTime": [],
                            "apogeeAltitude": [],
                                    "apogeeX": [],
                                    "apogeeY": [],
                                "impactTime": [],
                                    "impactX": [],
                                    "impactY": [],
                            "impactVelocity": [],
                        "initialStaticMargin": [],
                    "outOfRailStaticMargin": [],
                        "finalStaticMargin": [],
                            "numberOfEvents": [],
                                "maxVelocity": [],
                        "drogueTriggerTime": [],
                        "drogueInflatedTime": [],
                    "drogueInflatedVelocity": []}

        # Get all dispersion results
        for filename in glob.iglob(str(filename)+'.' + str(rocketname) + '_disp_out.txt'):
            # Get file
            dispersion_output_file = open(filename, 'r+')
            
            # Read each line of the file and convert to dict
            for line in dispersion_output_file:
                if line[0] == '{':
                    flight_result = eval(line)

                    # Store general result
                    # if flight_result['apogeeAltitude']  > 650:
                    dispersion_general_results.append(flight_result)
                    # Store result by type
                    for parameter_key, parameter_value in flight_result.items():
                        dispersion_results[parameter_key].append(parameter_value)

            # Close data file
            dispersion_output_file.close()

        # Creating end of file
        # dispersion_output_file.write ("Name Mean Value | Standard Deviation" + '\n')

        # Print number of flights simulated
        N = len(dispersion_general_results)
        print('Number of simulations: ', N)

        ellipses()