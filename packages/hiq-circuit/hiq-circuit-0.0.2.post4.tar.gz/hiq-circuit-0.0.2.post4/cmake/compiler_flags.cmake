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

# C++ standard falgs
set(CMAKE_CXX_STANDARD 14) # might decay to C++11
set(CMAKE_CXX_EXTENSIONS OFF)

# Always generate position independent code
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# ------------------------------------------------------------------------------

check_compiler_flags(_compile_flags_release "-ffast-math /fp:fast -fast"
                     "-O3 /Ox")

if(USE_NATIVE_INTRINSICS)
  # Add -march=native regardless of Debug/Release
  check_compiler_flags(_archnative_flag
                       "-march=native -xHost /QxHost /arch:AVX2")
  if(NOT _archnative_flag_cxx)
    message(FATAL_ERROR "Unable to find compiler flag for compiler intrinsics")
  endif()
elseif(USE_INTRIN)
  check_compiler_flags(_avx2_flag "-mavx2 -xCORE-AVX2 /QxCORE-AVX2 /arch:AVX2")
endif()

add_compile_options(
  "$<$<AND:$<COMPILE_LANGUAGE:CXX>,$<BOOL:${USE_NATIVE_INTRINSICS}>>:${_archnative_flag_cxx}>"
  "$<$<AND:$<COMPILE_LANGUAGE:CXX>,$<NOT:$<BOOL:${USE_NATIVE_INTRINSICS}>>>:${_avx2_flag_cxx}>"
  "$<$<AND:$<CONFIG:RELEASE>,$<COMPILE_LANGUAGE:CXX>>:${_compile_flags_release_cxx}>"
  )
