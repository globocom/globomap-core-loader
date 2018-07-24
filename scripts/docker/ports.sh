#!/bin/bash

if [ -z "${GMAP_QUEUE_PORT}" ]; then
    echo "Environment variable GMAP_QUEUE_PORT is not defined."
    echo "Setting default ..."
    GMAP_QUEUE_PORT=7007
fi

if [ -z "${GMAP_QUEUE_ADM_PORT}" ]; then
    echo "Environment variable GMAP_QUEUE_ADM_PORT is not defined."
    echo "Setting default ..."
    GMAP_QUEUE_ADM_PORT=7008
fi

if [ -z "${GMAP_DB_LOADER_PORT}" ]; then
    echo "Environment variable GMAP_DB_LOADER_PORT is not defined."
    echo "Setting default ..."
    GMAP_DB_LOADER_PORT=7009
fi

if [ -z "${GMAP_LOADER_API_PORT}" ]; then
    echo "Environment variable GMAP_LOADER_API_PORT is not defined."
    echo "Setting default ..."
    GMAP_LOADER_API_PORT=7010
fi

if [ -z "${GMAP_LOADER_API_DEBUG_PORT}" ]; then
    echo "Environment variable GMAP_LOADER_API_DEBUG_PORT is not defined."
    echo "Setting default ..."
    GMAP_LOADER_API_DEBUG_PORT=7011
fi

cp -R docker-compose.yml docker-compose-temp.yml
sed -i '' "s/\${GMAP_QUEUE_PORT}/$GMAP_QUEUE_PORT/g" docker-compose-temp.yml
sed -i '' "s/\${GMAP_QUEUE_ADM_PORT}/$GMAP_QUEUE_ADM_PORT/g" docker-compose-temp.yml
sed -i '' "s/\${GMAP_DB_LOADER_PORT}/$GMAP_DB_LOADER_PORT/g" docker-compose-temp.yml
sed -i '' "s/\${GMAP_LOADER_API_PORT}/$GMAP_LOADER_API_PORT/g" docker-compose-temp.yml
sed -i '' "s/\${GMAP_LOADER_API_DEBUG_PORT}/$GMAP_LOADER_API_DEBUG_PORT/g" docker-compose-temp.yml
