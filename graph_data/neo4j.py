import json
import requests
import structlog

logger = structlog.get_logger(__name__)

ctx = None

Q_CR_UNIQUE_CONSTRAINT = """
    CREATE CONSTRAINT ON (entity:{type})
    ASSERT entity.{property} IS UNIQUE;
    """

Q_CR_INDEX = """
    CREATE INDEX ON :{type}(`{property}`);
    """

Q_IN_STUDENTS = """
    UNWIND {students} AS student
    MERGE (s:Student {idno:student.idno})
      SET s += student.properties
    FOREACH (characteristic in student.characteristics |
      MERGE (ch:Characteristic {id:characteristic.type+':'+characteristic.value})
        ON CREATE SET ch.type=characteristic.type, ch.value=characteristic.value
      MERGE (s)-[:characteristic]->(ch)
    )
    FOREACH (fr in student.friends |
      MERGE (t:Student {idno:fr})
      MERGE (s)-[:friend]->(t)
    )
    """


def do_query_update(query, params={}):
    """
    Execute one query statement,
    Return result and statistics
    """
    url = get_neo4j_api_url('/db/data/transaction/commit')
    query_request = {
        'statements': [{
            'statement': query,
            'parameters': params,
            'includeStats': True
        }]
    }
    query_request = json.dumps(query_request).encode()
    response = requests.post(url, data=query_request)
    raise_for_update_errors(response)
    return response


def do_query_update_batch(queries):
    """
    Execute multiple query statements,
    Return result and statistics for each of the statements
    """
    url = get_neo4j_api_url('/db/data/transaction/commit')
    statements = []
    for query in queries:
        statement = {
            'statement': query['statement'],
            'parameters': query['params'],
            'includeStats': True
        }
        statements.append(statement)

    query_request = {
        'statements': statements
    }

    query_request = json.dumps(query_request).encode()
    response = requests.post(url, data=query_request)
    raise_for_update_errors(response)
    return response


def raise_for_update_errors(response):
    response.raise_for_status()
    errors = []
    for err in response.json().get('errors'):
        errors.append(err.get('message'))
    if errors:
        message = ";".join(errors)
        raise Exception("Neo4j Query Exception: " + message)


def get_neo4j_api_url(endpoint=None):
    neo4j_url = ctx.neo4j_url
    if not endpoint:
        return neo4j_url
    return neo4j_url + endpoint


def prepare_query(query, params):
    """Replace template query {parameter}s with the
    values provided in the dictionary
    """
    return query.format(**params)


def create_schema():
    """
    Create database indexes and uniqueness constraints
    """
    logger.info('graph.db.schema.prepare')
    # Add Student constraints
    params = {'type': 'Student', 'property': 'idno'}
    do_query_update(prepare_query(Q_CR_UNIQUE_CONSTRAINT, params))
    # Add Characteristic constraints
    params = {'type': 'Characteristic', 'property': 'id'}
    do_query_update(prepare_query(Q_CR_UNIQUE_CONSTRAINT, params))
    params['property'] = 'type'
    do_query_update(prepare_query(Q_CR_INDEX, params))
    params['property'] = 'value'
    do_query_update(prepare_query(Q_CR_INDEX, params))
    logger.info('graph.db.schema.created')


def log_update_query_stats(duration, response, **kwargs):
    update_response = response.json()
    # remove errors block since it's empty
    update_response.pop('errors')
    stats = {}
    for res in update_response['results']:
        for op in res['stats']:
            if op in stats:
                if isinstance(op, bool):
                    stats[op] = stats[op] or res['stats'][op]
                else:
                    stats[op] = stats[op] + res['stats'][op]
            else:
                stats[op] = res['stats'][op]

    logger.info('update_query',
                statistics=stats,
                duration_seconds='{:.3f}'.format(duration.total_seconds()),
                **kwargs)
