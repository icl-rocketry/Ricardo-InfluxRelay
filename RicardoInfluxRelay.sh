# Print start message
echo "Starting Ricardo Influx Relay"

# Execute the Ricardo Backend main file
python3 main.py --config ./config/config.yml

# Print exit message
echo "Ricardo Influx Relay exited"
