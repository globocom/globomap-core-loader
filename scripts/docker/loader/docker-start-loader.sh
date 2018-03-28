while ! nc -vz globomap_loader_queue 5672; do sleep 1; done

make run_loader module=GenericDriver
