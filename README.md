# Sprinkle
A homegrown sprinkler controller system. This system is broken up into a master and slave configuration. The slave is a Raspberry Pi using an RFM95W to receive commands from the master. It has an attached 4 channel relay board and a small I2C OLED display to see status information.
The master is another Raspberry Pi with another RFM95W to transmit commands to the slave. A CLI and web based control interface is provided (or will be ;-) ).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
This is a python based project. It uses a few open source modules including:
 * wiringpi
 * pySX127x
 * spidev

These modules can be installed using pip. Note that python-dev should also be installed to make the installation of the above modules easier. Also, these modules require access to the GPIO pins in multiple modes, so the user that runs this should either be root (not advised) or should be part of the SPI, GPIO, and I2C groups.

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [wiringpi](https://github.com/WiringPi/WiringPi-Python) - WiringPi: An implementation of most of the Arduino Wiring functions for the Raspberry Pi.
* [pySX127x](https://github.com/mayeranalytics/pySX127x) - pxSX127x: Python interface to Semtech SX1276/7/8/9 that is also compatible with the RFM95w. Some customizations have been made for use in Sprinkle.
* [spidev](https://github.com/doceme/py-spidev) - spidev: A python module for interfacing with SPI devices from user space via the spidev linux kernel driver.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Oliver Nelson** - *Initial work* - [flxkid](https://github.com/flxkid)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GNU GPL v3 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
