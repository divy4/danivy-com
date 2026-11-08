import kubernetes
import logging
import os

from typing import List
from kubernetes.client import V1Scale, V1ScaleSpec
from kubernetes.client.models.v1_deployment import V1Deployment
from kubernetes.client.models.v1_stateful_set import V1StatefulSet
from .models import Deployment, Statefulset

NAMESPACE = os.environ["K8S_NAMESPACE"]

_logger = logging.getLogger(__name__)

# Load clients
try:
    kubernetes.config.load_incluster_config()
except:
    kubernetes.config.load_kube_config()

core_v1 = kubernetes.client.CoreV1Api()
apps_v1 = kubernetes.client.AppsV1Api()


async def list_workloads() -> List[Deployment | Statefulset]:
    """Lists Deployments and StatefulSets in the namespace."""
    names = set()
    objects = []
    for obj_list in (list_deployments(), list_statefulsets()):
        for obj in await obj_list:
            if obj.metadata.name in names:
                raise RuntimeError(f"Duplicate objects detected under name {obj.metadata.name}")
            names.add(obj.metadata.name)
            objects.append(obj)
    return objects


async def list_deployments() -> List[Deployment]:
    """Lists every deployment in the namespace."""
    deployments = []
    # type: ignore
    for deployment in await _get_deployments():
        deployments.append(Deployment(**deployment.to_dict()))
    return deployments


async def list_statefulsets() -> List[Statefulset]:
    """Lists every statefulsets in the namespace."""
    statefulsets = []
    # type: ignore
    for statefulset in await _get_statefulsets():
        statefulsets.append(Statefulset(**statefulset.to_dict()))
    return statefulsets


async def scale_workload(workload: Deployment | Statefulset, replicas: int) -> bool:
    """Resizes a deployment to the expected replica count.
    Returns true if the deployment was scaled."""
    name = workload.metadata.name
    workload_type = type(workload).__name__
    _logger.info(f"Scaling {name} {workload_type} to {replicas} replicas...")

    # Exit early if already scaled
    if workload.status.replicas == replicas:
        _logger.info(f"Skipping {name} {workload_type} because it's already scaled.")
        return False

    scale = V1Scale(
        api_version="apps/v1",
        kind="Scale",
        spec=V1ScaleSpec(replicas=replicas),
    )

    if isinstance(workload, Deployment):
        scale_function = apps_v1.patch_namespaced_deployment_scale
    elif isinstance(workload, Statefulset):
        scale_function = apps_v1.patch_namespaced_stateful_set

    scale_function(
        namespace=NAMESPACE,
        name=name,
        body=scale,
    )

    _logger.info(f"{name} {workload_type} scaled.")
    return True


async def _get_deployments() -> List[V1Deployment]:
    """Returns the deployments in the namespace."""
    return apps_v1.list_namespaced_deployment(namespace=NAMESPACE).items  # type: ignore

async def _get_statefulsets() -> List[V1StatefulSet]:
    """Returns the deployments in the namespace."""
    return apps_v1.list_namespaced_stateful_set(namespace=NAMESPACE).items  # type: ignore
