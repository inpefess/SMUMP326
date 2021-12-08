# Copyright 2022 Boris Shminke
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
""" a generator for equations between finite categories morphisms """
from typing import List


class FiniteCategory:
    """
    >>> print(len(FiniteCategory(2, 1).equations))
    31
    """

    def __init__(self, number_of_objects: int, hom_set_size: int):
        self.number_of_objects = number_of_objects
        self.hom_set_size = hom_set_size
        self.equations = (
            self.identity_axioms()
            + self.non_composable_axioms()
            + self.generate_non_equations()
        )
        self.enumerate_constants()

    def identity_axioms(self) -> List[str]:
        """
        :returns: a list of Mace4 formulae like:
            c110 * c123 = c123.
            c456 * c660 = c456.
        """
        equations = []
        for src in range(self.number_of_objects):
            for trg in range(self.number_of_objects):
                for i in range(self.hom_set_size):
                    equations += [
                        f"c{src}{src}0 * c{src}{trg}{i} = c{src}{trg}{i}.",
                        f"c{src}{trg}{i} * c{trg}{trg}0 = c{src}{trg}{i}.",
                    ]
        return sorted(list(set(equations)))

    def non_composable_axioms(self) -> List[str]:
        """
        :returns: a list of Mace4 formulae like:
            c * c = c.
            c123 * c = c.
            c * c456 = c.
            % target of c123 is 2, not equal to 4, source of c456
            c123 * c456 = c.
        """
        equations = ["c * c = c."]
        for src in range(self.number_of_objects):
            for trg in range(self.number_of_objects):
                for i in range(self.hom_set_size):
                    equations += [
                        f"c * c{src}{trg}{i} = c.",
                        f"c{src}{trg}{i} * c = c.",
                    ]
        for src1 in range(self.number_of_objects):
            for trg1 in range(self.number_of_objects):
                for src2 in range(self.number_of_objects):
                    if trg1 != src2:
                        for trg2 in range(self.number_of_objects):
                            equations += [
                                f"c{src1}{trg1}{i} * c{src2}{trg2}{j} = c."
                                for i in range(self.hom_set_size)
                                for j in range(self.hom_set_size)
                            ]
        return sorted(list(set(equations)))

    def generate_non_equations(self) -> List[str]:
        """
        :returns: a list of Mace4 negated equations like:
            c123 * c245 != c678. (it can be only c14_)
            c123 * c245 != c. (morphisms c123 and c245 are composable)
        """
        non_equations = []
        for src1 in range(self.number_of_objects):
            for trg1 in range(self.number_of_objects):
                for src2 in range(self.number_of_objects):
                    for trg2 in range(self.number_of_objects):
                        if src1 != src2 or trg1 != trg2:
                            non_equations += [
                                f"c{src1}{interim}{i}"
                                + " * "
                                + f"c{interim}{trg1}{j}"
                                + " != "
                                + f"c{src2}{trg2}{k}."
                                for i in range(self.hom_set_size)
                                for j in range(self.hom_set_size)
                                for k in range(self.hom_set_size)
                                for interim in range(self.number_of_objects)
                                if not (
                                    src1 == interim
                                    and i == 0
                                    or interim == trg1
                                    and j == 0
                                )
                            ]
                        else:
                            non_equations += [
                                f"c{src1}{interim}{i}"
                                + " * "
                                + f"c{interim}{trg1}{j}"
                                + " != "
                                + "c."
                                for i in range(self.hom_set_size)
                                for j in range(self.hom_set_size)
                                for interim in range(self.number_of_objects)
                                if not (
                                    src1 == interim
                                    and i == 0
                                    or interim == trg1
                                    and j == 0
                                )
                            ]
        return sorted(list(set(non_equations)))

    def enumerate_constants(self) -> None:
        """
        change string constants to natural numbers starting from zero

        :returns:
        """
        for eq_ind, _ in enumerate(self.equations):
            for ord_num, const_name in enumerate(
                [
                    f"c{i}{j}{k}"
                    for i in range(self.number_of_objects)
                    for j in range(self.number_of_objects)
                    for k in range(self.hom_set_size)
                ]
            ):
                self.equations[eq_ind] = self.equations[eq_ind].replace(
                    const_name, str(ord_num + 1)
                )
            self.equations[eq_ind] = self.equations[eq_ind].replace("c", "0")
