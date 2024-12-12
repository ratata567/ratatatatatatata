#!/bin/bash

source .env

CURRENTDATE=$(date +"%Y%m%d")

echo "------------------------Login to Geddes Registry------------------------------------"
docker login geddes-registry.rcac.purdue.edu

echo "------------------------Building Container------------------------------------------"
docker build --progress=plain --platform linux/x86_64 -t purduegptui:${CURRENTDATE} .

echo "------------------------Tagging Container for Geddes--------------------------------"
docker tag purduegptui:${CURRENTDATE} geddes-registry.rcac.purdue.edu/purdue-gpt-ui/purduegptui:${CURRENTDATE}

echo "------------------------Pushing Container to Geddes Registry------------------------"
docker push geddes-registry.rcac.purdue.edu/purdue-gpt-ui/purduegptui:${CURRENTDATE}

# echo "------------------------Logout of Geddes Registry------------------------------------"
# docker logout geddes-registry.rcac.purdue.edu

echo "------------------------Login to Anvil Registry-------------------------------------"
docker login -u "$ANVIL_USER" -p "$ANVIL_SECRET" registry.anvil.rcac.purdue.edu

echo "------------------------Tagging Container for Anvil---------------------------------"
docker tag purduegptui:${CURRENTDATE} anvilgptui:${CURRENTDATE}
docker tag purduegptui:${CURRENTDATE} registry.anvil.rcac.purdue.edu/anvil-gpt-ui/anvilgptui:${CURRENTDATE}
docker rmi purduegptui:${CURRENTDATE}
docker rmi geddes-registry.rcac.purdue.edu/purdue-gpt-ui/purduegptui:${CURRENTDATE}

echo "------------------------Pushing Container to Anvil Registry-------------------------"
docker push registry.anvil.rcac.purdue.edu/anvil-gpt-ui/anvilgptui:${CURRENTDATE}

# echo "------------------------Logout of Anvil Registry------------------------------------"
# docker logout registry.anvil.rcac.purdue.edu