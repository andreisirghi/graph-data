#!/usr/bin/env python

import json
import sys
import io

import click
import structlog
from faker import Factory

from .generator import generate_student

PY2 = (sys.version_info[0] == 2)

PRETTY_JSON_KWARGS = dict(
    ensure_ascii=False,
    indent=2,
    sort_keys=True)

logger = structlog.get_logger(__name__)
fake = Factory.create('en_US')


class Namespace():
    """
    Simple attribute container.

    This is like types.SimpleNamespace in Python 3.3+.
    """
    pass


def main():
    return cli(obj=Namespace())


@click.group()
@click.option(
    '--output', '-o',
    help="output file location (default is stdout)",
    type=click.File('wb'),
    default=sys.stdout if PY2 else sys.stdout.buffer)
@click.option(
    '--output_dir',
    help="output dif for dump generation",
    default='/tmp/graph-dump')
@click.option(
    '--batches',
    help="number of batches to generate",
    default='50')
@click.option(
    '--batch_size',
    help="batch size",
    default='50')
@click.pass_context
def cli(ctx,
        output,
        output_dir,
        batches,
        batch_size):
    ctx.obj.output_dir = output_dir
    ctx.obj.batches = int(batches)
    ctx.obj.batch_size = int(batch_size)
    ctx.obj.entity_uuids = []
    ctx.obj.closeable = False
    if PY2 and output == sys.stdout:
        # The TextIOWrapper in Python 2 chokes on stdin/stdout. :-(
        import codecs
        ctx.obj.output = codecs.getwriter('utf-8')(output)
    else:
        ctx.obj.output = io.TextIOWrapper(output, encoding='UTF-8')
    if output != sys.stdout and output != sys.stdout.buffer:
        ctx.obj.closeable = True


@cli.command(help="Generate #`batches` of fake students and dumps "
                  "them in a `folder`, each batch in a separate file. "
                  "Each batch has #`batch_size` students")
@click.pass_context
def dump(ctx):
    logger.info('students.faker.dump.start', folder=ctx.obj.output_dir)

    more_batches = ctx.obj.batches
    batch_nr = 1
    while more_batches:
        with io.TextIOWrapper(
                open(ctx.obj.output_dir + "/" +
                     ('{0:05d}'.format(batch_nr)) + ".json",
                     mode='wb'),
                encoding='utf-8') as output:
            students = []
            more_students = ctx.obj.batch_size
            while more_students:
                students.append(generate_student())
                more_students -= 1
            json.dump({"data": students}, output, **PRETTY_JSON_KWARGS)
        more_batches -= 1
        batch_nr += 1

    logger.info('students.faker.dump.done')


@cli.command(help="Generate single batch of fake students."
                  "Batch size is given by batch_size parameter.")
@click.pass_context
def batch(ctx):
    students = []
    more_students = ctx.obj.batch_size
    while more_students:
        students.append(generate_student())
        more_students -= 1
    json.dump({"data": students}, ctx.obj.output, **PRETTY_JSON_KWARGS)
    if ctx.obj.closeable:
        ctx.obj.output.close()
