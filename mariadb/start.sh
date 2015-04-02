#!/bin/bash

__run_supervisor() {
echo "Running the run supervisor function."
supervisord -n
}

# Call all functions
__run_supervisor
