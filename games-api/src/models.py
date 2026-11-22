from pydantic import BaseModel, Field, conint

import json
import os

PASSWORDS = json.loads(os.getenv("PASSWORDS", "{}"))


class WorkloadAnnotations(BaseModel):
    cloudflared_command: str | None = Field(
        default=None, alias="danivy.com/help-cloudflared-command"
    )


class WorkloadMetadata(BaseModel):
    name: str
    annotations: WorkloadAnnotations = Field(
        default_factory=lambda: WorkloadAnnotations()
    )


class WorkloadStatus(BaseModel):
    replicas: int | None
    ready_replicas: int | None


class Deployment(BaseModel):
    """A K8s deployment."""

    metadata: WorkloadMetadata
    status: WorkloadStatus

    def enabled(self) -> bool:
        """If the deployment hasa replica count > 0."""
        return self.status.replicas not in (0, None)

    def healthy(self) -> bool:
        """If the deployment is healthy."""
        return self.status.replicas == self.status.ready_replicas


class Statefulset(BaseModel):
    """A K8s statefulset."""

    metadata: WorkloadMetadata
    status: WorkloadStatus

    def enabled(self) -> bool:
        """If the deployment has a replica count > 0."""
        return self.status.replicas not in (0, None)

    def healthy(self) -> bool:
        """If the deployment is healthy."""
        return self.status.replicas == self.status.ready_replicas


class Game(BaseModel):
    """The status of a game."""

    name: str = Field(..., description="The name of the game")
    enabled: bool = Field(..., description="If the game is enabled")
    healthy: bool = Field(..., description="If the game is healthy")
    start_time: int | None = Field(None, description="When the game started")
    end_time: int | None = Field(None, description="When the game will end")

    # Help
    cloudflared_command: str | None = Field(
        None, description="The command to connect cloudflared to the server"
    )
    password: str | None = Field(None, description="The server password")

    @classmethod
    def from_workload(
        cls, obj: Deployment | Statefulset, start_time: int | None, end_time: int | None
    ) -> Game:
        """Converts a K8s object to a Game."""
        if isinstance(obj, (Deployment, Statefulset)):
            return Game(
                name=obj.metadata.name,
                enabled=obj.enabled(),
                healthy=obj.healthy(),
                start_time=start_time,
                end_time=end_time,
                # Help
                cloudflared_command=obj.metadata.annotations.cloudflared_command,
                password=PASSWORDS.get(obj.metadata.name, None),
            )
        else:
            raise RuntimeError(f"Unexpected type {type(obj)}")


class WakeRequest(BaseModel):
    """A request to wake a game."""

    hours: conint(gt=0, lt=5) = Field(
        ..., description="The number of hours to keep the game awake"
    )
