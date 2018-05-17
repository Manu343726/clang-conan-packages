#!/usr/bin/python3

import yaml, sys

def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

def generate_gitlab_package(gitlab_ci, remote, packages, compiler, version, user, channel):
    job = "{}_{}_{}".format('+'.join(template["packages"]), version, compiler)
    build_job = "build_" + job
    test_job = "test_" + job
    deploy_job = "deploy_" + job

    gitlab_ci[build_job] = {
        "tags": ["linux", "docker"],
        "image": "lasote/conan" + compiler,
        "script": ["pushd {package} && CONAN_VERSION_OVERRIDE={version} CONAN_USERNAME={user} CONAN_REFERENCE={package}/{version} CONAN_CHANNEL={channel} python ../build.py && popd".format(package=package, user=user, version=version, channel=channel) for package in packages] +
                  ["conan upload {}/{}@{}/{} -r {} --all".format(package, version, user, channel, remote) for package in packages]
    }


def generate_gitlab(template):
    gitlab_ci = {}

    gitlab_ci['before_script'] = [
        "pip install conan_package_tools --user",
        "conan remote add {} {}".format(template["remote"]["name"], template["remote"]["url"]),
        "conan user {} -p ${} -r {}".format(template["remote"]["user"], template["remote"]["password"], template["remote"]["name"])
    ]

    for compiler in template["compilers"]:
        for version in template["versions"]:
            generate_gitlab_package(gitlab_ci, template["remote"]["name"], template["packages"], compiler, version, template["channel"]["user"], template["channel"]["channel"])

    yaml.dump(gitlab_ci, open('.gitlab-ci.yml', 'w'), default_flow_style = False)

with open('ci_template.yml') as template_file:
    try:
        template_yaml = yaml.load_all(template_file)
        template = list(template_yaml)[0]
        print("template loaded: {}", yaml.dump(template, default_flow_style=False))

        generate_gitlab(template)
    except yaml.YAMLError as err:
        eprint("Error loading Ci template file: {}", err)
