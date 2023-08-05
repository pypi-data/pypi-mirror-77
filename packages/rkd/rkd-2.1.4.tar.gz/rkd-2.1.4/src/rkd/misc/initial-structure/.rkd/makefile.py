
import os
from rkd.api.syntax import TaskAliasDeclaration as Task
from rkd.api.syntax import TaskDeclaration
from rkd.api.contract import ExecutionContext
from rkd.standardlib import CallableTask


# def create_union_task_as_method(context: ExecutionContext) -> bool:
#     os.system('xdg-open https://iwa-ait.org')
#     return True


IMPORTS = []
TASKS = []

#
# # optionally, add a custom task written in pure Python
# IMPORTS += [TaskDeclaration(CallableTask(':create-union', create_union_task_as_method))]
#
# # optionally, create own tasks that are using other tasks
# TASKS = [
#     Task(':hello-world', [':sh', '-c', '''
#         set -x
#         MSG="Hello world"
#
#         echo "${MSG}"
#     '''])
# ]
