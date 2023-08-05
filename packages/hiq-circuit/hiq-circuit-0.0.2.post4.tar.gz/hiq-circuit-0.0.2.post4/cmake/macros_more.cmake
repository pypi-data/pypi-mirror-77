# ==============================================================================
#
# Copyright 2020 <Huawei Technologies Co., Ltd>
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
#
# ==============================================================================

set(_python_targets)

function(pybind11_add_module target)
  _pybind11_add_module(${target} ${ARGN})

  list(APPEND _doc_targets ${target})
  set(_doc_targets ${_doc_targets} PARENT_SCOPE)
  list(APPEND _python_targets ${target})
  set(_python_targets ${_python_targets} PARENT_SCOPE)

  string(TOUPPER ${target} _TARGET)

  if(${target}_LIBRARY_OUTPUT_DIRECTORY)
    set(${_TARGET}_LIBRARY_OUTPUT_DIRECTORY
        ${${target}_LIBRARY_OUTPUT_DIRECTORY})
  endif()

  # Properly set output directory for a target so that during an installation
  # using either 'pip install' or 'python3 setup.py install' the libraries get
  # built in the proper directory
  if(${_TARGET}_LIBRARY_OUTPUT_DIRECTORY)
    set_target_properties(${target}
                          PROPERTIES LIBRARY_OUTPUT_DIRECTORY
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY}
                                     LIBRARY_OUTPUT_DIRECTORY_DEBUG
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY}
                                     LIBRARY_OUTPUT_DIRECTORY_RELEASE
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY}
                                     LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY}
                                     LIBRARY_OUTPUT_DIRECTORY_MINSIZEREL
                                     ${${_TARGET}_LIBRARY_OUTPUT_DIRECTORY})
  elseif(IS_PYTHON_BUILD)
    message(
      WARNING "IS_PYTHON_BUILD=ON but ${_TARGET}_LIBRARY_OUTPUT_DIRECTORY "
              "was not defined! The shared library for target ${target} "
              "will probably not be copied to the correct directory.")
  endif(${_TARGET}_LIBRARY_OUTPUT_DIRECTORY)
endfunction()

# ==============================================================================
