# -*- coding: utf-8 -*-
from workflow.steps.util.database import DatabaseStep
from workflow.steps.util import test_bash_script_error
from workflow.steps.mongodb.util import build_create_data_dir_script
from workflow.steps.mongodb.util import build_add_read_only_replica_set_member_script
from workflow.steps.mongodb.util import build_remove_read_only_replica_set_member_script


class AddInstanceToReplicaSet(DatabaseStep):

    def __unicode__(self):
        return "Adding instance to Replica Set..."

    @property
    def script_variables(self):
        variables = {
            'CONNECT_ADMIN_URI': self.driver.get_admin_connection(),
            'HOSTADDRESS': self.instance.address,
            'PORT': self.instance.port,
        }
        return variables

    def do(self):

        script = test_bash_script_error()
        script += build_add_read_only_replica_set_member_script()
        self._execute_script(self.script_variables, script)

    def undo(self):
        script = test_bash_script_error()
        script += build_remove_read_only_replica_set_member_script()
        self._execute_script(self.script_variables, script)


class CreateDataDir(DatabaseStep):

    def __unicode__(self):
        return "Creating data dir..."

    @property
    def script_variables(self):
        return {}

    def do(self):

        script = test_bash_script_error()
        script += build_create_data_dir_script()
        self._execute_script(self.script_variables, script)
