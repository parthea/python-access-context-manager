# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import synthtool as s
import synthtool.gcp as gcp
from synthtool import tmp
from synthtool.languages import python
from synthtool.sources import git

# ----------------------------------------------------------------------------
#  Add templated files
# ----------------------------------------------------------------------------
common = gcp.CommonTemplates()
templated_files = common.py_library()
s.move(
    templated_files, excludes=["noxfile.py", ".coveragerc", ".gitignore",],
)

s.shell.run(["nox", "-s", "generate_protos"])
s.shell.run(["nox", "-s", "blacken"], hide_output=False)

# Add license headers
python.fix_pb2_headers()

LICENSE = """
# Copyright 2020 Google LLC
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
# limitations under the License."""

PB2_GRPC_HEADER = r"""(\# Generated by the gRPC Python protocol compiler plugin\. DO NOT EDIT!$)
(.*?$)"""

s.replace(
    "**/*_pb2_grpc.py",
    PB2_GRPC_HEADER,
    fr"{LICENSE}\n\n\g<1>\n\n\g<2>",  # add line breaks to avoid stacking replacements
)
