#!/bin/bash

exec celery -A environment_provider.environment_provider.APP worker -P eventlet -c 1000 -l DEBUG
