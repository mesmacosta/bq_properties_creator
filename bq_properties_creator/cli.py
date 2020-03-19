"""Console script for bq_properties_creator."""
import sys
import click

from google.cloud import bigquery
from jinja2 import Template


@click.command()
@click.option('--batch-size', default=1000, help='Rows batch size.')
@click.option('--sample-size', default=0, help='Rows sample size.')
@click.option('--shard-size', default=50, help='Shard size to distribute and bucket the rows.')
@click.option('--verbose-logging', default='false', help='Enable verbose logging.')
@click.option('--file-dest', default='config.properties',
              help='Destination where file will be created.')
@click.option('--project-id', help='Your Google Project id.', required=True)
def main(**kargs):
    template = Template("""rows.batch.size={{ batch_size }}
rows.sample.size={{ sample_size }}
rows.shard.size={{ shard_size }}
verbose.logging={{ verbose_logging }}
bigquery.tables={{ bigquery_tables }}
bigquery.tables.count={{ bigquery_tables_count }}
""")

    bq_results = get_bigquery_results(kargs['project_id'])

    print('BigQuery results: {}'.format(bq_results))

    bigquery_tables_count, bigquery_tables_strings = build_bigquery_tables_strings(bq_results)

    kargs['bigquery_tables'] = bigquery_tables_strings
    kargs['bigquery_tables_count'] = bigquery_tables_count

    render = template.render(kargs)

    with open(kargs['file_dest'], 'w', encoding='utf-8') as f:
        f.write(render)

    return 0


def get_bigquery_results(project_id):
    # Construct a BigQuery client object.
    client = bigquery.Client()
    datasets = list(client.list_datasets(project=project_id))  # Make an API request.
    project = client.project
    bq_results = {
        'project': project,
        'datasets': []
    }
    if datasets:
        bq_results['datasets'].extend([(dataset.dataset_id, []) for dataset in datasets])

        for dataset_id, tables in bq_results['datasets']:
            tables_reponse = client.list_tables(dataset_id)
            tables.extend([table.table_id for table in tables_reponse])
        pass

    else:
        print('{} project does not contain any datasets.'.format(project))
    return bq_results


def build_bigquery_tables_strings(bq_results):
    bigquery_tables_strings = []

    project = bq_results['project']
    template_str = '{}:{}.{}'
    template_str = template_str.replace('{}', project, 1)

    for dataset_id, tables in bq_results['datasets']:
        bigquery_table_string = template_str.replace('{}', dataset_id, 1)
        for table in tables:
            bigquery_tables_strings.append(bigquery_table_string.replace('{}', table, 1))

    return len(bigquery_tables_strings), ",".join(bigquery_tables_strings)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
