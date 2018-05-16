#!/usr/bin/python3

import yaml, sys

def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

def generate_gitlab_package(gitlab_ci, package, compiler, version, user, channel):
    job = "{}-{}-{}".format(package, version, compiler)
    build_job = "build-" + job
    test_job = "test-" + job
    deploy_job = "deploy-" + job

    gitlab_ci[build_job] = {
        "tags": ["linux", "docker"],
        "image": "lasote/conan" + compiler,
        "script": [
            "CONAN_VERSION_OVERRIDE={} conan create {} {}/{}".format(version, package, user, channel)
        ]
    }


def generate_gitlab(template):
    gitlab_ci = {}

    gitlab_ci['before_script'] = [
        "conan remote add {} {}".format(template["remote"]["name"], template["remote"]["url"]),
        "conan user {} -p ${} -r {}".format(template["remote"]["user"], template["remote"]["password"], template["remote"]["name"])
    ]

    for package in template["packages"]:
        for compiler in template["compilers"]:
            for version in template["versions"]:
                generate_gitlab_package(gitlab_ci, package, compiler, version, template["channel"]["user"], template["channel"]["channel"])

    yaml.dump(gitlab_ci, open('.gitlab.ci', 'w'), default_flow_style = False)

with open('ci_template.yml') as template_file:
    try:
        template_yaml = yaml.load_all(template_file)
        template = list(template_yaml)[0]
        print("template loaded: {}", yaml.dump(template, default_flow_style=False))

        generate_gitlab(template)
    except yaml.YAMLError as err:
        eprint("Error loading Ci template file: {}", err)
