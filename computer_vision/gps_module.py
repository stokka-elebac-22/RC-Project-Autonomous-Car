import serial
SERIAL_PORT = "/dev/serial0"
'''
    GPS Module example
'''
def format_degrees_minutes(coordinates, digits):
    ''' In the NMEA message, the position gets transmitted as:
        DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
        the minutes. However, I want to convert this format to the following:
        DD.MMMM. This method converts a transmitted string to the desired format'''
    parts = coordinates.split(".")

    if len(parts) != 2:
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates

    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])

    return degrees + "." + minutes

def get_position_data(gps):
    ''' This method reads the data from the serial port, the GPS dongle is attached to,
        and then parses the NMEA messages it transmits.
        gps is the serial port, that's used to communicate with the GPS adapter'''
    data = gps.readline()
    message = data[0:6]
    if message == b'$GPRMC':
        # GPRMC = Recommended minimum specific GPS/Transit data
        # Reading the GPS fix data is an alternative approach that also works
        parts = str(data).split(",")
        if parts[2] == 'V':
            # V = Warning, most likely, there are no satellites in view...
            print ("GPS receiver warning")
        else:
            # Get the position data that was transmitted with the GPRMC message
            # In this example, I'm only interested in the longitude and latitude
            # for other values, that can be read, refer to: http://aprs.gids.nl/nmea/#rmc
            longitude = format_degrees_minutes(parts[5], 3)
            latitude = format_degrees_minutes(parts[3], 2)
            print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
    else:
        # Handle other NMEA messages and unsupported strings
        pass

print ("Application started!")
gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)

running = True
while running:
    try:
        get_position_data(gps)
    except KeyboardInterrupt:
        running = False
        gps.close()
        print ("Application closed!")
