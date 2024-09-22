"""
        Calcula la salida de un controlador PID (Proporcional, Integral, Derivativo).

    El método calcula la salida del controlador PID utilizando el valor actual y el setpoint.
    Se almacena el histórico de velocidades en self.record y se limita a 500 elementos.
    Se calculan los componentes P, I y D del controlador y se suman para obtener la salida.
    La salida se limita al rango de 0 a 100 (%).
"""

class Control_valve():

    def __init__ (self, measured_variable, kp, ki, kd, manual_mode = False, sp_man = 0.0, sp_auto = 0.0):
        self.measured_variable = measured_variable
        self.manual_mode = manual_mode
        self.sp_man = sp_man
        self.sp_auto = sp_auto
        self.error = 0.0
        self.error_accuracy = 0.0
        self.record = []
        self.open = 0
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def valve_update(self):
        if self.manual_mode == False:
     
            self.record.append(self.measured_variable)
            if len(self.record) > 500:                  # Almaceno el vector velocidad en una lista de 100 elementos.
                self.record = self.record[-500:]


            self.error = self.sp_auto - self.measured_variable                 

            self.error_accuracy = [(self.sp_auto - elem) for elem in self.record[-100:]]
                
            aP = self.error * self.kp    # Acción proporcional

            aI = (self.kp * (sum(self.error_accuracy) / (len(self.error_accuracy)*0.002) * self.ki))    # Acción integral
        
            if len(self.record) > 2:    # Acción derivativa
                aD = (self.error_accuracy[-1]-self.error_accuracy[-2])*self.kd*self.kp
            else:
                aD = 0.0
    
                
            output = self.open + aP + aI + aD

            if output < 0:
                self.open = 0
            elif output > 100:
                self.open = 100         
            else:
                self.open = output

        else:
            self.open = self.sp_man