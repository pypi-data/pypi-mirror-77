//#ifdef __KERNEL__
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
//#endif

/******************************************************************************/
/*!                         System header files                               */
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include <errno.h>

/******************************************************************************/
/*!                         Own header files                                  */
#include "bme280.h"

/******************************************************************************/
/*!                               Structures                                  */

/* Structure that contains identifier details used in example */
struct identifier
{
    /* Variable to hold device address */
    uint8_t dev_addr;

    /* Variable that contains file descriptor */
    int8_t fd;
};

/****************************************************************************/
/*!                         Functions                                       */

/*!
 *  @brief Function that creates a mandatory delay required in some of the APIs.
 *
 * @param[in] period              : Delay in microseconds.
 * @param[in, out] intf_ptr       : Void pointer that can enable the linking of descriptors
 *                                  for interface related call backs
 *  @return void.
 *
 */
void user_delay_us(uint32_t period, void* intf_ptr);

/*!
 * @brief Function for print the temperature, humidity and pressure data.
 *
 * @param[out] comp_data    :   Structure instance of bme280_data
 *
 * @note Sensor data whose can be read
 *
 * sens_list
 * --------------
 * Pressure
 * Temperature
 * Humidity
 *
 */
void print_sensor_data(struct bme280_data* comp_data);

/*!
 *  @brief Function for reading the sensor's registers through I2C bus.
 *
 *  @param[in] reg_addr       : Register address.
 *  @param[out] data          : Pointer to the data buffer to store the read data.
 *  @param[in] len            : No of bytes to read.
 *  @param[in, out] intf_ptr  : Void pointer that can enable the linking of descriptors
 *                                  for interface related call backs.
 *
 *  @return Status of execution
 *
 *  @retval 0 -> Success
 *  @retval > 0 -> Failure Info
 *
 */
int8_t user_i2c_read(uint8_t reg_addr, uint8_t* data, uint32_t len, void* intf_ptr);

/*!
 *  @brief Function for writing the sensor's registers through I2C bus.
 *
 *  @param[in] reg_addr       : Register address.
 *  @param[in] data           : Pointer to the data buffer whose value is to be written.
 *  @param[in] len            : No of bytes to write.
 *  @param[in, out] intf_ptr  : Void pointer that can enable the linking of descriptors
 *                                  for interface related call backs
 *
 *  @return Status of execution
 *
 *  @retval BME280_OK -> Success
 *  @retval BME280_E_COMM_FAIL -> Communication failure.
 *
 */
int8_t user_i2c_write(uint8_t reg_addr, const uint8_t* data, uint32_t len, void* intf_ptr);


/*!
 * @brief This function reading the sensor's registers through I2C bus.
 */
int8_t user_i2c_read(uint8_t reg_addr, uint8_t* data, uint32_t len, void* intf_ptr)
{
    struct identifier id;

    id = *((struct identifier*)intf_ptr);

    write(id.fd, &reg_addr, 1);
    read(id.fd, data, len);

    return 0;
}

/*!
 * @brief This function provides the delay for required time (Microseconds) as per the input provided in some of the
 * APIs
 */
void user_delay_us(uint32_t period, void* intf_ptr)
{
    usleep(period);
}

/*!
 * @brief This function for writing the sensor's registers through I2C bus.
 */
int8_t user_i2c_write(uint8_t reg_addr, const uint8_t* data, uint32_t len, void* intf_ptr)
{
    uint8_t* buf;
    struct identifier id;

    id = *((struct identifier*)intf_ptr);

    buf = malloc(len + 1);
    buf[0] = reg_addr;
    memcpy(buf + 1, data, len);
    if (write(id.fd, buf, len + 1) < (uint16_t)len)
    {
        return BME280_E_COMM_FAIL;
    }

    free(buf);

    return BME280_OK;
}

/*** Melopero Python Wrapper Helper Functions ***/

//TODO: change to malloc and return pointers to structures

static struct bme280_dev dev;
static struct identifier id;
static struct bme280_data data;

int8_t init_device(uint8_t i2c_address, uint8_t i2c_bus) {

    char filename[20];
    snprintf(filename, 19, "/dev/i2c-%d", i2c_bus);

    id.dev_addr = i2c_address;

    dev.intf = BME280_I2C_INTF;
    dev.read = user_i2c_read;
    dev.write = user_i2c_write;
    dev.delay_us = user_delay_us;

    /* Update interface pointer with the structure that contains both device address and file descriptor */
    dev.intf_ptr = &id;

    int i2c_fd = open(filename, O_RDWR);
    if (i2c_fd < 0) {
        fprintf(stderr, "Error occurred while opening file %s! %s\n", filename, strerror(errno));
        return BME280_E_COMM_FAIL;
    }

    id.fd = i2c_fd;

//#ifdef __KERNEL__
    if (ioctl(id.fd, I2C_SLAVE, id.dev_addr) < 0)
    {
        fprintf(stderr, "Failed to acquire bus access and/or talk to slave.\n");
        return BME280_E_COMM_FAIL;
    }

//#endif

    /* Initialize the bme280 */
    int8_t rslt = bme280_init(&dev);
    if (rslt != BME280_OK)
    {
        fprintf(stderr, "Failed to initialize the device (code %+d).\n", rslt);
    }

    return rslt;
}

int8_t set_oversampling(uint8_t pressure_os, uint8_t temperature_os, uint8_t humidity_os) {
    dev.settings.osr_p = pressure_os;
    dev.settings.osr_t = temperature_os;
    dev.settings.osr_h = humidity_os;
    return BME280_OK;
}

int8_t set_filter_coefficient(uint8_t filter_coefficient) {
    dev.settings.filter = filter_coefficient;
    return BME280_OK;
}

int8_t set_sensor_settings(uint8_t settings) {
    int8_t rslt = bme280_set_sensor_settings(settings, &dev);
    if (rslt != BME280_OK)
    {
        fprintf(stderr, "Failed to set sensor settings (code %+d).", rslt);
    }
    return rslt;
}

int8_t update_data() {
    int8_t rslt = BME280_OK;
    /* In forced mode, a single measurement is performed in accordance
    to the selected measurement and filter options. When the measurement
    is finished, the sensor returns to sleep mode and the measurement 
    results can be obtained from the data registers. For a next 
    measurement, forced mode needs to be selected again.*/
    rslt = bme280_set_sensor_mode(BME280_FORCED_MODE, &dev);
    if (rslt != BME280_OK)
    {
        fprintf(stderr, "Failed to set sensor mode (code %+d).", rslt);
        return rslt;
    }

    /*Calculate the minimum delay required between consecutive measurement based upon the sensor enabled
    *  and the oversampling configuration. */
    uint32_t req_delay = bme280_cal_meas_delay(&(dev.settings));

    /* Wait for the measurement to complete and print data */
    dev.delay_us(req_delay, dev.intf_ptr);
    rslt = bme280_get_sensor_data(BME280_ALL, &data, &dev);
    if (rslt != BME280_OK)
    {
        fprintf(stderr, "Failed to get sensor data (code %+d).", rslt);
        return rslt;
    }

    return rslt;
}

//TODO: return pointer to structure for portability

float get_pressure() {
    return data.pressure;
}

float get_temperature() {
    return data.temperature;
}

float get_humidity() {
    return 0.01 * data.humidity;
}

int8_t close_connection() {
    close(id.fd);
}