// Copyright 2019 Google LLC. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef FORMUX_H_
#define FORMUX_H_

#ifdef _OPENMP
# include "parfor.h"
  namespace qsim {
    using For = ParallelFor;
  }
#else
# include "seqfor.h"
  namespace qsim {
    using For = SequentialFor;
  }
#endif

#endif  // FORMUX_H_
