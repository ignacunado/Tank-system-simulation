import threading
import time

from settings import Settings
from tank import Tank
from control_valve import Control_valve

settings = Settings()
g = settings.g
rho = settings.rho
delta_t = settings.delta_t

variable_changed = 0
new_value = 0
t = 0
q_factor = 60 # m3/s
tank = Tank(20, 15, 5.5, 2, 1, 0.5, 1000000, 101325)
valve = Control_valve(tank.liquid_high, kp=20, ki=0.0002, kd=10, sp_auto= 6)
# kp = 20
# ki = 0.0002
# kd = 1

tank.tk_bem()
print("Nozzle velocity: ", round(tank.v2, 2))
print("Nozzle area: ", round(tank.nozzle_area, 2))
print("Volume Flow: ", round(tank.nozzle_area * tank.v2, 2))

lock = threading.Lock()          # Lock for thread safety
stop_event = threading.Event()   # Event to stop threads


def general_update():
    tank.tk_update()
    tank.tk_bem()
    valve.valve_update()
    tank.q_inlet = (valve.open/100) * q_factor
    tank.tk_fill() 
    valve.measured_variable = tank.liquid_high

def variable_choosen(variable_changed, new_value):
    if variable_changed == 1:
        tank.liquid_high = new_value
    elif variable_changed == 2:
        tank.nozzle_high = new_value
    elif variable_changed == 3:
        tank.p1 = new_value
    elif variable_changed == 4:
        valve.sp_auto = new_value   


def update_variables():
    global variable_changed, new_value, t
    while not stop_event.is_set():
        with lock:
            general_update()
            print(f"\n\n\n\n-----| Nozzle vel: {round(tank.v2, 2)} | Liquid level: {round(tank.liquid_high, 2)} | Inner pressure: {round(tank.p1, 2)} | Valve opening: {round(valve.open,2)} | Set point {valve.sp_auto} | t: {t} |-----")
            print('Select a variable to change:\n1. Liquid level (m)\n2. Nozzle high (m)\n3. Inner pressure (pa)\n4. New level setpoint (%)\n')
            print('Enter the number and the new value separated by a space, or "q" to quit.\n')
            t += delta_t
            time.sleep(delta_t)

def change_variables():
    global variable_changed, new_value, t
    while not stop_event.is_set():
        user_input = input(" ")
        if user_input.lower() == 'q':
            stop_event.set()
            break
        try:
            variable_changed, new_value = map(int, user_input.split())
            with lock:
                variable_choosen(variable_changed, new_value)                  
            print(f"\n********** Variable changed: {variable_changed}, New value: {new_value} ***********\n")
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")


# Create and start threads
update_thread = threading.Thread(target=update_variables)
input_thread = threading.Thread(target=change_variables)

update_thread.start()
input_thread.start()

# Join threads to the main thread
update_thread.join()
input_thread.join()

print("Threads have been stopped and program is exiting.\n")
