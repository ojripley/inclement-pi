import time
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)

# returns a dict of temperature, humidity
def read_data(PRINT_OUT_PUT = False):


  climate_conditions = dict()

  # because cpu temp affects sense readings, we need to offest the raw data

  try:
    # Print the values to the serial port
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity

    time_of_reading = time.ctime(time.time())

    climate_conditions['temperature'] = temperature
    climate_conditions['humidity'] = humidity
    climate_conditions['time_of_reading'] = time.ctime(time.time())
    print(
      "Temp: {:.1f} C    Humidity: {}% ".format(
        temperature, humidity
      )
    )

  except RuntimeError as error:
    # Errors happen fairly often, DHT's are hard to read, just keep going
    print(error.args[0])



  if (PRINT_OUT_PUT):
    print("\n\n-- Weather Readout --")
    print("Temperature:  " + str(temperature) + " C")
    print("Humidity:     " + str(humidity) + " %")
    print("Taken at:     " + str(time_of_reading))

  return(climate_conditions)
