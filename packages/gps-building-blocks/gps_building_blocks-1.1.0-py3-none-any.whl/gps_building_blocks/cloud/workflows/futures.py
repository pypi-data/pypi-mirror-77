# python3
# coding=utf-8
# Copyright 2020 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Future: the return type for async tasks.
"""

from typing import Any, Dict, Optional


class Result:
  """Wrapper for results of async tasks."""

  def __init__(self, trigger_id: str, is_success: bool,
               result: Optional[Any] = None, error: Optional[Any] = None):
    """Initializes the Result object.

    Args:
      trigger_id: The id associated with the async task. Needs to be unique
        across whole workflow.
      is_success: Is the task successfully finished.
      result: The result of the task.
      error: The error, typically a string message.
    """
    self.trigger_id = trigger_id
    self.is_success = is_success
    self.result = result
    self.error = error


class Future:
  """Return type for async tasks."""
  all_futures = []

  def __init_subclass__(cls, **kwargs):
    """Adds future subclass to the list of all available future classes.

    Args:
      **kwargs: other args
    """
    super().__init_subclass__(**kwargs)
    cls.all_futures.append(cls)

  def __init__(self, trigger_id: str):
    """Initializes the Future object.

    Args:
      trigger_id: The trigger id to be associated with this async task. This id
                  is used to trigger the corresponding function flow task to be
                  marked as finished. For example, in a BigQuery job, the job id
                  can be used as a trigger id.
    """
    self.trigger_id = trigger_id

  @classmethod
  def handle_message(cls, message: Dict[str, Any]) -> Optional[Result]:
    """Handles the external message(event).

      This method needs to be overwritten by subclasses.

    Args:
      message: The message dict to be handled.
    Returns:
      A Result object, if the message can be parsed and handled, or None if the
        message is ignored.
    """
    raise NotImplementedError('Please implement class method handle_message!')


class BigQueryFuture(Future):
  """Return type for async big query task."""

  @classmethod
  def handle_message(cls, message: Dict[str, Any]) -> Optional[Result]:
    """Handles bigquery task finish messages.

      If the message is a bigquery message, then parse it and return its status,
        otherwise just return None.

    Args:
      message: The message JSON dictionary.

    Returns:
      Parsed task result from the message.
    """
    if _get_value(message, 'resource.type') == 'bigquery_resource':
      bq_job_id = _get_value(
          message,
          'protoPayload.serviceData.jobCompletedEvent.job.jobName.jobId')
      code = _get_value(message, 'protoPayload.status.code')

      if code:
        # The current behavior of BQ job status logs is empty status dict when
        # no errors (in this case code will be None), and all error codes are
        # non-zero.
        error = _get_value(message, 'protoPayload.status.message')
        return Result(trigger_id=bq_job_id, is_success=False, error=error)
      else:
        return Result(trigger_id=bq_job_id, is_success=True)


def _get_value(obj: Dict[str, Any], keypath: str):
  """Gets a value from a dictionary using dot-separated keys.

  Args:
    obj: A dictionary, which can be multi-level.
    keypath: Keys separated by dot.

  Returns:
    Value from the dictionary using multiple keys in order, for example
      `_get_value(d, 'a.b.c')` is equivalent to `d['a']['b']['c']`. If the key
      does not exist at any level, return None.
  """
  try:
    for key in keypath.split('.'):
      obj = obj[key]
  except KeyError:
    return None
  return obj
