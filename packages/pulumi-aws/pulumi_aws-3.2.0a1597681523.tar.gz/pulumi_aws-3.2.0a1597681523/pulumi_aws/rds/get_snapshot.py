# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import _utilities, _tables


class GetSnapshotResult:
    """
    A collection of values returned by getSnapshot.
    """
    def __init__(__self__, allocated_storage=None, availability_zone=None, db_instance_identifier=None, db_snapshot_arn=None, db_snapshot_identifier=None, encrypted=None, engine=None, engine_version=None, id=None, include_public=None, include_shared=None, iops=None, kms_key_id=None, license_model=None, most_recent=None, option_group_name=None, port=None, snapshot_create_time=None, snapshot_type=None, source_db_snapshot_identifier=None, source_region=None, status=None, storage_type=None, vpc_id=None):
        if allocated_storage and not isinstance(allocated_storage, float):
            raise TypeError("Expected argument 'allocated_storage' to be a float")
        __self__.allocated_storage = allocated_storage
        """
        Specifies the allocated storage size in gigabytes (GB).
        """
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        __self__.availability_zone = availability_zone
        """
        Specifies the name of the Availability Zone the DB instance was located in at the time of the DB snapshot.
        """
        if db_instance_identifier and not isinstance(db_instance_identifier, str):
            raise TypeError("Expected argument 'db_instance_identifier' to be a str")
        __self__.db_instance_identifier = db_instance_identifier
        if db_snapshot_arn and not isinstance(db_snapshot_arn, str):
            raise TypeError("Expected argument 'db_snapshot_arn' to be a str")
        __self__.db_snapshot_arn = db_snapshot_arn
        """
        The Amazon Resource Name (ARN) for the DB snapshot.
        """
        if db_snapshot_identifier and not isinstance(db_snapshot_identifier, str):
            raise TypeError("Expected argument 'db_snapshot_identifier' to be a str")
        __self__.db_snapshot_identifier = db_snapshot_identifier
        if encrypted and not isinstance(encrypted, bool):
            raise TypeError("Expected argument 'encrypted' to be a bool")
        __self__.encrypted = encrypted
        """
        Specifies whether the DB snapshot is encrypted.
        """
        if engine and not isinstance(engine, str):
            raise TypeError("Expected argument 'engine' to be a str")
        __self__.engine = engine
        """
        Specifies the name of the database engine.
        """
        if engine_version and not isinstance(engine_version, str):
            raise TypeError("Expected argument 'engine_version' to be a str")
        __self__.engine_version = engine_version
        """
        Specifies the version of the database engine.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if include_public and not isinstance(include_public, bool):
            raise TypeError("Expected argument 'include_public' to be a bool")
        __self__.include_public = include_public
        if include_shared and not isinstance(include_shared, bool):
            raise TypeError("Expected argument 'include_shared' to be a bool")
        __self__.include_shared = include_shared
        if iops and not isinstance(iops, float):
            raise TypeError("Expected argument 'iops' to be a float")
        __self__.iops = iops
        """
        Specifies the Provisioned IOPS (I/O operations per second) value of the DB instance at the time of the snapshot.
        """
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        __self__.kms_key_id = kms_key_id
        """
        The ARN for the KMS encryption key.
        """
        if license_model and not isinstance(license_model, str):
            raise TypeError("Expected argument 'license_model' to be a str")
        __self__.license_model = license_model
        """
        License model information for the restored DB instance.
        """
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        __self__.most_recent = most_recent
        if option_group_name and not isinstance(option_group_name, str):
            raise TypeError("Expected argument 'option_group_name' to be a str")
        __self__.option_group_name = option_group_name
        """
        Provides the option group name for the DB snapshot.
        """
        if port and not isinstance(port, float):
            raise TypeError("Expected argument 'port' to be a float")
        __self__.port = port
        if snapshot_create_time and not isinstance(snapshot_create_time, str):
            raise TypeError("Expected argument 'snapshot_create_time' to be a str")
        __self__.snapshot_create_time = snapshot_create_time
        """
        Provides the time when the snapshot was taken, in Universal Coordinated Time (UTC).
        """
        if snapshot_type and not isinstance(snapshot_type, str):
            raise TypeError("Expected argument 'snapshot_type' to be a str")
        __self__.snapshot_type = snapshot_type
        if source_db_snapshot_identifier and not isinstance(source_db_snapshot_identifier, str):
            raise TypeError("Expected argument 'source_db_snapshot_identifier' to be a str")
        __self__.source_db_snapshot_identifier = source_db_snapshot_identifier
        """
        The DB snapshot Arn that the DB snapshot was copied from. It only has value in case of cross customer or cross region copy.
        """
        if source_region and not isinstance(source_region, str):
            raise TypeError("Expected argument 'source_region' to be a str")
        __self__.source_region = source_region
        """
        The region that the DB snapshot was created in or copied from.
        """
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        __self__.status = status
        """
        Specifies the status of this DB snapshot.
        """
        if storage_type and not isinstance(storage_type, str):
            raise TypeError("Expected argument 'storage_type' to be a str")
        __self__.storage_type = storage_type
        """
        Specifies the storage type associated with DB snapshot.
        """
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        __self__.vpc_id = vpc_id
        """
        Specifies the ID of the VPC associated with the DB snapshot.
        """


class AwaitableGetSnapshotResult(GetSnapshotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSnapshotResult(
            allocated_storage=self.allocated_storage,
            availability_zone=self.availability_zone,
            db_instance_identifier=self.db_instance_identifier,
            db_snapshot_arn=self.db_snapshot_arn,
            db_snapshot_identifier=self.db_snapshot_identifier,
            encrypted=self.encrypted,
            engine=self.engine,
            engine_version=self.engine_version,
            id=self.id,
            include_public=self.include_public,
            include_shared=self.include_shared,
            iops=self.iops,
            kms_key_id=self.kms_key_id,
            license_model=self.license_model,
            most_recent=self.most_recent,
            option_group_name=self.option_group_name,
            port=self.port,
            snapshot_create_time=self.snapshot_create_time,
            snapshot_type=self.snapshot_type,
            source_db_snapshot_identifier=self.source_db_snapshot_identifier,
            source_region=self.source_region,
            status=self.status,
            storage_type=self.storage_type,
            vpc_id=self.vpc_id)


def get_snapshot(db_instance_identifier=None, db_snapshot_identifier=None, include_public=None, include_shared=None, most_recent=None, snapshot_type=None, opts=None):
    """
    Use this data source to get information about a DB Snapshot for use when provisioning DB instances

    > **NOTE:** This data source does not apply to snapshots created on Aurora DB clusters.
    See the `rds.ClusterSnapshot` data source for DB Cluster snapshots.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    prod = aws.rds.Instance("prod",
        allocated_storage=10,
        engine="mysql",
        engine_version="5.6.17",
        instance_class="db.t2.micro",
        name="mydb",
        username="foo",
        password="bar",
        db_subnet_group_name="my_database_subnet_group",
        parameter_group_name="default.mysql5.6")
    latest_prod_snapshot = prod.id.apply(lambda id: aws.rds.get_snapshot(db_instance_identifier=id,
        most_recent=True))
    # Use the latest production snapshot to create a dev instance.
    dev = aws.rds.Instance("dev",
        instance_class="db.t2.micro",
        name="mydbdev",
        snapshot_identifier=latest_prod_snapshot.id)
    ```


    :param str db_instance_identifier: Returns the list of snapshots created by the specific db_instance
    :param str db_snapshot_identifier: Returns information on a specific snapshot_id.
    :param bool include_public: Set this value to true to include manual DB snapshots that are public and can be
           copied or restored by any AWS account, otherwise set this value to false. The default is `false`.
    :param bool include_shared: Set this value to true to include shared manual DB snapshots from other
           AWS accounts that this AWS account has been given permission to copy or restore, otherwise set this value to false.
           The default is `false`.
    :param bool most_recent: If more than one result is returned, use the most
           recent Snapshot.
    :param str snapshot_type: The type of snapshots to be returned. If you don't specify a SnapshotType
           value, then both automated and manual snapshots are returned. Shared and public DB snapshots are not
           included in the returned results by default. Possible values are, `automated`, `manual`, `shared` and `public`.
    """
    __args__ = dict()
    __args__['dbInstanceIdentifier'] = db_instance_identifier
    __args__['dbSnapshotIdentifier'] = db_snapshot_identifier
    __args__['includePublic'] = include_public
    __args__['includeShared'] = include_shared
    __args__['mostRecent'] = most_recent
    __args__['snapshotType'] = snapshot_type
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:rds/getSnapshot:getSnapshot', __args__, opts=opts).value

    return AwaitableGetSnapshotResult(
        allocated_storage=__ret__.get('allocatedStorage'),
        availability_zone=__ret__.get('availabilityZone'),
        db_instance_identifier=__ret__.get('dbInstanceIdentifier'),
        db_snapshot_arn=__ret__.get('dbSnapshotArn'),
        db_snapshot_identifier=__ret__.get('dbSnapshotIdentifier'),
        encrypted=__ret__.get('encrypted'),
        engine=__ret__.get('engine'),
        engine_version=__ret__.get('engineVersion'),
        id=__ret__.get('id'),
        include_public=__ret__.get('includePublic'),
        include_shared=__ret__.get('includeShared'),
        iops=__ret__.get('iops'),
        kms_key_id=__ret__.get('kmsKeyId'),
        license_model=__ret__.get('licenseModel'),
        most_recent=__ret__.get('mostRecent'),
        option_group_name=__ret__.get('optionGroupName'),
        port=__ret__.get('port'),
        snapshot_create_time=__ret__.get('snapshotCreateTime'),
        snapshot_type=__ret__.get('snapshotType'),
        source_db_snapshot_identifier=__ret__.get('sourceDbSnapshotIdentifier'),
        source_region=__ret__.get('sourceRegion'),
        status=__ret__.get('status'),
        storage_type=__ret__.get('storageType'),
        vpc_id=__ret__.get('vpcId'))
