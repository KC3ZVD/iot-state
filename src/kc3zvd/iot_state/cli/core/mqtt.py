from kc3zvd.iot_state.publishers import mqtt as p
import click

@click.group()
@click.option('--host', help="The MQTT host to connect to", default='localhost', type=str)
@click.option('--port', help="The port to use to connect to the MQTT host", default=1883, type=int)
@click.option('--topic_prefix', help="The prefix to use for the MQTT topic", default='', type=str)
@click.pass_context
def mqtt(ctx, host, port, topic_prefix):
    ctx.ensure_object(dict)
    try:
        if topic_prefix[-1] != '/':
            topic_prefix = f"{topic_prefix}/"
    except IndexError:
        pass


    ctx.obj['mqtt'] = {
        "host": host,
        "port": port,
        "topic_prefix": topic_prefix
    }

@mqtt.command() 

@click.pass_context
def publisher(ctx):
    p.run()
