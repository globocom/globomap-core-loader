# globomap-core-loader

Application responsible for reading connected applications events and apply them to the [Globo Map API](https://github.com/globocom/globomap-api).
This application makes use of decoupled drivers for reading and transforming sources' information and make
them available for updating the [Globo Map API](https://github.com/globocom/globomap-api).

Drivers:

[Network API driver](https://github.com/globocom/globomap-driver-napi)

[Cloudstack driver](https://github.com/globocom/globomap-driver-acs)

## Environment variables configuration
All of the environment variables below must be set for the application to work properly.

| Variable                    | Description                                                       | Example                      |
|-----------------------------|-------------------------------------------------------------------|------------------------------|
| DRIVER_FETCH_INTERVAL       | Interval in seconds on which the updates are fetched from a driver| 30 (default)                 |
| DRIVER_NUMBER_OF_UPDATES    | Number of updates that are fetched from the driver on each interval| 1 (default)              |
| GLOBOMAP_API_ADDRESS        | Globo MAP API address                                             | http://globomap.domain.com   |
| GLOBOMAP_RMQ_HOST           | Globo MAP RabbitMQ host                                           | rabbitmq.yourdomain.com      |
| GLOBOMAP_RMQ_PORT           | Globo MAP RabbitMQ port                                           | 5672 (default)               |
| GLOBOMAP_RMQ_USER           | Globo MAP RabbitMQ user                                           | user-name                    |
| GLOBOMAP_RMQ_PASSWORD       | Globo MAP RabbitMQ password                                       | password                     |
| GLOBOMAP_RMQ_VIRTUAL_HOST   | Globo MAP RabbitMQ virtual host                                   | /globomap                    |
| GLOBOMAP_RMQ_QUEUE_NAME     | Globo MAP RabbitMQ queue name                                     | globomap-events              |
| GLOBOMAP_RMQ_ERROR_EXCHANGE | Globo MAP RabbitMQ error exchange name                            | globomap-errors              |
