import json
import os
import subprocess
from cf_common import exception_handler_function, cf_cli_initialise


def create_initial_autoscaling_policy(instance_max_count, instance_min_count):
    autoscaling_policy = {
        "instance_min_count": instance_min_count,
        "instance_max_count": instance_max_count,
        "scaling_rules": [],
    }
    return autoscaling_policy


def create_metric_types_dict(cpu, throughput):
    metric_types_dict = {"cpu": cpu, "throughput": throughput}
    return metric_types_dict


def create_cpu_values_dict(
    cpu_breach_duration_seconds, cpu_threshold, cpu_cool_down_secs
):
    cpu_values_dict = {
        "cpu": [
            {
                "metric_type": "cpu",
                "breach_duration_secs": cpu_breach_duration_seconds,
                "threshold": cpu_threshold,
                "operator": "<",
                "cool_down_secs": cpu_cool_down_secs,
                "adjustment": "-1",
            },
            {
                "metric_type": "cpu",
                "breach_duration_secs": cpu_breach_duration_seconds,
                "threshold": cpu_threshold,
                "operator": ">=",
                "cool_down_secs": cpu_cool_down_secs,
                "adjustment": "+1",
            },
        ]
    }
    return cpu_values_dict


def create_throughput_values_dict(
    throughput_breach_duration_seconds, throughput_threshold, throughput_cool_down_secs
):
    throughput_values_dict = {
        "throughput": [
            {
                "metric_type": "throughput",
                "breach_duration_secs": throughput_breach_duration_seconds,
                "threshold": throughput_threshold,
                "operator": "<",
                "cool_down_secs": throughput_cool_down_secs,
                "adjustment": "-1",
            },
            {
                "metric_type": "throughput",
                "breach_duration_secs": throughput_breach_duration_seconds,
                "threshold": throughput_threshold,
                "operator": ">=",
                "cool_down_secs": throughput_cool_down_secs,
                "adjustment": "+1",
            },
        ]
    }
    return throughput_values_dict


def get_metrics_to_append(metric_types_dict):
    metrics_to_append = []
    for metric_key, metric_value in metric_types_dict.items():
        if metric_value:
            metrics_to_append.append(metric_key)

    return metrics_to_append


def append_metric_parameters_to_policy(autoscaling_policy, dict, metric):
    print(f"Retrieving autoscaling values for the {metric} metric")
    try:
        for metric_values in dict[metric]:
            for single_key, single_value in metric_values.items():
                if not single_value:
                    exception_handler_function(
                        msg=f"Value {single_key} for {metric} cannot be {single_value}"
                    )
            autoscaling_policy["scaling_rules"].append(metric_values)
    except KeyError as e:
        exception_handler_function(
            msg=f"Key error when attempting to create config for {metric}: {e}"
        )
    print(f"Successfully added ASG values for {metric}")


def attach_autoscaling_policy(app, policy_json_filename):
    try:
        print(f"Attaching autoscaling policy to {app}")
        attach_asg_response = subprocess.call(
            ["cf", "attach-autoscaling-policy", app, policy_json_filename]
        )
        if attach_asg_response != 0:
            exception_handler_function(
                msg=f"Failed to attach ASG policy, received return value {attach_asg_response}"
            )
            cleanup_policy_json_filename(policy_json_filename=policy_json_filename)
        print(f"Attached autoscaling policy to {app}")
    except subprocess.CalledProcessError as e:
        exception_handler_function(
            msg=f"Failed to attach ASG policy, received subprocess error: {e}"
        )
        cleanup_policy_json_filename(policy_json_filename=policy_json_filename)


def cleanup_policy_json_filename(policy_json_filename):
    os.remove(policy_json_filename)


def autoscaling_handler(
    app,
    cpu,
    cpu_breach_duration_seconds,
    cpu_threshold,
    cpu_cool_down_secs,
    instance_max_count,
    instance_min_count,
    organisation,
    organisation_space,
    throughput,
    throughput_breach_duration_seconds,
    throughput_threshold,
    throughput_cool_down_secs,
    policy_json_filename="policy.json",
):
    autoscaling_policy = create_initial_autoscaling_policy(
        instance_max_count=instance_max_count, instance_min_count=instance_min_count
    )
    metrics_type_dict = create_metric_types_dict(cpu=cpu, throughput=throughput)
    cpu_values_dict = create_cpu_values_dict(
        cpu_breach_duration_seconds=cpu_breach_duration_seconds,
        cpu_threshold=cpu_threshold,
        cpu_cool_down_secs=cpu_cool_down_secs,
    )
    throughput_values_dict = create_throughput_values_dict(
        throughput_breach_duration_seconds=throughput_breach_duration_seconds,
        throughput_threshold=throughput_threshold,
        throughput_cool_down_secs=throughput_cool_down_secs,
    )
    metrics = get_metrics_to_append(metric_types_dict=metrics_type_dict)
    for metric in metrics:
        if metric == "cpu":
            append_metric_parameters_to_policy(
                autoscaling_policy=autoscaling_policy,
                dict=cpu_values_dict,
                metric=metric,
            )
        elif metric == "throughput":
            append_metric_parameters_to_policy(
                autoscaling_policy=autoscaling_policy,
                dict=throughput_values_dict,
                metric=metric,
            )

    with open(policy_json_filename, "w") as json_file:
        json.dump(autoscaling_policy, json_file)
        print("Created policy.json file")

    cf_cli_initialise(organisation=organisation, space=organisation_space)
    attach_autoscaling_policy(app=app, policy_json_filename=policy_json_filename)
    cleanup_policy_json_filename(policy_json_filename=policy_json_filename)
