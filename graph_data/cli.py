#!/usr/bin/env python

import json
import sys
import io
import click
import structlog

from os import listdir
from os.path import isfile, join
from datetime import datetime
from faker import Factory

from . import generator, neo4j

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
    help="output dir for dump generation",
    default='/tmp/graph-dump')
@click.option(
    '--batches',
    help="number of batches to generate",
    default='50')
@click.option(
    '--batch_size',
    help="batch size",
    default='50')
@click.option(
    '--neo4j_url',
    help="neo4j url",
    default='http://localhost:7474')
@click.pass_context
def cli(ctx,
        output,
        output_dir,
        batches,
        batch_size,
        neo4j_url):
    ctx.obj.output_dir = output_dir
    ctx.obj.batches = int(batches)
    ctx.obj.batch_size = int(batch_size)
    ctx.obj.neo4j_url = neo4j_url
    ctx.obj.entity_uuids = []
    ctx.obj.closeable = False
    if PY2 and output == sys.stdout:
        # The TextIOWrapper in Python 2 chokes on stdin/stdout. :-(
        import codecs
        ctx.obj.output = codecs.getwriter('utf-8')(output)
    else:
        ctx.obj.output = io.TextIOWrapper(output, encoding='utf-8')
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
        start_time = datetime.now()
        file_name = ('{0:05d}'.format(batch_nr)) + ".json"
        file_path = ctx.obj.output_dir + "/" + file_name
        with io.TextIOWrapper(
                open(file_path, mode='wb'), encoding='utf-8') as output:
            students = []
            more_students = ctx.obj.batch_size
            while more_students:
                students.append(generator.generate_student())
                more_students -= 1
            json.dump({"data": students}, output, **PRETTY_JSON_KWARGS)
        end_time = datetime.now()
        duration = end_time - start_time
        more_batches -= 1
        batch_nr += 1
        logger.info(
            'batch.done', file=file_name,
            duration_seconds='{:.3f}'.format(duration.total_seconds()))
    logger.info('students.faker.dump.done')


@cli.command(help="Generate single batch of fake students."
                  "Batch size is given by batch_size parameter.")
@click.pass_context
def batch(ctx):
    students = []
    more_students = ctx.obj.batch_size
    while more_students:
        students.append(generator.generate_student())
        more_students -= 1
    json.dump({"data": students}, ctx.obj.output, **PRETTY_JSON_KWARGS)
    if ctx.obj.closeable:
        ctx.obj.output.close()


@cli.command(help="Loads a dump of generated data into neo4j in JSON mode")
@click.pass_context
def neo4j_load_dump_json(ctx):
    neo4j.ctx = ctx.obj
    neo4j.create_schema()
    logger.info('neo4j.json.ingest.start', folder=ctx.obj.output_dir)

    batch_files = [f for f in listdir(ctx.obj.output_dir)
                   if isfile(join(ctx.obj.output_dir, f))
                   and f.endswith('.json')]

    student_ids = []
    for file in batch_files:
        with open(join(ctx.obj.output_dir, file), mode='r',
                  encoding='utf-8') as input:
            students = []
            json_data = json.load(input)
            for item in json_data['data']:
                student_ids.append(item['idno'])

            start_time = datetime.now()
            for item in json_data['data']:
                student = {
                    'idno': item['idno'],
                    'characteristics': item['characteristics'],
                    'properties': {k: v for k, v in item.items()
                                   if k not in ('idno', 'characteristics')}
                }
                friends = generator.pick_friends(student_ids)
                friends = [f for f in friends if f != item['idno']]
                student['friends'] = friends
                students.append(student)

            logger.info('neo4j.json.ingest.batch', file=file)
            rs = neo4j.do_query_update(neo4j.Q_IN_STUDENTS, {'students': students})
            end_time = datetime.now()
            neo4j.log_update_query_stats(end_time-start_time, rs)

    logger.info('neo4j.json.ingest.done')
