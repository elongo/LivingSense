SOFTWARE
  LivingSense is an open source software for the Raspberry Pi, which senses environmental data (e.g.: air temperature, 
  air humidty, water content in soil, water temperature, air and water flow, object proximity) and based on such data is 
  able to control different outputs, be it by mechanical relays (for pumps, fans, lights, whatever 220-250 V AC) or solid 
  state relays (for AC motors speed control) allowing different interactions with the environment (irrigation, ventialtion, 
  illumination, etc.)

UI
  A webserver and user interface is included within this repository, which allows manual control of different relays.

DASHBOARD
  Sensor data is easily streamed to Power BI (other services can be easilz implemented), where data is displayed in real time 
  and histroically plotted, as well. 

NETWORKING
  More than one LivingSense can be installed and communicate via sockets, to exchange data or share control responsabilities 
  between machines.

REMOTE ACCESS
  Remote access to the UI and DASHBOARD is enabled via VPN. Remote SSH and FTP is also enbaled.

HARDWARE
  The LivingSense also provides the PCB designs to develop the proper hats for an easy plug and play setup. 
      TYPICAL SENSORS USED:
          - DS18B20: waterproof temperature sensor for soil, water or other tough conditions.
          - AM2315: air temperature and humidty sensor.
          - HC-SR04: proximity sensor (to be replaced for a range finder LIDAR sensor, for the sake of accuracy)
          - Fdit 60 mm: Water or air flow sensor.
          - Water proofed capacitive soil sensor. 

      TYPICAL DEVICES CONTROLLED:
          - Pumps (AC)
          - 24 VAC solenoid valves
          - Fan (AC)
          - Single phase AC motors.
          - Light fixtures (AC)

CASING - MODELS FOR 3D PRINTING:
  3D models are provided for 3D printing water proofed cases for the main board and components, and for some sensors 
  which are not provided water proofed by manufacturers.
