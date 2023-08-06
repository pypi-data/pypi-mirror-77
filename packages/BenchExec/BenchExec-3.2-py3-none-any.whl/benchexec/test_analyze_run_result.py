# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import sys
import unittest
import types

from benchexec.util import ProcessExitCode
from benchexec.model import Run
from benchexec.result import (
    RESULT_FALSE_REACH,
    RESULT_ERROR,
    RESULT_UNKNOWN,
    RESULT_TRUE_PROP,
)
from benchexec.tools.template import BaseTool

sys.dont_write_bytecode = True  # prevent creation of .pyc files

normal_result = ProcessExitCode(raw=0, value=0, signal=None)


class TestResult(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        logging.disable(logging.CRITICAL)

    def create_run(self, info_result=RESULT_UNKNOWN):
        runSet = types.SimpleNamespace()
        runSet.log_folder = "."
        runSet.result_files_folder = "."
        runSet.options = []
        runSet.real_name = None
        runSet.propertytag = None
        runSet.benchmark = lambda: None
        runSet.benchmark.base_dir = "."
        runSet.benchmark.benchmark_file = "Test.xml"
        runSet.benchmark.columns = []
        runSet.benchmark.name = "Test"
        runSet.benchmark.instance = "Test"
        runSet.benchmark.rlimits = {}
        runSet.benchmark.tool = BaseTool()

        def determine_result(self, returncode, returnsignal, output, isTimeout=False):
            return info_result

        runSet.benchmark.tool.determine_result = determine_result

        return Run(
            identifier="test.c", sourcefiles=["test.c"], fileOptions=[], runSet=runSet
        )

    def test_simple(self):
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(
            RESULT_UNKNOWN, run._analyze_result(normal_result, "", False, None)
        )

        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(
            RESULT_TRUE_PROP, run._analyze_result(normal_result, "", False, None)
        )

        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(
            RESULT_FALSE_REACH, run._analyze_result(normal_result, "", False, None)
        )

    def test_timeout(self):
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual("TIMEOUT", run._analyze_result(normal_result, "", True, None))

        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(
            "TIMEOUT (" + RESULT_TRUE_PROP + ")",
            run._analyze_result(normal_result, "", True, None),
        )

        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(
            "TIMEOUT (" + RESULT_FALSE_REACH + ")",
            run._analyze_result(normal_result, "", True, None),
        )

        run = self.create_run(info_result="SOME OTHER RESULT")
        self.assertEqual(
            "TIMEOUT (SOME OTHER RESULT)",
            run._analyze_result(normal_result, "", True, None),
        )

        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual("TIMEOUT", run._analyze_result(normal_result, "", True, None))

    def test_out_of_memory(self):
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(
            "OUT OF MEMORY", run._analyze_result(normal_result, "", False, "memory")
        )

        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(
            "OUT OF MEMORY (" + RESULT_TRUE_PROP + ")",
            run._analyze_result(normal_result, "", False, "memory"),
        )

        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(
            "OUT OF MEMORY (" + RESULT_FALSE_REACH + ")",
            run._analyze_result(normal_result, "", False, "memory"),
        )

        run = self.create_run(info_result="SOME OTHER RESULT")
        self.assertEqual(
            "OUT OF MEMORY (SOME OTHER RESULT)",
            run._analyze_result(normal_result, "", False, "memory"),
        )

        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual(
            "OUT OF MEMORY", run._analyze_result(normal_result, "", False, "memory")
        )

    def test_timeout_and_out_of_memory(self):
        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(
            "TIMEOUT", run._analyze_result(normal_result, "", True, "memory")
        )

        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(
            "TIMEOUT (" + RESULT_TRUE_PROP + ")",
            run._analyze_result(normal_result, "", True, "memory"),
        )

        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(
            "TIMEOUT (" + RESULT_FALSE_REACH + ")",
            run._analyze_result(normal_result, "", True, "memory"),
        )

        run = self.create_run(info_result="SOME OTHER RESULT")
        self.assertEqual(
            "TIMEOUT (SOME OTHER RESULT)",
            run._analyze_result(normal_result, "", True, "memory"),
        )

        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual(
            "TIMEOUT", run._analyze_result(normal_result, "", True, "memory")
        )

    def test_returnsignal(self):
        def signal(sig):
            """Encode a signal as it would be returned by os.wait"""
            return ProcessExitCode(raw=sig, value=None, signal=sig)

        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual("TIMEOUT", run._analyze_result(signal(9), "", True, None))

        run = self.create_run(info_result=RESULT_ERROR)
        self.assertEqual(
            "OUT OF MEMORY", run._analyze_result(signal(9), "", False, "memory")
        )

        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(
            RESULT_TRUE_PROP, run._analyze_result(signal(9), "", False, None)
        )

        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(
            RESULT_FALSE_REACH, run._analyze_result(signal(9), "", False, None)
        )

        run = self.create_run(info_result="SOME OTHER RESULT")
        self.assertEqual(
            "SOME OTHER RESULT", run._analyze_result(signal(9), "", False, None)
        )

        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(
            "KILLED BY SIGNAL 9", run._analyze_result(signal(9), "", False, None)
        )

    def test_exitcode(self):
        def returnvalue(value):
            """Encode an exit of aprogram as it would be returned by os.wait"""
            return ProcessExitCode(raw=value << 8, value=value, signal=None)

        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual("TIMEOUT", run._analyze_result(returnvalue(1), "", True, None))

        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(
            "OUT OF MEMORY", run._analyze_result(returnvalue(1), "", False, "memory"),
        )

        run = self.create_run(info_result=RESULT_TRUE_PROP)
        self.assertEqual(
            RESULT_TRUE_PROP, run._analyze_result(returnvalue(1), "", False, None)
        )

        run = self.create_run(info_result=RESULT_FALSE_REACH)
        self.assertEqual(
            RESULT_FALSE_REACH, run._analyze_result(returnvalue(1), "", False, None)
        )

        run = self.create_run(info_result="SOME OTHER RESULT")
        self.assertEqual(
            "SOME OTHER RESULT", run._analyze_result(returnvalue(1), "", False, None)
        )

        run = self.create_run(info_result=RESULT_UNKNOWN)
        self.assertEqual(
            RESULT_UNKNOWN, run._analyze_result(returnvalue(1), "", False, None)
        )
