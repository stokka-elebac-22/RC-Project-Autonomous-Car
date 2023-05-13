from joystick_handler.joystick_position import CurrentHeading

class ManualDriving():
    '''Class for manual driving of the vehicle'''
    @staticmethod
    def run_calculation(input_data: CurrentHeading):
        '''Take input from Gamepad currentHeading
            output direction and speed for manual driving'''
        y_velocity = input_data.y_velocity
        x_velocity = input_data.x_velocity
        if y_velocity > 0:
            dir_0 = 1
            dir_1 = 1
            speed_0 = 10
            speed_1 = 10
        elif y_velocity < 0:
            dir_0 = 0
            dir_1 = 0
            speed_0 = 10
            speed_1 = 10
        else:
            dir_0 = 0
            dir_1 = 0
            speed_0 = 0
            speed_1 = 0
        if x_velocity < 0:
            speed_0 += 10
        elif x_velocity > 0:
            speed_1 += 10
        print(f"Speeds Speed0: {int(speed_0)}, Speed1: {speed_1} dir0/1: {dir_0} {dir_1}")
        return {
            "dir_0" : dir_0,
            "dir_1" : dir_1,
            "speed_0" : speed_0,
            "speed_1" : speed_1
        }
