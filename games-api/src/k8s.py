import kubernetes
import logging
import os

from typing import List
from kubernetes.client import V1Scale, V1ScaleSpec
from kubernetes.client.models.v1_deployment import V1Deployment
from .models import Deployment

NAMESPACE = os.environ["K8S_NAMESPACE"]

_logger = logging.getLogger(__name__)

# Load clients
try:
    kubernetes.config.load_incluster_config()
except:
    kubernetes.config.load_kube_config()

core_v1 = kubernetes.client.CoreV1Api()
apps_v1 = kubernetes.client.AppsV1Api()


async def list_deployments() -> List[Deployment]:
    """Lists every deployment in the namespace."""
    deployments = []
    # type: ignore
    for deployment in await _get_deployments():
        deployments.append(Deployment(**deployment.to_dict()))
    return deployments


async def scale_deployment(name: str, replicas: int) -> bool:
    """Resizes a deployment to the expected replica count.
    Returns true if the deployment was scaled."""
    _logger.info(f"Scaling {name} deployment to {replicas} replicas...")
    deployment = apps_v1.read_namespaced_deployment(namespace=NAMESPACE, name=name)  # type: ignore
    deployment = Deployment(**deployment.to_dict())  # type: ignore

    # Exit early if already scaled
    if deployment.status.replicas == replicas:
        _logger.info(f"Skipping {name} deployment because it's already scaled.")
        return False

    scale = V1Scale(
        api_version="apps/v1",
        kind="Scale",
        spec=V1ScaleSpec(replicas=replicas),
    )

    apps_v1.patch_namespaced_deployment_scale(
        namespace=NAMESPACE,
        name=name,
        body=scale,
    )
    _logger.info(f"{name} deployment scaled.")
    return True


async def _get_deployments() -> List[V1Deployment]:
    """Returns the deployments in the namespace."""
    return apps_v1.list_namespaced_deployment(namespace=NAMESPACE).items  # type: ignore
