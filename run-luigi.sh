#!/bin/bash

# Add "--local-scheduler" in dev to avoid running on luigid
python2 -m luigi --module all_luigi_tasks AllLuigiTasks
