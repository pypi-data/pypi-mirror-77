"""
Producer implementation of the base connection wrapper
"""

import json
import logging
from typing import List, Union

import pika
from pika.exceptions import UnroutableError, NackError
from retry import retry
from retry.api import retry_call

from talus.base import DurableBlockingBaseWrapper

logger = logging.getLogger(__name__)


__all__ = ["DurableBlockingProducerWrapper"]

HOUR_1 = 3600

class DurableBlockingProducerWrapper(DurableBlockingBaseWrapper):
    """
    RabbitMQ Connector for posting to 1 to many queues via an exchange
    """

    def __init__(
        self,
        producer_queue_bindings: Union[List[dict], dict],
        publish_exchange: str,
        rabbitmq_host: str = "localhost",
        rabbitmq_port: int = 5672,
        rabbitmq_user: str = "guest",
        rabbitmq_pass: str = "guest",
        retry_delay: int = 1,
        retry_backoff: int = 2,
        retry_jitter: int = (1, 10),
        retry_max_delay: int = 300,
        retry_tries: int = -1,
        prefetch_count: int = 1,
        connection_name: str = "producer connection",
    ):
        """
        Constructor for the producer connector

        :param producer_queue_bindings: Bindings from routing key to destination queue for an exchange
        e.g. [{"routing_key": "frame.audit.m", "bound_queue": "data.holding.audit.q"},]

        :param publish_exchange: Name of the exchange that the  producer will publish to.

        :param rabbitmq_host: Host name or IP of the rabbitMQ server. e.g. 127.0.0.1

        :param rabbitmq_port: Port the rabbitmq server listens on e.g. 5674

        :param rabbitmq_user: Username for the rabbitMQ server e.g. guest

        :param rabbitmq_pass: Password for the rabbitMQ server e.g. guest

        :param retry_delay: initial delay between attempts.

        :param retry_backoff: multiplier applied to delay between attempts.

        :param retry_jitter: extra seconds added to delay between attempts.
                   fixed if a number, random if a range tuple (min, max)

        :param retry_max_delay: the maximum value of delay.

        :param prefetch_count: Number of un-acked messages that can be consumed

        :param connection_name: Name of the connection that will be visible in the rabbitmq admin console
        """
        super().__init__(
            rabbitmq_host=rabbitmq_host,
            rabbitmq_port=rabbitmq_port,
            rabbitmq_user=rabbitmq_user,
            rabbitmq_pass=rabbitmq_pass,
            retry_delay=retry_delay,
            retry_backoff=retry_backoff,
            retry_jitter=retry_jitter,
            retry_max_delay=retry_max_delay,
            retry_tries=retry_tries,
            connection_name=connection_name,
            prefetch_count=prefetch_count,
            heartbeat=HOUR_1
        )
        if isinstance(producer_queue_bindings, dict):
            producer_queue_bindings = [producer_queue_bindings]
        self.producer_queue_bindings = producer_queue_bindings
        self.publish_exchange = publish_exchange
        self.publish_message_properties = pika.BasicProperties(
            content_type="text/plain", priority=0, delivery_mode=2, content_encoding="UTF-8"
        )

    def _connect_producer(self) -> None:
        """
        Configures and initiates producer connection to the RabbitMQ server.
        :return:
        """
        if not self.is_connected:
            super().connect()

        for queue_binding in self.producer_queue_bindings:
            self.channel.queue_declare(queue=queue_binding["bound_queue"], durable=True)
            logger.info(f"Queue Created: queue={queue_binding['bound_queue']}")
            self.channel.queue_bind(
                exchange=self.publish_exchange,
                queue=queue_binding["bound_queue"],
                routing_key=queue_binding["routing_key"],
            )
            logger.info(
                f"Bindings configured: exchange={self.publish_exchange}, "
                f"queue={queue_binding['bound_queue']}, "
                f"routing_key={queue_binding['routing_key']} "
            )

    def connect(self) -> None:
        """
        Retries configuration of producer connection to the RabbitMQ server
        :return:None
        """
        retry_call(self._connect_producer, **self.retry_config)
        logger.info(f"Connected to RabbitMQ: " f"connection={self.connection_parameters}")

    def _validate_routing_key(self, routing_key: str):
        """
        Validate that the routing key is configured on the instance to prevent un-route-able posts
        :param routing_key: key to check for the existence of
        :return: True if the routing key exists on the instance. Raise a value error if it does not
        """
        if any([routing_key in binding["routing_key"] for binding in self.producer_queue_bindings]):
            return True

        raise ValueError(
            f"Routing key not configured: "
            f"routing_key={routing_key}, "
            f"initialized_routing_keys="
            f"{[binding['routing_key'] for binding in self.producer_queue_bindings]}"
        )

    def _post(self, routing_key: str, message: dict) -> None:
        """
        Post message to the exchange configured on the producer instance
        :param routing_key: routing key to use on the published message.
            It must exist on the instance binding config
        :param message: body of the message to post
        :return: None
        """
        if not self.is_connected:
            self.connect()

        self.channel.basic_publish(
            exchange=self.publish_exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=self.publish_message_properties,
            mandatory=True,
        )

    # Retry posts which are not confirmed by the broker
    @retry((UnroutableError, NackError), tries=3, delay=1)
    def post(self, routing_key: str, message: dict, validate_routing_key: bool = True) -> None:
        """
        Retry as configured  message post to the exchange configured on the producer instance
        :param routing_key: routing key to use on the published message.
        It must exist on the instance binding config
        :param message: body of the message to post
        :param validate_routing_key: Boolean indicator to validate the routing key was configured during init
        :return: None
        """
        if validate_routing_key:
            self._validate_routing_key(routing_key)
        retry_call(self._post, fargs=[routing_key, message], **self.retry_config)

    def publish_message(self, message) -> None:
        """
        Publish a message using an object constructed with the talus.message.message_class decorator
        :return: None
        """
        if not hasattr(message, 'routing_key') and hasattr(message, 'dict'):
            raise TypeError("Argument 'message' must implement routing_key and dict methods.  "
                        "Recommend using talus.message.message_class decorator")
        self.post(message.routing_key(), message.dict())
