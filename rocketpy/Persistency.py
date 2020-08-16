import textwrap

import numpy as np
from lambdaJSON import lambdaJSON


from .Environment import Environment
from .Flight import Flight
from .Rocket import Rocket
from .SolidMotor import SolidMotor

def exportSimulation(filename, environment, solidMotor, rocket, flight):
    """Export simulation inputs to rpy file

    Parameters
    ----------
    filename : string
        Name of the file to export
    environment : Environment
        Simulation environment
    solidMotor : SolidMotor
        Rocket motor
    rocket : Rocket
        Simulation rocket
    flight : Flight
        Simulation flight
    """
    lj = lambdaJSON(globs = (lambda: globals()))

    exportText = "\n\"Environment\": " + lj.dumps(environment.exportEnvironment(), indent=4) + ", \n" + "\"SolidMotor\": " + lj.dumps(solidMotor.exportSolidMotor(), indent=4) + ", \n" + "\"Rocket\": " + lj.dumps(rocket.exportRocket(), indent=4) + ", \n" +  "\"Flight\": " + lj.dumps(flight.exportFlight(), indent=4) + "\n"

    exportText = "{" + textwrap.indent(exportText, "    ") + "}"

    with open(filename, "w") as write_file:
        write_file.write(exportText)

def importSimulation(filename, verbose=False):
    """Import simulation inputs from rpy file

    Parameters
    ----------
    filename : string
        Name of the file to import
    verbose : bool, optional
        If True prints extra information about the simulation, by default False

    Returns
    -------
    Environment, SolidMotor, Rocket, Flight
        Simulation objects
    """
    lj = lambdaJSON(globs = (lambda: globals()))

    with open(filename, "r") as read_file:
        file_contents = read_file.read()

    data = lj.loads(file_contents)

    environment = Environment(
        railLength=data["Environment"]["railLength"],
        gravity=data["Environment"]["gravity"],
        date=tuple(data["Environment"]["date"]),
        latitude=data["Environment"]["latitude"],
        longitude=data["Environment"]["longitude"],
        elevation=data["Environment"]["elevation"]
    )

    environment.setAtmosphericModel(
        type=data["Environment"]["atmosphericModelType"],
        file=data["Environment"]["atmosphericModelFile"],
        dictionary=data["Environment"]["atmosphericModelDictionary"],
        pressure=data["Environment"]["atmosphericModelPressure"],
        temperature=data["Environment"]["atmosphericModelTemperature"],
        wind_u=data["Environment"]["wind_u"],
        wind_v=data["Environment"]["wind_v"]
    )

    if verbose:
        environment.info()


    solidMotor = SolidMotor(
        thrustSource=data["SolidMotor"]["thrustSource"],
        burnOut=data["SolidMotor"]["burnOut"],
        grainNumber=data["SolidMotor"]["grainNumber"],
        grainDensity=data["SolidMotor"]["grainDensity"],
        grainOuterRadius=data["SolidMotor"]["grainOuterRadius"],
        grainInitialInnerRadius=data["SolidMotor"]["grainInitialInnerRadius"],
        grainInitialHeight=data["SolidMotor"]["grainInitialHeight"],
        grainSeparation=data["SolidMotor"]["grainSeparation"],
        nozzleRadius=data["SolidMotor"]["nozzleRadius"],
        throatRadius=data["SolidMotor"]["throatRadius"],
        reshapeThrustCurve=data["SolidMotor"]["reshapeThrustCurve"],
        interpolationMethod=data["SolidMotor"]["interpolationMethod"]
    )

    if verbose:
        solidMotor.info()
    
    rocket = Rocket(
        motor=solidMotor,
        mass=data["Rocket"]["mass"],
        inertiaI=data["Rocket"]["inertiaI"],
        inertiaZ=data["Rocket"]["inertiaZ"],
        radius=data["Rocket"]["radius"],
        distanceRocketNozzle=data["Rocket"]["distanceRocketNozzle"],
        distanceRocketPropellant=data["Rocket"]["distanceRocketPropellant"],
        powerOffDrag=data["Rocket"]["powerOffDrag"],
        powerOnDrag=data["Rocket"]["powerOnDrag"],
    )

    
    rocket.setRailButtons(data["Rocket"]["railButtons"])

    rocket.addNose(
        length=data["Rocket"]["NoseCone"]["length"],
        kind=data["Rocket"]["NoseCone"]["kind"],
        distanceToCM=data["Rocket"]["NoseCone"]["distanceToCM"]
    )

    rocket.addFins(
        n=data["Rocket"]["FinSet"]["nFins"],
        span=data["Rocket"]["FinSet"]["span"],
        rootChord=data["Rocket"]["FinSet"]["rootChord"],
        tipChord=data["Rocket"]["FinSet"]["tipChord"],
        distanceToCM=data["Rocket"]["FinSet"]["distanceToCM"],
        radius=data["Rocket"]["FinSet"]["radius"]
    )

    rocket.addTail(
        topRadius=data["Rocket"]["Tail"]["topRadius"],
        bottomRadius=data["Rocket"]["Tail"]["bottomRadius"],
        length=data["Rocket"]["Tail"]["length"],
        distanceToCM=data["Rocket"]["Tail"]["distanceToCM"]
    )

    for name,parachute in data["Rocket"]["parachutes"].items():        
        rocket.addParachute(
            name=name,
            CdS=parachute["CdS"],
            trigger=parachute["trigger"],
            samplingRate=parachute["samplingRate"],
            lag=parachute["lag"],
            noise=(parachute["noise"][0], parachute["noise"][1], parachute["noise"][2])
        )


    flight = Flight(
        rocket=rocket,
        environment=environment,
        inclination=data["Flight"]["inclination"],
        heading=data["Flight"]["heading"],
        initialSolution=data["Flight"]["initialSolution"],
        terminateOnApogee=data["Flight"]["terminateOnApogee"],
        maxTime=data["Flight"]["maxTime"],
        maxTimeStep=np.inf if data["Flight"]["maxTimeStep"] >= 1.7976931348623157e+308 else data["Flight"]["maxTimeStep"],
        minTimeStep=data["Flight"]["minTimeStep"],
        rtol=data["Flight"]["rtol"],
        atol=data["Flight"]["atol"],
        timeOvershoot=data["Flight"]["timeOvershoot"],
        verbose=data["Flight"]["verbose"]
    )

    if verbose:
        flight.allInfo()
    
    return environment, solidMotor, rocket, flight

    

    








