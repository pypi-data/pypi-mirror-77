# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CreateExperimentDto(Model):
    """CreateExperimentDto.

    :param description:
    :type description: str
    :param generator_config:
    :type generator_config:
     ~hyperdrive.models.CreateExperimentDtoGeneratorConfig
    :param max_concurrent_jobs:
    :type max_concurrent_jobs: int
    :param max_duration_minutes:
    :type max_duration_minutes: int
    :param max_total_jobs:
    :type max_total_jobs: int
    :param name:
    :type name: str
    :param platform:
    :type platform: str
    :param platform_config:
    :type platform_config: object
    :param policy_config:
    :type policy_config: ~hyperdrive.models.CreateExperimentDtoPolicyConfig
    :param primary_metric_config:
    :type primary_metric_config:
     ~hyperdrive.models.CreateExperimentDtoPrimaryMetricConfig
    :param resume_from:
    :type resume_from: list[~hyperdrive.models.RunKey]
    :param resume_child_runs:
    :type resume_child_runs: list[~hyperdrive.models.RunKey]
    :param study_id:
    :type study_id: int
    :param user:
    :type user: str
    """

    _validation = {
        'description': {'max_length': 511},
        'generator_config': {'required': True},
        'max_concurrent_jobs': {'maximum': 100, 'minimum': 1},
        'max_duration_minutes': {'maximum': 43200, 'minimum': 1},
        'max_total_jobs': {'maximum': 1000, 'minimum': 1},
        'name': {'required': True, 'max_length': 255},
        'platform': {'required': True},
        'platform_config': {'required': True},
        'policy_config': {'required': True},
        'primary_metric_config': {'required': True},
        'study_id': {'minimum': 0},
        'user': {'required': True, 'max_length': 255},
    }

    _attribute_map = {
        'description': {'key': 'description', 'type': 'str'},
        'generator_config': {'key': 'generator_config', 'type': 'CreateExperimentDtoGeneratorConfig'},
        'max_concurrent_jobs': {'key': 'max_concurrent_jobs', 'type': 'int'},
        'max_duration_minutes': {'key': 'max_duration_minutes', 'type': 'int'},
        'max_total_jobs': {'key': 'max_total_jobs', 'type': 'int'},
        'name': {'key': 'name', 'type': 'str'},
        'platform': {'key': 'platform', 'type': 'str'},
        'platform_config': {'key': 'platform_config', 'type': 'object'},
        'policy_config': {'key': 'policy_config', 'type': 'CreateExperimentDtoPolicyConfig'},
        'primary_metric_config': {'key': 'primary_metric_config', 'type': 'CreateExperimentDtoPrimaryMetricConfig'},
        'resume_from': {'key': 'resume_from', 'type': '[RunKey]'},
        'resume_child_runs': {'key': 'resume_child_runs', 'type': '[RunKey]'},
        'study_id': {'key': 'study_id', 'type': 'int'},
        'user': {'key': 'user', 'type': 'str'},
    }

    def __init__(self, generator_config, name, platform, platform_config, policy_config, primary_metric_config, user, description=None, max_concurrent_jobs=None, max_duration_minutes=None, max_total_jobs=None, resume_from=None, resume_child_runs=None, study_id=None):
        super(CreateExperimentDto, self).__init__()
        self.description = description
        self.generator_config = generator_config
        self.max_concurrent_jobs = max_concurrent_jobs
        self.max_duration_minutes = max_duration_minutes
        self.max_total_jobs = max_total_jobs
        self.name = name
        self.platform = platform
        self.platform_config = platform_config
        self.policy_config = policy_config
        self.primary_metric_config = primary_metric_config
        self.resume_from = resume_from
        self.resume_child_runs = resume_child_runs
        self.study_id = study_id
        self.user = user
