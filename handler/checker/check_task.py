#!/usr/bin/env python
# -*- coding: UTF-8 -*
# Copyright (c) 2022 OceanBase
# OceanBase Diagnostic Tool is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

"""
@time: 2023/9/26
@file: check_task.py
@desc:
"""

from common.logger import logger
from handler.checker.check_exception import StepResultFailException, \
    StepExecuteFailException, StepResultFalseException, TaskException
from handler.checker.step.stepbase import StepBase
from utils.utils import node_cut_passwd_for_log
from utils.version_utils import compare_versions_greater


class TaskBase(object):
    def __init__(self, task, nodes, cluster, report, task_variable_dict=None):
        if task_variable_dict is None:
            self.task_variable_dict = {}
        else:
            self.task_variable_dict = task_variable_dict
        self.task = task
        self.cluster = cluster
        self.nodes = nodes
        self.report = report

    def execute(self):
        logger.info("task_base execute")
        steps_nu = self.filter_by_version()
        if steps_nu < 0:
            logger.warning("Unadapted by version. SKIP")
            self.report.add("Unadapted by version. SKIP", "warning")
            return "Unadapted by version.SKIP"
        logger.info("filter_by_version is return {0}".format(steps_nu))
        if len(self.nodes)==0:
            raise Exception("node is not exist")
        for node in self.nodes:
            logger.info("run task in node: {0}".format(node_cut_passwd_for_log(node)))
            steps = self.task[steps_nu]
            nu = 1
            for step in steps["steps"]:
                try:
                    logger.debug("step nu: {0}".format(nu))
                    if len(self.cluster)==0:
                        raise Exception("cluster is not exist")
                    step_run = StepBase(step, node, self.cluster, self.task_variable_dict)
                    logger.info("step nu: {0} initted, to execute".format(nu))
                    step_run.execute(self.report)
                    self.task_variable_dict = step_run.update_task_variable_dict()
                    if "report_type" in step["result"] and step["result"]["report_type"] == "execution":
                        logger.info("report_type stop this step")
                        return
                except StepExecuteFailException as e:
                    logger.error("TaskBase execute CheckStepFailException: {0} . Do Next Task".format(e))
                    return
                except StepResultFalseException as e:
                    logger.warning("TaskBase execute StepResultFalseException: {0} .".format(e))
                    continue
                except StepResultFailException as e:
                    logger.error("TaskBase execute StepResultFailException: {0}".format(e))
                    return
                except Exception as e:
                    logger.error("TaskBase execute Exception: {0}".format(e))
                    raise TaskException("TaskBase execute Exception:  {0}".format(e))

                logger.info("step nu: {0} execute end ".format(nu))
                nu = nu + 1
        logger.info("task execute end")

    def filter_by_version(self):
        try:
            steps = self.task
            steps_nu = 0
            # get observer version
            if "version" not in self.cluster or self.cluster["version"] == "":
                return steps_nu
            for now_steps in steps:
                # have version in task ?
                if "version" in now_steps:
                    steps_versions = now_steps["version"]
                    if not isinstance(steps_versions, str):
                        raise TaskException("filter_by_version steps_version Exception : {0}".format("the type of version is not string"))
                    version_real = self.cluster["version"]
                    logger.info("version_int is {0} steps_versions is {1}".format(version_real, steps_versions))

                    steps_versions = steps_versions.replace(" ", "")
                    steps_versions = steps_versions[1:-1]
                    steps_versions_list = steps_versions.split(",")
                    minVersion = steps_versions_list[0]
                    maxVersion = steps_versions_list[1]
                    # min
                    if minVersion == "*":
                        minVersion = "-1"
                    if maxVersion == "*":
                        maxVersion = "999"
                    if compare_versions_greater(version_real, minVersion) and compare_versions_greater(maxVersion,
                                                                                                         version_real):
                        break
                else:
                    logger.info("not version in now_steps")
                    break
                steps_nu = steps_nu + 1
            if steps_nu > len(steps) - 1:
                logger.warning("not version in this task")
                return -1
            return steps_nu
        except Exception as e:
            logger.error("filter_by_version Exception : {0}".format(e))
            raise TaskException("filter_by_version Exception : {0}".format(e))
