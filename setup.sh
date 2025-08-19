#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
maxUploadSize = 200\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
" > ~/.streamlit/config.toml
