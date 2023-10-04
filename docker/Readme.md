# Batchee Service Docker Image

This directory contains the `Dockerfile` used to build the Docker image capable of running the Batchee service.

## Building

The docker image is setup to install the Batchee project into userspace using pip. It will look
in both PyPi and TestPyPi indexes unless building from a local wheel file.