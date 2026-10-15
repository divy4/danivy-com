from pydantic import BaseModel, Field


class DeploymentMetadata(BaseModel):
    name: str


class DeploymentStatus(BaseModel):
    replicas: int | None
    ready_replicas: int | None


class Deployment(BaseModel):
    """A K8s deployment."""

    metadata: DeploymentMetadata
    status: DeploymentStatus

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
    start_time: int | None = Field(None, description="When the game started.")
    end_time: int | None = Field(None, description="When the game will end.")

    @classmethod
    def from_deployment(
        cls, deployment: Deployment, start_time: int | None, end_time: int | None
    ) -> Game:
        """Converts a Deployment to a Game."""
        return Game(
            name=deployment.metadata.name,
            enabled=deployment.enabled(),
            healthy=deployment.healthy(),
            start_time=start_time,
            end_time=end_time,
        )
