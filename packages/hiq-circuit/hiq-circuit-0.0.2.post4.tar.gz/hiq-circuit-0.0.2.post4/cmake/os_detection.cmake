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

set(_os_found FALSE)
macro(find_os_name name files paths)
  string(TOUPPER ${name} NAME)

  if(NOT _os_found)
    find_file(${NAME}_FOUND ${files} PATHS ${paths})
    if(${NAME}_FOUND)
      set(_os_found TRUE)
      set(OS_NAME
          ${name}
          CACHE STRING "Operating system name" FORCE)
    endif(DEBIAN_FOUND)
  endif()
endmacro()

if(UNIX)
  if(APPLE)
    set(OS_NAME
        "OSX"
        CACHE STRING "Operating system name" FORCE)
  else()
    # Tested with:
    #   - ArchLinux
    #   - CentOS
    #   - Debian
    #   - Fedora
    #   - OpenSUSE (leap)
    #   - Ubuntu

    set(_regex "^ID=\"?([a-zA-Z]+)\"?")
    file(STRINGS /etc/os-release OS_NAME_RAW REGEX ${_regex})
    string(REGEX MATCH ${_regex} OS_NAME_RAW ${OS_NAME_RAW})
    set(OS_NAME ${CMAKE_MATCH_1})

    set(OS_RELEASE 0)
    set(_regex "^VERSION_ID=\"?([0-9\\.]+)\"?")
    file(STRINGS /etc/os-release OS_RELEASE_RAW REGEX ${_regex})
    if(OS_RELEASE_RAW)
      string(REGEX MATCH ${_regex} OS_RELEASE_RAW ${OS_RELEASE_RAW})
      set(OS_RELEASE ${CMAKE_MATCH_1})
    endif()
  endif() # APPLE
endif() # UNIX
