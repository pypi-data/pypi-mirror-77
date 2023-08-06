"""
Copyright (c) 2020 AudienceProject ApS (https://audienceproject.com)
"""
import time
import uuid as uuidlib
from typing import Dict, Optional, Any

import boto3


class ArtifactsMetadataClient:
    """
    Class which provides functionality for:
         - logging metadata information about artifacts to DynamoDB
         - retrieving metadata information about artifacts from DynamoDB
         - searching for artifacts based on various criteria being matched against metadata
    """

    def __init__(self, table_name: str = "artifacts_metadata", dynamodb_resource=None):
        if dynamodb_resource is None:
            session = boto3.session.Session()
            dynamodb_resource = session.resource("dynamodb")
        self.table = dynamodb_resource.Table(table_name)

    @staticmethod
    def get_uuid() -> str:
        """
        Returns a UUID

        @return: A UUID
        """
        return str(uuidlib.uuid1())

    def log(self, artifact_type: str, uuid: str = get_uuid,
            metadata: Optional[Dict[str, object]] = None) -> str:
        """
        Stores a dictionary of metadata into DynamoDB. Will always create a record,
        it does not update.
        If the location key is part of the dictionary, it will look for a {artifact-id}
        template variable that will be replaced by the id of the record to be inserted.

        @param artifact_type: A string categorization for artifacts.
        @param uuid: Optionally hardcode the ID of the metadata artifact
        @param metadata: A dictionary of values. Can be deep, but must conform to the
            constraints of a DynamoDB PUT operation.

        @return: The id of the artifact.
        """
        if metadata is None:
            metadata = {}
        metadata["id"] = uuid
        metadata["artifactType"] = artifact_type
        if "timestamp" not in metadata:
            metadata["timestamp"] = int(round(time.time() * 1000))
        if "location" in metadata:
            metadata["location"] = metadata["location"].replace("{artifact-id}", metadata["id"])
        self.table.put_item(
            Item=metadata
        )
        return metadata["id"]

    def get(self, artifact_id: str) -> Dict[str, Any]:
        """
        Returns the medata associated with a give id.

        @param artifact_id: The id of the artifact's metadata as it is stored in DynamoDB
        @return: A dictionary of values representing the whole metadata associated with
            a particular artifact id.
        """
        return self.table.get_item(Key={"id": artifact_id})["Item"]

    def log_with_reference_time_as_date_string(self, artifact_type: str, date: str,
                                               metadata: Optional[Dict[str, object]] = None) -> str:
        """
        Simplify providing a reference date when saving the metadata.

        @param artifact_type: A string categorization for artifacts.
        @param date: Reference date
        @param metadata: A dictionary of values. Can be deep, but must conform to the
            constraints of a DynamoDB PUT operation.
        """
        metadata["yyyy"] = int(date.split("-")[0])
        metadata["mm"] = int(date.split("-")[1])
        metadata["dd"] = int(date.split("-")[2])
        return self.log(artifact_type, metadata)
