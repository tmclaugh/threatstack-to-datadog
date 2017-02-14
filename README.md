# threatstack-to-datadog
Takes a Threat Stack web hook request and add an event to DataDog.

**NOTE: This code is provided as an example and without support for creating services that use Threat Stack webhooks to perform actions within an environment.**

## Setup
Setup will need to be performed for both this service and in Threat Stack.

Set the following environmental variables:
```
$ export DATADOG_API_KEY=<API key>
$ export DATADOG_APP_KEY=<App key>
$ export THREATSTACK_API_KEY=<Threat Stack API key>
```

Create and initialize Python virtualenv using virtualenvwrapper
```
mkvirtualenv threatstack-to-datadog
pip install -r requirements.txt
```

__NOTE:__ If Running on OS X you will need extra packages to work around issues with Python and SSL. OS X usage should be for development only.
```
pip install -r requirements.osx.txt
```

To launch the service:
```
gunicorn -c gunicorn.conf.py threatstack-to-datadog
```

If performing debugging you may wish to run the app directly instead of via Gunicorn:
```
python threatstack-to-datadog.py
```

## Build
This service uses [Chef Habitat](http://www.habitat.sh) to build deployable packages.  Habitat supports the following package formats natively:
* Habitat package (.hart)
* tar
* docker
* aci
* mesos

See the following resources for getting started with Habitat.
* https:///www.habitat.sh/docs/overview/
* https:///www.habitat.sh/tutorial/

Building packages:
```
# Builds Habitat .hart package
$ hab pkg build build/

# Export a Docker container
$ hab pkg export docker <your_docker_org>/threatstack-to-datadog
```

Building in Hab studio (OS X):
```
$ hab studio enter
[1][default:/src:0]# cd build/

# Builds Habitat .hart package
[2][default:/src/build:0]# build

# Export a Docker container.
[3][default:/src/build:0]# hab pkg export docker <your_docker_org>/threatstack-to-datadog
```

## API
### POST https://_{host}_/api/v1/datadog/event
Post a JSON doc from Threat Stack and record an event in DataDog.  JSON doc will be in the following format.  __NOTE__: A webhook may contain multiple alerts but this service will store each one individually.
```
{
  "alerts": [
    {
      "id": "<alert ID>",
      "title": "<alert title / description>",
      "created_at": <time in milliseconds from epoch UTC>,
      "severity": <severity value>,
      "organization_id": "<alphanumeric organization ID>",
      "server_or_region": "<name of host in Threat Stack platform>",
      "source": "<source type>"
    }
  [
}
```

