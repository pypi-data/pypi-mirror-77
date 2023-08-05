// Copyright (C) 2019. Huawei Technologies Co., Ltd.
// Copyright 2017 ProjectQ-Framework (www.projectq.ch)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <algorithm>
#include <cmath>
#include <complex>
#include <cstdlib>
#include <functional>
#include <vector>

#include "cintrin.hpp"

#define LOOP_COLLAPSE1 2
#define LOOP_COLLAPSE2 3
#define LOOP_COLLAPSE3 4
#define LOOP_COLLAPSE4 5
#define LOOP_COLLAPSE5 6

#include "kernel1.hpp"
#include "kernel2.hpp"
#include "kernel3.hpp"
#ifdef INTRIN_CF
#     include "kernel4_cf.hpp"
namespace intrin {
     using intrin_cf::kernel_compute;
     using intrin_cf::kernel_core;
     using intrin_cf::kernelK;
}  // intrin
#else
#     include "kernel4.hpp"
#endif  // INTRIN_CF
#include "kernel5.hpp"
