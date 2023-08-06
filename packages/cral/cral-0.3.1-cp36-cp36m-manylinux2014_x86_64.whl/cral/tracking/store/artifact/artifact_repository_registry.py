import entrypoints
import warnings

from cral.tracking.exceptions import MlflowException
from cral.tracking.store.artifact.azure_blob_artifact_repo import AzureBlobArtifactRepository
from cral.tracking.store.artifact.dbfs_artifact_repo import dbfs_artifact_repo_factory
from cral.tracking.store.artifact.ftp_artifact_repo import FTPArtifactRepository
from cral.tracking.store.artifact.gcs_artifact_repo import GCSArtifactRepository
from cral.tracking.store.artifact.hdfs_artifact_repo import HdfsArtifactRepository
from cral.tracking.store.artifact.local_artifact_repo import LocalArtifactRepository
from cral.tracking.store.artifact.models_artifact_repo import ModelsArtifactRepository
from cral.tracking.store.artifact.runs_artifact_repo import RunsArtifactRepository
from cral.tracking.store.artifact.s3_artifact_repo import S3ArtifactRepository
from cral.tracking.store.artifact.sftp_artifact_repo import SFTPArtifactRepository

from cral.tracking.utils.uri import get_uri_scheme


class ArtifactRepositoryRegistry:
    """Scheme-based registry for artifact repository implementations

    This class allows the registration of a function or class to provide an implementation for a
    given scheme of `artifact_uri` through the `register` method. Implementations declared though
    the entrypoints `cral.tracking.artifact_repository` group can be automatically registered through the
    `register_entrypoints` method.

    When instantiating an artifact repository through the `get_artifact_repository` method, the
    scheme of the artifact URI provided will be used to select which implementation to instantiate,
    which will be called with same arguments passed to the `get_artifact_repository` method.
    """

    def __init__(self):
        self._registry = {}

    def register(self, scheme, repository):
        """Register artifact repositories provided by other packages"""
        self._registry[scheme] = repository

    def register_entrypoints(self):
        # Register artifact repositories provided by other packages
        for entrypoint in entrypoints.get_group_all("cral.tracking.artifact_repository"):
            try:
                self.register(entrypoint.name, entrypoint.load())
            except (AttributeError, ImportError) as exc:
                warnings.warn(
                    'Failure attempting to register artifact repository for scheme "{}": {}'.format(
                        entrypoint.name, str(exc)
                    ),
                    stacklevel=2
                )

    def get_artifact_repository(self, artifact_uri):
        """Get an artifact repository from the registry based on the scheme of artifact_uri

        :param store_uri: The store URI. This URI is used to select which artifact repository
                          implementation to instantiate and is passed to the
                          constructor of the implementation.

        :return: An instance of `cral.tracking.store.ArtifactRepository` that fulfills the artifact URI
                 requirements.
        """
        scheme = get_uri_scheme(artifact_uri)
        repository = self._registry.get(scheme)
        if repository is None:
            raise MlflowException(
                "Could not find a registered artifact repository for: {}. "
                "Currently registered schemes are: {}".format(
                    artifact_uri, list(self._registry.keys())
                )
            )
        return repository(artifact_uri)


_artifact_repository_registry = ArtifactRepositoryRegistry()

_artifact_repository_registry.register('', LocalArtifactRepository)
_artifact_repository_registry.register('file', LocalArtifactRepository)
_artifact_repository_registry.register('s3', S3ArtifactRepository)
_artifact_repository_registry.register('gs', GCSArtifactRepository)
_artifact_repository_registry.register('wasbs', AzureBlobArtifactRepository)
_artifact_repository_registry.register('ftp', FTPArtifactRepository)
_artifact_repository_registry.register('sftp', SFTPArtifactRepository)
_artifact_repository_registry.register('dbfs', dbfs_artifact_repo_factory)
_artifact_repository_registry.register('hdfs', HdfsArtifactRepository)
_artifact_repository_registry.register('viewfs', HdfsArtifactRepository)
_artifact_repository_registry.register('runs', RunsArtifactRepository)
_artifact_repository_registry.register('models', ModelsArtifactRepository)

_artifact_repository_registry.register_entrypoints()


def get_artifact_repository(artifact_uri):
    """Get an artifact repository from the registry based on the scheme of artifact_uri

    :param store_uri: The store URI. This URI is used to select which artifact repository
                      implementation to instantiate and is passed to the
                      constructor of the implementation.

    :return: An instance of `cral.tracking.store.ArtifactRepository` that fulfills the artifact URI
             requirements.
    """
    return _artifact_repository_registry.get_artifact_repository(artifact_uri)
