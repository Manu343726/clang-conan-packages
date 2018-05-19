#!/usr/bin/python3

import yaml, sys, itertools

def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

def generate_inputs(template, input_category, input):
    result = []

    for key, values in input.items():
        result.append([(input_category, key, value) for value in values])

    return result

def input_matrix(template, inputs):
    result = []

    for input in inputs:
        result += generate_inputs(template, input, template[input])

    result = list(itertools.product(*result))
    return result

def format_flag(packages, flag_tuple):
    category, name, value = flag_tuple

    if category == "settings":
        return " ".join("-s {}:{}={}".format(package, name, value) for package in packages)
    elif category == "options":
        return " ".join("-o {}:{}={}".format(package, name, value) for package in packages)


def format_flags(packages, flags_tuple):
    return ' '.join(format_flag(packages, e) for e in flags_tuple)

def pretty_format_flag(flag_tuple):
    _, name, value = flag_tuple
    return "{}={}".format(name, value)

def pretty_format_flags(flags_tuple):
    return '+'.join(pretty_format_flag(e) for e in flags_tuple)

def filter_package_args(package_args, expected_category):
    filtered = []
    others = []

    for arg in package_args:
        category, name, value = arg

        if category == expected_category:
            filtered.append((name, value))
        else:
            others.append(arg)

    return (filtered, tuple(others))

def generate_gitlab_package(gitlab_ci, remote, packages, compiler, version, user, channel, package_args):
    job = "{}_{}_{}_{}".format('+'.join(template["packages"]), version, compiler, pretty_format_flags(package_args))
    build_job = "build_" + job
    test_job = "test_" + job
    deploy_job = "deploy_" + job

    settings, others = filter_package_args(package_args, "settings")

    print("gitlab ci job " + job)

    gitlab_ci[build_job] = {
        "tags": ["linux", "docker"],
        "image": "lasote/conan" + compiler,
        "stage": "build",
        "artifacts": {"paths": ["conan_data/"]},
        "script": ["conan profile update settings.{}={} default".format(name, value) for name, value in settings] + \
                  ["CONAN_VERSION_OVERRIDE={version} conan create --profile=default {flags} {package} {user}/{channel} && conan remove -b -s -f \"*\"".format(version=version, package=package, user=user, channel=channel, flags=format_flags(packages, others)) for package in packages] + \
                  ["cp -r /home/conan/.conan/ conan_data/"]
    }

    gitlab_ci[deploy_job] = {
        "tags": ["linux", "docker"],
        "image": "lasote/conan" + compiler,
        "stage": "deploy",
        "dependencies": [build_job],
        "script": [
            "cp -rf conan_data/.conan /home/conan/",
            "conan user {} -p ${} -r {}".format(template["remote"]["user"], template["remote"]["password"], template["remote"]["name"])
        ] + \
            ["conan upload {}/{}@{}/{} -r {} --all".format(package, version, user, channel, remote) for package in packages]
    }


def generate_gitlab(template):
    gitlab_ci = {}

    gitlab_ci['before_script'] = [
        "conan remote add {} {}".format(template["remote"]["name"], template["remote"]["url"]),
        "conan profile new --detect default"
    ]

    package_matrix = input_matrix(template, ["settings", "options"])

    for compiler in template["compilers"]:
        for version in template["versions"]:
            for package_args in package_matrix:
                generate_gitlab_package(gitlab_ci, template["remote"]["name"], template["packages"], compiler, version, template["channel"]["user"], template["channel"]["channel"], package_args)

    yaml.dump(gitlab_ci, open('.gitlab-ci.yml', 'w'), default_flow_style = False)

with open('ci_template.yml') as template_file:
    try:
        template_yaml = yaml.load_all(template_file)
        template = list(template_yaml)[0]

        generate_gitlab(template)
    except yaml.YAMLError as err:
        eprint("Error loading Ci template file: {}", err)
