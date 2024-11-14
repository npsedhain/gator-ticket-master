# Define variables
PYTHON = python3
SOURCE = gatorTicketMaster.py
TARGET = gatorTicketMaster

# Default target to create an executable
all: $(TARGET)

# Create executable by linking to the main Python file
$(TARGET): $(SOURCE)
	echo "#!/bin/bash\n$(PYTHON) $(SOURCE) \$$1" > $(TARGET)
	chmod +x $(TARGET)

# Clean generated executable
clean:
	rm -f $(TARGET)
	rm -rf __pycache__
