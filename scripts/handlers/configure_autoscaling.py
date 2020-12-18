import argparse
import os
import sys

current_dir = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{dir_path}/../")

from service import service_handler
from binding import binding_handler
from autoscaling_json_policy_generator import autoscaling_handler


def parse_arguments():
    description = "Arguments for configure_autoscaling.py"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-app",
        help="The name of the app to configure autoscaling for",
        dest="app",
        required=True,
    )
    parser.add_argument(
        "-cpu",
        help="If present, ensures a CPU block is present in the ASG",
        dest="cpu",
        required=False,
    )
    parser.add_argument(
        "-cpu-breach-duration-seconds",
        help="Defines the breach duration seconds for the CPU Metric",
        dest="cpu_breach_duration_seconds",
        required=False,
    )
    parser.add_argument(
        "-cpu-cool-down-secs",
        help="Defines the cool down settings for the CPU Metric",
        dest="cpu_cool_down_secs",
        required=False,
    )
    parser.add_argument(
        "-cpu-threshold",
        help="Defines the threshold for the CPU Metric",
        dest="cpu_threshold",
        required=False,
    )
    parser.add_argument(
        "-instance-max-count",
        help="The max count for the number of instances (to define in ASG)",
        dest="instance_max_count",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-instance-min-count",
        help="The min count for the number of instances (to define in ASG)",
        dest="instance_min_count",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-organisation",
        help="The organisation to create resources within",
        dest="organisation",
        required=True,
    )
    parser.add_argument(
        "-parameters",
        help="The paramters to assign to autoscaling group",
        dest="parameters",
        required=False,
    )
    parser.add_argument(
        "-space",
        help="The name of the space to create resources for",
        dest="space",
        required=True,
    )
    parser.add_argument(
        "-throughput",
        help="If present, ensures a throughput block is present in the ASG",
        dest="throughput",
        required=False,
        default=True,
    )
    parser.add_argument(
        "-throughput-breach-duration-seconds",
        help="Defines the breach duration seconds for the throughput Metric",
        dest="throughput_breach_duration_seconds",
        required=False,
        default=60,
    )
    parser.add_argument(
        "-throughput-cool-down-secs",
        help="Defines the cool down settings for the throughput Metric",
        dest="throughput_cool_down_secs",
        required=False,
        default=60,
    )
    parser.add_argument(
        "-throughput-threshold",
        help="Defines the threshold for the throughput Metric",
        dest="throughput_threshold",
        required=False,
        default=90,
    )
    return parser.parse_args()


# Set arguments
args = parse_arguments()
app = args.app
cpu = args.cpu
cpu_breach_duration_seconds = args.cpu_breach_duration_seconds
cpu_cool_down_secs = args.cpu_cool_down_secs
cpu_threshold = args.cpu_threshold
organisation = args.organisation
organisation_space = args.space
parameters = args.parameters
instance_max_count = args.instance_max_count
instance_min_count = args.instance_min_count
instance_name = f"scale-{app}"
throughput = args.throughput
throughput_breach_duration_seconds = args.throughput_breach_duration_seconds
throughput_cool_down_secs = args.throughput_cool_down_secs
throughput_threshold = args.throughput_threshold


# Call methods
print(f"Creating autoscaling service {instance_name} for {app}")
service_handler(
    instance_name=instance_name,
    organisation=organisation,
    organisation_space=organisation_space,
    parameters=parameters,
    service_plan="autoscaler-free-plan",
)

print(f"Creating binding for {app} to {instance_name}")
binding_handler(
    app=app,
    instance=instance_name,
    organisation=organisation,
    organisation_space=organisation_space,
)

print(f"Creating JSON policy for {app}")
autoscaling_handler(
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
)
