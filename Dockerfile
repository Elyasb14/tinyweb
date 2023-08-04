# Use the official Raspberry Pi OS (Raspbian) image for ARM architecture
FROM balenalib/raspberry-pi-debian:latest

# Update the package lists and install any required packages
RUN sudo apt update && sudo apt upgrade

# Set the default working directory (you can change this as per your project)
WORKDIR /tinyweb

# Copy your application files into the container
COPY . /tinyweb

# Add any additional configurations or commands here if necessary

# Start your application (modify this as per your project requirements)
CMD ["sudo ./deploy.sh"]
CMD ["./cron.sh"]

