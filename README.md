# YouThere

This project uses a PIR sensor and an arduino to detect presence in a room.

`pir.ino` is the arduino project.
`pir-logger.py` reads the data over the serial from the arduino, and logs.
`plot.py` reads the log file and plots the data for a given day.
