# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import sys
import os
import re

import benchexec.result as result
import benchexec.util as util
import benchexec.tools.template
from benchexec.model import SOFTTIMELIMIT


class Tool(benchexec.tools.template.BaseTool):
    """
    Tool info for CPAchecker, the Configurable Software-Verification Platform.
    URL: https://cpachecker.sosy-lab.org/

    Both binary and source distributions of CPAchecker are supported.
    If the source of CPAchecker is present,
    it is automatically compiled before benchmarks are executed.
    Additional statistics can be extracted from the output of CPAchecker
    and added to the result tables.
    For this reason, the parameter -stats is always added to the command line.
    Furthermore, if a soft time limit is specified for BenchExec,
    it is passed to CPAchecker using the parameter -timelimit.
    This allows for proper termination of CPAchecker and statistics output
    even in cases of a timeout.
    """

    REQUIRED_PATHS = [
        "lib/java/runtime",
        "lib/*.jar",
        "lib/native/x86_64-linux",
        "scripts",
        "cpachecker.jar",
        "config",
    ]

    def executable(self):
        executable = util.find_executable("cpa.sh", "scripts/cpa.sh")
        base_dir = os.path.join(os.path.dirname(executable), os.path.pardir)
        jar_file = os.path.join(base_dir, "cpachecker.jar")
        bin_dir = os.path.join(base_dir, "bin")
        src_dir = os.path.join(base_dir, "src")

        # If this is a source checkout of CPAchecker, we heuristically check that
        # sources are not newer than binaries (cpachecker.jar or files in bin/).
        if os.path.isdir(src_dir):
            src_mtime = self._find_newest_mtime(src_dir)

            if os.path.isfile(jar_file):
                if src_mtime > os.stat(jar_file).st_mtime:
                    sys.exit("CPAchecker JAR is not uptodate, run 'ant jar'!")

            elif os.path.isdir(bin_dir):
                if src_mtime > self._find_newest_mtime(bin_dir):
                    sys.exit("CPAchecker build is not uptodate, run 'ant'!")

        return executable

    def _find_newest_mtime(self, path):
        mtime = 0
        for _root, _dirs, files, rootfd in os.fwalk(path):
            for f in files:
                mtime = max(mtime, os.stat(f, dir_fd=rootfd).st_mtime)

        return mtime

    def program_files(self, executable):
        return self._program_files_from_executable(
            executable, self.REQUIRED_PATHS, parent_dir=True
        )

    def version(self, executable):
        version = self._version_from_tool(executable, "-help", line_prefix="CPAchecker")
        return version.split("(")[0].strip()

    def name(self):
        return "CPAchecker"

    def _get_additional_options(self, existing_options, propertyfile, rlimits):
        options = []
        if SOFTTIMELIMIT in rlimits:
            if "-timelimit" not in existing_options:
                options = options + [
                    "-timelimit",
                    str(rlimits[SOFTTIMELIMIT]) + "s",
                ]  # benchmark-xml uses seconds as unit

        if "-stats" not in existing_options:
            options = options + ["-stats"]

        spec = ["-spec", propertyfile] if propertyfile is not None else []

        return options + spec

    def cmdline(self, executable, options, tasks, propertyfile=None, rlimits={}):
        additional_options = self._get_additional_options(
            options, propertyfile, rlimits
        )
        return [executable] + options + additional_options + tasks

    def determine_result(self, returncode, returnsignal, output, isTimeout):
        """
        @param returncode: code returned by CPAchecker
        @param returnsignal: signal, which terminated CPAchecker
        @param output: the output of CPAchecker
        @return: status of CPAchecker after executing a run
        """

        def isOutOfNativeMemory(line):
            return (
                "std::bad_alloc" in line  # C++ out of memory exception (MathSAT)
                or "Cannot allocate memory" in line
                or "Native memory allocation (malloc) failed to allocate" in line  # JNI
                or line.startswith("out of memory")  # CuDD
            )

        status = None

        for line in output:
            line = line.strip()
            if "java.lang.OutOfMemoryError" in line:
                status = "OUT OF JAVA MEMORY"
            elif isOutOfNativeMemory(line):
                status = "OUT OF NATIVE MEMORY"
            elif (
                "There is insufficient memory for the Java Runtime Environment to continue."
                in line
                or "cannot allocate memory for thread-local data: ABORT" in line
            ):
                status = "OUT OF MEMORY"
            elif "SIGSEGV" in line:
                status = "SEGMENTATION FAULT"
            elif "java.lang.AssertionError" in line:
                status = "ASSERTION"
            elif (
                ("Exception:" in line or line.startswith("Exception in thread"))
                # ignore "cbmc error output: ... Minisat::OutOfMemoryException"
                and not line.startswith("cbmc")
            ):
                status = "EXCEPTION"
            elif "Could not reserve enough space for object heap" in line:
                status = "JAVA HEAP ERROR"
            elif line.startswith("Error: ") and not status:
                status = result.RESULT_ERROR
                if "Cannot parse witness" in line:
                    status += " (invalid witness file)"
                elif "Unsupported" in line:
                    if "recursion" in line:
                        status += " (recursion)"
                    elif "threads" in line:
                        status += " (threads)"
                elif "Parsing failed" in line:
                    status += " (parsing failed)"
                elif "Interpolation failed" in line:
                    status += " (interpolation failed)"
            elif line.startswith("Invalid configuration: ") and not status:
                if "Cannot parse witness" in line:
                    status = result.RESULT_ERROR
                    status += " (invalid witness file)"
            elif (
                line.startswith(
                    "For your information: CPAchecker is currently hanging at"
                )
                and not status
                and isTimeout
            ):
                status = "TIMEOUT"

            elif line.startswith("Verification result: "):
                line = line[21:].strip()
                if line.startswith("TRUE"):
                    newStatus = result.RESULT_TRUE_PROP
                elif line.startswith("FALSE"):
                    newStatus = result.RESULT_FALSE_PROP
                    match = re.match(
                        r".* Property violation \(([a-zA-Z0-9_-]+)(:.*)?\) found by chosen configuration.*",
                        line,
                    )
                    if match:
                        newStatus += "(" + match.group(1) + ")"
                else:
                    newStatus = result.RESULT_UNKNOWN

                if not status:
                    status = newStatus
                elif newStatus != result.RESULT_UNKNOWN and status != newStatus:
                    status = "{0} ({1})".format(status, newStatus)
            elif line == "Finished." and not status:
                status = result.RESULT_DONE

        if (
            (not status or status == result.RESULT_UNKNOWN)
            and isTimeout
            and returncode in [15, 143]
        ):
            # The JVM sets such an returncode if it receives signal 15 (143 is 15+128)
            status = "TIMEOUT"

        if not status:
            status = result.RESULT_ERROR
        return status

    def get_value_from_output(self, lines, identifier):
        # search for the text in output and get its value,
        # search the first line, that starts with the searched text
        # warn if there are more lines (multiple statistics from sequential analysis?)
        match = None
        for line in lines:
            if line.lstrip().startswith(identifier):
                startPosition = line.find(":") + 1
                endPosition = line.find("(", startPosition)
                if endPosition == -1:
                    endPosition = len(line)
                if match is None:
                    match = line[startPosition:endPosition].strip()
                else:
                    logging.warning(
                        "skipping repeated match for identifier '{0}': '{1}'".format(
                            identifier, line
                        )
                    )
        return match
