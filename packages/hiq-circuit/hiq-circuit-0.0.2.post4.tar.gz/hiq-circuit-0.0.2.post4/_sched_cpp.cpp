//   Copyright 2019 <Huawei Technologies Co., Ltd>
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.

#include <pybind11/complex.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>

#include <vector>
#include "scheduler/cluster_scheduler.h"
#include "scheduler/convertors.h"
#include "scheduler/definitions.h"
#include "scheduler/swap_scheduler.h"

namespace py = pybind11;

PYBIND11_MODULE(_sched_cpp, m)
{
     py::class_<SwapScheduler>(m, "SwapScheduler")
         .def(py::init<std::vector<std::vector<id_num_t>>,
                       std::vector<std::vector<id_num_t>>, std::vector<bool>,
                       int, int, bool>())
         .def("ScheduleSwap", &SwapScheduler::ScheduleSwap)
         .def("GetComamndsFromMsk", &SwapScheduler::GetComamndsFromMsk);
     py::class_<ClusterScheduler>(m, "ClusterScheduler")
         .def(py::init<std::vector<std::vector<id_num_t>>,
                       std::vector<std::vector<id_num_t>>, std::vector<bool>,
                       std::vector<id_num_t>, std::vector<id_num_t>, int>())
         .def("ScheduleCluster", &ClusterScheduler::ScheduleCluster);

     m.attr("all_defined_symbols") = std::vector<py::object>({m.attr("SwapScheduler"),
							      m.attr("ClusterScheduler")});
}
