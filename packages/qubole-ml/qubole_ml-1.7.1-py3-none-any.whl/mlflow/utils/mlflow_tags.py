"""
File containing all of the run tags in the mlflow. namespace.

See the REST API documentation for information on the meaning of these tags.
"""

MLFLOW_RUN_NAME = "mlflow.runName"
MLFLOW_PARENT_RUN_ID = "mlflow.parentRunId"
MLFLOW_USER = "mlflow.user"
MLFLOW_SOURCE_TYPE = "mlflow.source.type"
MLFLOW_SOURCE_NAME = "mlflow.source.name"
MLFLOW_GIT_COMMIT = "mlflow.source.git.commit"
MLFLOW_GIT_BRANCH = "mlflow.source.git.branch"
MLFLOW_GIT_REPO_URL = "mlflow.source.git.repoURL"
MLFLOW_LOGGED_MODELS = "mlflow.log-model.history"
MLFLOW_PROJECT_ENV = "mlflow.project.env"
MLFLOW_PROJECT_ENTRY_POINT = "mlflow.project.entryPoint"
MLFLOW_DOCKER_IMAGE_URI = "mlflow.docker.image.uri"
MLFLOW_DOCKER_IMAGE_ID = "mlflow.docker.image.id"

MLFLOW_DATABRICKS_NOTEBOOK_ID = "mlflow.databricks.notebookID"
MLFLOW_DATABRICKS_NOTEBOOK_PATH = "mlflow.databricks.notebookPath"
MLFLOW_DATABRICKS_WEBAPP_URL = "mlflow.databricks.webappURL"
MLFLOW_DATABRICKS_RUN_URL = "mlflow.databricks.runURL"
# The SHELL_JOB_ID and SHELL_JOB_RUN_ID tags are used for tracking the
# Databricks Job ID and Databricks Job Run ID associated with an MLflow Project run
MLFLOW_DATABRICKS_SHELL_JOB_ID = "mlflow.databricks.shellJobID"
MLFLOW_DATABRICKS_SHELL_JOB_RUN_ID = "mlflow.databricks.shellJobRunID"
# The JOB_ID, JOB_RUN_ID, and JOB_TYPE tags are used for automatically recording Job information
# when MLflow Tracking APIs are used within a Databricks Job
MLFLOW_DATABRICKS_JOB_ID = "mlflow.databricks.jobID"
MLFLOW_DATABRICKS_JOB_RUN_ID = "mlflow.databricks.jobRunID"
MLFLOW_DATABRICKS_JOB_TYPE = "mlflow.databricks.jobType"


MLFLOW_PROJECT_BACKEND = "mlflow.project.backend"

MLFLOW_QUBOLE_COMMAND_URI = "mlflow.qubole.commandURI"
MLFLOW_QUBOLE_COMMAND_ID = "mlflow.qubole.commandID"

# All the qubole injected tags which are available in jupyter notebook context
MLFLOW_QUBOLE_NOTEBOOK_PATH = "mlflow.qubole.notebookPath"
MLFLOW_QUBOLE_NOTEBOOK_ID = "mlflow.qubole.notebook.id"
MLFLOW_QUBOLE_SNAPSHOT_PATH = "mlflow.qubole.snapshotPath"
MLFLOW_QUBOLE_JUPYTER_SNAPSHOT_PATH = "mlflow.qubole.jupyterSnapshotPath"
MLFLOW_QUBOLE_NOTEBOOK_NAME = "mlflow.qubole.notebookName"
MLFLOW_QUBOLE_USER_EMAIL = "mlflow.qubole.userEmail"
MLFLOW_QUBOLE_IS_SCHEDULED = "mlflow.qubole.isScheduled"
MLFLOW_QUBOLE_CLUSTER_ID = "mlflow.qubole.clusterId"
MLFLOW_QUBOLE_CLUSTER_INST_ID = "mlflow.qubole.clusterInstId"
MLFLOW_QUBOLE_SPARK_VERSION = "mlflow.qubole.sparkVersion"
MLFLOW_QUBOLE_RUNTIME_ID = "mlflow.qubole.runtimeId"
MLFLOW_QUBOLE_QUBOLED_ENV_ID = "mlflow.qubole.quboledEnvId"
MLFLOW_QUBOLE_SPARK_APPLICATION_ID = "mlflow.qubole.sparkApplicationId"

# The following legacy tags are deprecated and will be removed by MLflow 1.0.
LEGACY_MLFLOW_GIT_BRANCH_NAME = "mlflow.gitBranchName"  # Replaced with mlflow.source.git.branch
LEGACY_MLFLOW_GIT_REPO_URL = "mlflow.gitRepoURL"  # Replaced with mlflow.source.git.repoURL
