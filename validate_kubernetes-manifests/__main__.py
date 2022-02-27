import time
from argparse import ArgumentParser
from os import fdopen
from pathlib import Path
from subprocess import run, PIPE
from tempfile import mkstemp

# Kubernetes seems to use yaml 1.1 (https://github.com/kubernetes/kubernetes/issues/34146)
# Should switch to ruamel.yaml if it switches to yaml 1.2 as explained here
# https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python/38922434#38922434
import yaml
from junit_xml import TestSuite, TestCase, to_xml_report_string, to_xml_report_file


def apply_manifests(manifests: str, output_file_path: str):
    test_suites = []

    for manifest in manifests:
        test_suite = TestSuite(Path(manifest).name, [])
        test_suites.append(test_suite)

        with open(manifest, 'r') as _file:
            manifest = yaml.safe_load(_file)

        for _yaml in manifest['items']:
            file_descriptor, file_path = mkstemp()
            with fdopen(file_descriptor, 'w') as _file:
                _file.write(yaml.dump(_yaml))

            start_time = time.perf_counter()
            process = run(['oc', 'apply', '--dry-run=server', '--server-side=true', '-f', file_path],
                          stdout=PIPE, stderr=PIPE)
            stdout = process.stdout
            stderr = process.stderr
            elapsed_time = time.perf_counter() - start_time

            test_suite.test_cases.append(TestCase(_yaml['metadata']['name'], _yaml['kind'],
                                                  elapsed_time, stdout.decode('utf-8'), stderr.decode('utf-8')))

    if output_file_path:
        with open(output_file_path, 'w') as f:
            to_xml_report_file(f, test_suites, prettyprint=True)
    else:
        print(to_xml_report_string(test_suites, prettyprint=True))


def main():
    parser = ArgumentParser()
    parser.add_argument('--manifests', nargs='+', dest='manifests',
                        help='Manifests to test', required=True)
    parser.add_argument('-o', '--output-file', dest='output_file',
                        help='The output file path', required=False)

    args = parser.parse_args()

    apply_manifests(args.manifests, args.output_file)


if __name__ == "__main__":
    main()
