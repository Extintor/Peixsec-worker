# Peixsec-worker
[![Build Status](https://travis-ci.com/Extintor/Peixsec.svg?token=ySBoF7gL1qEzUFtntZjQ&branch=master)](https://travis-ci.com/Extintor/Peixsec)
[![codecov](https://codecov.io/gh/Extintor/Peixsec/branch/master/graph/badge.svg?token=buF4QKhYVq)](https://codecov.io/gh/Extintor/Peixsec)

A Simple worker image that consumes FEN Notation chess positions from a AMQP Broker, executes stockfish chess engine
and saves the result in a MongoDB instance. 

This is meant to be executed as a Kubernetes Job. You can see and example how here:
[Kubernetes Job example](https://kubernetes.io/docs/tasks/job/coarse-parallel-processing-work-queue/)

An updated docker image can be found here:
[Docker Image](https://hub.docker.com/r/paulcharbo/peixsec_worker)

---

### Instructions

The following environment variables have to be passed to the docker image:

- `DB_USER`: Username to access the database.
- `DB_PASSWORD`: Password to access the database.
