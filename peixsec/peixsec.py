import pika


def callback(ch, method, properties, body) -> None:
    print(" [x] Received %r" % body)


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-service'))
    channel = connection.channel()
    channel.queue_declare(queue='position_request', durable=True, exclusive=False, auto_delete=False)
    channel.basic_consume(queue='position_request', auto_ack=True, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


if __name__ == "__main__":
    main()
