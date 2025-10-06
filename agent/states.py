from pydantic import BaseModel, ConfigDict, Field


class File(BaseModel):
    path: str = Field(description="The path to the file to be created or modified")
    purpose: str = Field(
        description="The purpose of the file , e.g. : 'main application logic' 'data processing module', etc. "
    )


class Plan(BaseModel):
    name: str = Field(description="The name of the app built")
    description: str = Field(
        description="A oneline description of the app built e.g : A web application for managing personal techstack "
    )

    techstack: str = Field(
        description="The tech stack to be used for the app, e.g. : 'Python', 'javascript', 'react', 'flask' , etc  "
    )

    features: list[str] = Field(
        description="A list of features that the app should have, e.g. : 'user authentication', 'data visualisation'"
    )

    files: list[File]


class ImplementationTask(BaseModel):
    filepath: str = Field(description="The path to the file to be modified")
    task_description: str = Field(
        description="A detailed description of the task to be performed"
    )


class TaskPlan(BaseModel):
    implementation_steps: list[ImplementationTask] = Field(
        description="A list of steps to be taken to implement the required task."
    )
    model_config = ConfigDict(extra="allow")  #
