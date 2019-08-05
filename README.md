## This is not the live LCO website software

The LCO website now uses Wagtail, a Django-based CMS. The new repo is called [LCO_global](https://github.com/LCOGT/lco_global)

# Las Cumbres Observatory Website

This is the project containing the Las Cumbres Observatory website, available
online at <https://lco.global/>.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See the Deployment section
of this document for notes on how to deploy the project on a live system.

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Run the application

Please read and customize the provided [docker-compose.yml](docker-compose.yml)
file for your specific database configuration. See the Configuration section
of this document for notes on the available configuration options. This example
configuration will have the application up and running on port 80.

You can run the current latest available version of this project by running:

    $ docker-compose up

If you need to build your own version of this project, you can follow these
instructions instead:

    $ docker build --pull -t docker.lco.global/mezzanine:latest .
    $ docker-compose up

### Configuration

This project is configured using environment variables. The available
configuration options and their defaults are listed below.

- **`DB_HOST`** - MySQL Database Hostname (default: `db.example.com`)
- **`DB_NAME`** - MySQL Database Name (default: `main_website`)
- **`DB_USER`** - MySQL Database Username (default: `username`)
- **`DB_PASS`** - MySQL Database Password (default: `password`)
- **`SECRET_KEY`** - Django Secret Key (default: random)
- **`EMAIL_USER`** - SMTP Username (default: None)
- **`EMAIL_PASS`** - SMTP Password (default: None)
- **`ADS_TOKEN`** - Unknown (default: None)
- **`ROLLBAR_TOKEN`** - Unknown: (default: None)

## Deployment

This project is intended to be deployed an a Docker orchestration platform,
such as [Rancher](https://rancher.com/) or [Kubernetes](https://kubernetes.io/).

Please read through the Configuration section of this document for notes on the
available configuration options. Please set all of the options to values which
are known to work for your production environment.

## Authors

This project is maintained by the [Las Cumbres Observatory](https://lco.global/)
staff.
