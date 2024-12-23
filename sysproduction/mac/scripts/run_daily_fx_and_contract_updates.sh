#!/bin/bash

# Source the project-specific environment variables
source /Users/nanthawat/PycharmProjects/pysystemtrade/project_env.sh

# Execute the daily FX and contract updates
/bin/bash /Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/mac/scripts/run_daily_fx_and_contract_updates.sh
