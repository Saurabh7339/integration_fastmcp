#!/bin/bash
echo "Activating Virutal Environment...."
. /mnt2/ssd/python_projects/external_mcp_integration/env/bin/activate

echo "Starting the main server..."
nohup python -u -m main > nohup_main.out 2>&1 &

echo "Starting MCP Servers..."
nohup python -u -m run_mcp_servers > nohup_mcp_servers.out 2>&1 &

