#!/bin/bash
set -e

# Fix permissions of the home directory if the user doesn't own it
# Find out who owns /home/user
OWNER=$(stat -c '%U' /home/user 2>/dev/null || echo "user")

if [ "$OWNER" != "user" ]; then
    # We use sudo because the container runs as 'user' but has passwordless sudo
    sudo chown -R user:user /home/user 2>/dev/null || true
fi

exec open-terminal "$@"
