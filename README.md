# globomap-core-loader

Application responsible for reading connected applications events and apply them to the [Globo Map API](https://github.com/globocom/globomap-api).
This application makes use of decoupled drivers for reading and transforming sources' information and make
them available for updating the [Globo Map API](https://github.com/globocom/globomap-api).

Drivers:

[Network API driver](https://github.com/globocom/globomap-driver-napi)

[Cloudstack driver](https://github.com/globocom/globomap-driver-acs)

## Environment variables configuration
All of the environment variables below must be set for the application to work properly.

### Loader
| Variable                           | Description                                                                | Example                             |
|------------------------------------|----------------------------------------------------------------------------|----------------------------------   |
| DRIVER_FETCH_INTERVAL              | Interval in seconds on which the updates are fetched from a driver         | 60 (default)                        |
| GLOBOMAP_API_URL                   | Globo Map API address                                                      | http://globomap.domain.com          |
| GLOBOMAP_API_USERNAME              | Globo Map API username                                                     | username                            |
| GLOBOMAP_API_PASSWORD              | Globo Map API password                                                     | xyz                                 |
| GLOBOMAP_RMQ_HOST                  | RabbitMQ host                                                              | rabbitmq.yourdomain.com             |
| GLOBOMAP_RMQ_PORT                  | RabbitMQ port                                                              | 5672 (default)                      |
| GLOBOMAP_RMQ_USER                  | RabbitMQ user                                                              | user-name                           |
| GLOBOMAP_RMQ_PASSWORD              | RabbitMQ password                                                          | password                            |
| GLOBOMAP_RMQ_VIRTUAL_HOST          | RabbitMQ virtual host                                                      | /globomap                           |
| GLOBOMAP_RMQ_QUEUE_NAME            | RabbitMQ queue name                                                        | globomap-updates                    |
| GLOBOMAP_RMQ_EXCHANGE              | RabbitMQ updates exchange name                                             | globomap-updates-exchange           |
| GLOBOMAP_RMQ_ERROR_EXCHANGE        | RabbitMQ error exchange name                                               | globomap-errors-exchange            |
| GLOBOMAP_RMQ_BINDING_KEY           | RabbitMQ generic driver API binding key                                    | globomap.updates (default)          |
| DATABASE_POOL_SIZE                 | Relational database connection pool size                                   | 20 (default)                        |
| DATABASE_POOL_OVERFLOW             | Relational database connection pool overflow                               | 10 (default)                        |
| DATABASE_POOL_RECYCLE              | Number of seconds in which an idle connection is refreshed                 | 120 (default)                       |
| SQLALCHEMY_DATABASE_URI            | The database URI that should be used for the connection                    | mysql://username:password@server/db |
| VARIABLES of globomap-auth-manager | [globomap-auth-manager](https://github.com/globocom/globomap-auth-manager) | --                                  |
| VARIABLES of globomap-driver-napi  | [globomap-driver-napi](https://github.com/globocom/globomap-driver-napi)   | --                                  |
| VARIABLES of globomap-driver-acs   | [globomap-driver-acs](https://github.com/globocom/globomap-driver-acs)     | --                                  |

### API
| Variable                           | Description                                                               | Example                                 |
|------------------------------------|---------------------------------------------------------------------------|-----------------------------------------|
| GLOBOMAP_RMQ_HOST                  | RabbitMQ host                                                             | rabbitmq.yourdomain.com                 |
| GLOBOMAP_RMQ_PORT                  | RabbitMQ port                                                             | 5672 (default)                          |
| GLOBOMAP_RMQ_USER                  | RabbitMQ user                                                             | user-name                               |
| GLOBOMAP_RMQ_PASSWORD              | RabbitMQ password                                                         | password                                |
| GLOBOMAP_RMQ_VIRTUAL_HOST          | RabbitMQ virtual host                                                     | /globomap                               |
| GLOBOMAP_RMQ_QUEUE_NAME            | RabbitMQ queue name                                                       | globomap-updates                        |
| GLOBOMAP_RMQ_EXCHANGE              | RabbitMQ updates exchange name                                            | globomap-updates-exchange               |
| GLOBOMAP_RMQ_ERROR_EXCHANGE        | RabbitMQ error exchange name                                              | globomap-errors-exchange                |
| GLOBOMAP_RMQ_BINDING_KEY           | RabbitMQ generic driver API binding key                                   | globomap.updates (default)              |
| DATABASE_POOL_SIZE                 | Relational database connection pool size                                  | 20 (default)                            |
| DATABASE_POOL_OVERFLOW             | Relational database connection pool overflow                              | 10 (default)                            |
| DATABASE_POOL_RECYCLE              | Number of seconds in which an idle connection is refreshed                | 120 (default)                           |
| SQLALCHEMY_DATABASE_URI            | The database URI that should be used for the connection                   | mysql://username:password@server/db     |
| VARIABLES of globomap-auth-manager | [globomap-auth-manager](https://github.com/globocom/globomap-auth-manager)| --                                      |

### Environment variables configuration from external libs
All of the environment variables below must be set for the application to work properly.

[globomap-auth-manager](https://github.com/globocom/globomap-auth-manager)
[globomap-driver-napi](https://github.com/globocom/globomap-driver-napi)
[globomap-driver-acs](https://github.com/globocom/globomap-driver-acs)

 ## API
[Documentation](https://github.com/globocom/globomap-core-loader/blob/master/doc/api.md)
