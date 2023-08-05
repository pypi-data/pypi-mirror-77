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

#ifndef SWAPPING_HPP
#define SWAPPING_HPP

#include <glog/logging.h>

#include <boost/format.hpp>
#include <cstdint>
#include <vector>

#include "funcs.hpp"
#include "simulator-mpi/SwapArrays.hpp"

namespace swapping
{
template<class State_Vector_Iterator, class Buffer_Iterator>
struct BufferExchange {
    static void buffer_to_state(const State_Vector_Iterator state_vector, Buffer_Iterator rbuffer, uint64_t i, uint64_t j) {
         state_vector[j] = rbuffer[i];
    };

    static void state_to_buffer(const State_Vector_Iterator state_vector, Buffer_Iterator sbuffer, uint64_t i, uint64_t j) {
         sbuffer[i] = state_vector[j];
    };
};

template <size_t n_bits>
struct SwappingBase
{
     template <class T, class Iterator, void buffer_exchange(const Iterator, T*, uint64_t, uint64_t)>
     static size_t doCalc(const Iterator state_vector, uint64_t n,
                          size_t start_free_idx, T* svalues,
                          const std::vector<uint64_t>& swap_bits)
     {
          size_t free_idx_end = start_free_idx + n;
          for (size_t free_idx = start_free_idx; free_idx < free_idx_end;
               ++free_idx) {
               size_t res_free_idx = free_idx;
               for (size_t bit_idx = 0; bit_idx < n_bits; ++bit_idx) {
                    uint64_t sw_bit = swap_bits[bit_idx];
                    uint64_t l = res_free_idx & (sw_bit - 1);
                    uint64_t r = res_free_idx - l;

                    res_free_idx = 2 * r + l;
               }

               for (size_t swap_idx = 0; swap_idx < (1ul << n_bits);
                    ++swap_idx) {
                    size_t res_idx = res_free_idx;
                    size_t res_swap_idx = 0;
                    for (size_t bi = 0; bi < n_bits; ++bi) {
                         bool bv = swap_idx & (1ul << bi);
                         res_swap_idx
                             |= bv * (swap_bits[swap_bits[n_bits + bi]]);
                    }

                    res_idx += res_swap_idx;
                    size_t idx = n * swap_idx + free_idx - start_free_idx;
                    buffer_exchange(state_vector, svalues, idx, res_idx);
               }
          }

          return free_idx_end;
     }
};

template <size_t n_bits_max>
struct Swapping
{
     template <class T, class Iterator, void buffer_exchange(const Iterator, T*, uint64_t, uint64_t)>
     static size_t calcSwap(uint64_t n_bits, const Iterator state_vector,
                            uint64_t n, size_t start_free_idx, T* svalues,
                            const std::vector<uint64_t>& swap_bits)
     {
          if (n_bits == n_bits_max) {
               return SwappingBase<n_bits_max>::template doCalc<T, Iterator, buffer_exchange>(state_vector, n,
                                                       start_free_idx, svalues, swap_bits);
          }
          else {
               return Swapping<n_bits_max - 1>::template calcSwap<T, Iterator, buffer_exchange>(
                   n_bits, state_vector, n, start_free_idx, svalues, swap_bits);
          }
     }
};

template <>
struct Swapping<0>
{
     template <class T, class Iterator, void buffer_exchange(const Iterator, T*, uint64_t, uint64_t)>
     static size_t calcSwap(uint64_t, const Iterator, uint64_t, size_t, T*,
                             const std::vector<uint64_t>&)
     {
          return 0;
     }
};

}  // namespace swapping

#endif  // SWAPPING_HPP
