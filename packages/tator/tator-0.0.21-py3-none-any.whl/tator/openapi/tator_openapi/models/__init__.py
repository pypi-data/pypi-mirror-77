# coding: utf-8

# flake8: noqa
"""
    Tator REST API

    Interface to the Tator backend.  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from tator.openapi.tator_openapi.models.algorithm import Algorithm
from tator.openapi.tator_openapi.models.algorithm_launch import AlgorithmLaunch
from tator.openapi.tator_openapi.models.algorithm_launch_spec import AlgorithmLaunchSpec
from tator.openapi.tator_openapi.models.algorithm_manifest import AlgorithmManifest
from tator.openapi.tator_openapi.models.algorithm_manifest_spec import AlgorithmManifestSpec
from tator.openapi.tator_openapi.models.algorithm_spec import AlgorithmSpec
from tator.openapi.tator_openapi.models.analysis import Analysis
from tator.openapi.tator_openapi.models.analysis_spec import AnalysisSpec
from tator.openapi.tator_openapi.models.archive_config import ArchiveConfig
from tator.openapi.tator_openapi.models.attribute_bulk_update import AttributeBulkUpdate
from tator.openapi.tator_openapi.models.attribute_type import AttributeType
from tator.openapi.tator_openapi.models.audio_definition import AudioDefinition
from tator.openapi.tator_openapi.models.autocomplete_service import AutocompleteService
from tator.openapi.tator_openapi.models.bad_request_response import BadRequestResponse
from tator.openapi.tator_openapi.models.color_map import ColorMap
from tator.openapi.tator_openapi.models.create_list_response import CreateListResponse
from tator.openapi.tator_openapi.models.create_response import CreateResponse
from tator.openapi.tator_openapi.models.credentials import Credentials
from tator.openapi.tator_openapi.models.encode_config import EncodeConfig
from tator.openapi.tator_openapi.models.fill import Fill
from tator.openapi.tator_openapi.models.leaf import Leaf
from tator.openapi.tator_openapi.models.leaf_spec import LeafSpec
from tator.openapi.tator_openapi.models.leaf_suggestion import LeafSuggestion
from tator.openapi.tator_openapi.models.leaf_type import LeafType
from tator.openapi.tator_openapi.models.leaf_type_spec import LeafTypeSpec
from tator.openapi.tator_openapi.models.leaf_type_update import LeafTypeUpdate
from tator.openapi.tator_openapi.models.leaf_update import LeafUpdate
from tator.openapi.tator_openapi.models.localization import Localization
from tator.openapi.tator_openapi.models.localization_spec import LocalizationSpec
from tator.openapi.tator_openapi.models.localization_type import LocalizationType
from tator.openapi.tator_openapi.models.localization_type_spec import LocalizationTypeSpec
from tator.openapi.tator_openapi.models.localization_type_update import LocalizationTypeUpdate
from tator.openapi.tator_openapi.models.localization_update import LocalizationUpdate
from tator.openapi.tator_openapi.models.media import Media
from tator.openapi.tator_openapi.models.media_files import MediaFiles
from tator.openapi.tator_openapi.models.media_next import MediaNext
from tator.openapi.tator_openapi.models.media_prev import MediaPrev
from tator.openapi.tator_openapi.models.media_spec import MediaSpec
from tator.openapi.tator_openapi.models.media_type import MediaType
from tator.openapi.tator_openapi.models.media_type_spec import MediaTypeSpec
from tator.openapi.tator_openapi.models.media_type_update import MediaTypeUpdate
from tator.openapi.tator_openapi.models.media_update import MediaUpdate
from tator.openapi.tator_openapi.models.membership import Membership
from tator.openapi.tator_openapi.models.membership_spec import MembershipSpec
from tator.openapi.tator_openapi.models.membership_update import MembershipUpdate
from tator.openapi.tator_openapi.models.message_response import MessageResponse
from tator.openapi.tator_openapi.models.move_video_spec import MoveVideoSpec
from tator.openapi.tator_openapi.models.not_found_response import NotFoundResponse
from tator.openapi.tator_openapi.models.notify_spec import NotifySpec
from tator.openapi.tator_openapi.models.progress_spec import ProgressSpec
from tator.openapi.tator_openapi.models.progress_summary_spec import ProgressSummarySpec
from tator.openapi.tator_openapi.models.project import Project
from tator.openapi.tator_openapi.models.project_spec import ProjectSpec
from tator.openapi.tator_openapi.models.s3_storage_config import S3StorageConfig
from tator.openapi.tator_openapi.models.state import State
from tator.openapi.tator_openapi.models.state_spec import StateSpec
from tator.openapi.tator_openapi.models.state_type import StateType
from tator.openapi.tator_openapi.models.state_type_spec import StateTypeSpec
from tator.openapi.tator_openapi.models.state_type_update import StateTypeUpdate
from tator.openapi.tator_openapi.models.state_update import StateUpdate
from tator.openapi.tator_openapi.models.temporary_file import TemporaryFile
from tator.openapi.tator_openapi.models.temporary_file_spec import TemporaryFileSpec
from tator.openapi.tator_openapi.models.token import Token
from tator.openapi.tator_openapi.models.transcode import Transcode
from tator.openapi.tator_openapi.models.transcode_spec import TranscodeSpec
from tator.openapi.tator_openapi.models.user import User
from tator.openapi.tator_openapi.models.user_update import UserUpdate
from tator.openapi.tator_openapi.models.version import Version
from tator.openapi.tator_openapi.models.version_spec import VersionSpec
from tator.openapi.tator_openapi.models.version_update import VersionUpdate
from tator.openapi.tator_openapi.models.video_definition import VideoDefinition
