
from singer import utils
from tap_asana.context import Context
from tap_asana.streams.base import Stream


class Tasks(Stream):
  name = 'tasks'
  replication_key = "modified_at"
  replication_method = 'INCREMENTAL'
  fields = [
    "gid",
    "resource_type",
    "name",
    "approval_status",
    "assignee_status",
    "completed",
    "completed_at",
    "completed_by",
    "created_at",
    "dependencies",
    "dependents",
    "due_at",
    "due_on",
    "external",
    "hearted",
    "hearts",
    "html_notes",
    "is_rendered_as_seperator",
    "liked",
    "likes",
    "memberships",
    "modified_at",
    "notes",
    "num_hearts",
    "num_likes",
    "num_subtasks",
    "resource_subtype",
    "start_on",
    "assignee",
    "custom_fields",
    "followers",
    "parent",
    "permalink_url",
    "projects",
    "tags",
    "workspace"
  ]


  def get_objects(self):
    bookmark = self.get_bookmark()
    session_bookmark = bookmark
    modified_since = bookmark.strftime("%Y-%m-%dT%H:%M:%S.%f")
    opt_fields = ",".join(self.fields)
    for workspace in self.call_api("workspaces"):
      for user in self.call_api("users", workspace=workspace["gid"]):
        for task in self.call_api("tasks", assignee=user["gid"], workspace=workspace['gid'], opt_fields=opt_fields,
                                  modified_since=modified_since):
          session_bookmark = self.get_updated_session_bookmark(session_bookmark, task[self.replication_key])
          if self.is_bookmark_old(task[self.replication_key]):
            yield task
    self.update_bookmark(session_bookmark)


Context.stream_objects['tasks'] = Tasks
