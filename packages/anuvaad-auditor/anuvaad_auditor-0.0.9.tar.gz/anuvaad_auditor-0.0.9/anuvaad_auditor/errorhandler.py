import logging
import time
import uuid

from .kfproducer import push_to_queue
from .eswrapper import index_error_to_es
from .loghandler import log_info
from .loghandler import log_exception
from .config import anu_etl_wf_error_topic

log = logging.getLogger('file')


# Method to standardize and index errors for the core flow
# code: Any string that uniquely identifies an error
# message: The error message
# cause: JSON or String that explains the cause of the error
def post_error(code, message, cause):
    try:
        error = {
            "errorID": generate_error_id(),
            "code": code,
            "message": message,
            "timeStamp": eval(str(time.time()).replace('.', '')),
            "errorType": "core-error"
        }
        if cause is not None:
            error["cause"] = cause
        index_error_to_es(error)
        log_info("Error posted to the es index.", None)
        return error
    except Exception as e:
        log_exception("Error Handler Failed.", None, e)
        return None


# Method to standardize, post and index errors for the workflow.
# code: Any string that uniquely identifies an error
# message: The error message
# cause: JSON or String that explains the cause of the error
# jobID: Unique JOB ID generated for the wf.
# taskID: Unique TASK ID generated for the current task.
# state: State of the workflow pertaining to the current task.
# status: Status of the workflow pertaining to the current task.
def post_error_wf(code, message, entity, cause):
    try:
        error = {
            "errorID": generate_error_id(),
            "code": code,
            "message": message,
            "timeStamp": eval(str(time.time()).replace('.', '')),
            "jobID": entity["jobID"],
            "taskID": entity["taskID"],
            "state": entity["state"],
            "status": "FAILED",
            "errorType": "wf-error"
        }
        if cause is not None:
            error["cause"] = cause
        if entity["status"]:
            error["status"] = entity["status"]
        if entity["metadata"] is not None:
            error["metadata"] = entity["metadata"]

        push_to_queue(error, anu_etl_wf_error_topic)
        log_info("Error pushed to the wf error topic.", None)
        index_error_to_es(error)
        log_info("Error posted to the es index.", None)
        return error
    except Exception as e:
        log_exception("Error Handler WF Failed.", None, e)
        return None


# Method to generate error ID.
def generate_error_id():
    return str(uuid.uuid4())
