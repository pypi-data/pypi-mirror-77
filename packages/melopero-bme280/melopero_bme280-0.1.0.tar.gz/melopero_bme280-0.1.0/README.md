# Melopero_BME280
## Install 

To install the module, open a terminal and run this command:
```sudo pip3 install melopero-bme280```
## How to use

Importing the module and device object creation:

```python
import melopero_bme280 as mp

bme = mp.BME280()
# Alternatively you can specify which i2c bus and address to use
bme = mp.BME280(i2c_addr=your_i2c_address, i2c_bus=1)
```

### Settings
You can select one of three settings presets: weather monitoring, indoor navigation and gaming.

```python
bme.set_weather_monitoring_configuration()
bme.set_indoor_navigation_configuration()
bme.set_gaming_configuration()
```
Or you can specify your own settings:
```python
# Set the Oversampling:
# To turn off a sensor (and not take measurements from that sensor) 
# set the oversampling to BME280.SENSOR_OFF 
# The possible oversampling values are :
# BME280.OVERSAMPLING_1X
# BME280.OVERSAMPLING_2X
# BME280.OVERSAMPLING_4X
# BME280.OVERSAMPLING_8X
# BME280.OVERSAMPLING_16X
bme.set_oversampling(pressure_os, temperature_os, humidity_os):

# Set the Filter settings:
# To turn off the filter set the filter settings to BME280.FILTER_COEFF_OFF
# The possible filter settings values are:
# BME280.FILTER_COEFF_2
# BME280.FILTER_COEFF_4
# BME280.FILTER_COEFF_8
# BME280.FILTER_COEFF_16
bme.set_filter_coefficient(filter_coefficient)
```

### Reading the data

To take a measurement and read the data :

```python
# get_data() returns a Dictionary with the following structure:
# {'T': temperature data, 'P': pressure data, 'H': humidity data }
# Temperature data is expressed in Celsius degrees
# Pressure data is expressed in Pascal
# Humidity data is expressed in % (0-1)

data = bme.get_data()
```

### Closing the device
To close correctly the device :
```python
data = bme.close()
```