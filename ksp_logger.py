import time
import krpc
from math import sqrt

conn = krpc.connect(name="bebralet")
vessel = conn.space_center.active_vessel
obt_frame = vessel.orbit.body.non_rotating_reference_frame
srf_frame = vessel.orbit.body.reference_frame

with open("data.txt", "w") as file:
    file.write('OrbitalSpeed;SurfaceSpeed;TerminalVelocity;Altitude;Mass;Thrust;SpecificImpulse;SurfaceGravity;AerodynamicForce\n')

with open("data.txt", "a") as file:
    while True:
        obt_speed = vessel.flight(obt_frame).speed
        srf_speed = vessel.flight(srf_frame).speed
        mass = 0
        impulse = vessel.specific_impulse
        thrust = vessel.thrust
        force = vessel.flight(srf_frame).aerodynamic_force
        square = 0
        for i in force:
            square += i**2
        AerodynamicForce = sqrt(square)
        gravity = vessel.orbit.body.surface_gravity
        for part in vessel.parts.all:
            mass += part.mass
        mass = vessel.mass
        t_vel = vessel.flight(srf_frame).terminal_velocity
        altitude = vessel.flight(srf_frame).mean_altitude
        file.write(f"{obt_speed};{srf_speed};{t_vel};{altitude};{mass};{thrust};{impulse};{gravity};{AerodynamicForce}\n")
        print('Orbital speed = %.1f m/s, Surface speed = %.1f m/s, Terminal velocity = %.1f m/s, Altitude = %.1f m, '
              'Mass = %.1f kg, Thrust = %.1f Newt, Specific Impulse= %.1f m/s, SurfaceGravity = %.1f m/s^2, AerodynamicForce = %.1f Newt' %
              (obt_speed, srf_speed, t_vel, altitude, mass,thrust,impulse,gravity,AerodynamicForce))
        time.sleep(1)
