from abc import abstractmethod
from functools import reduce
from itertools import combinations, accumulate, repeat, product
from networkx import has_path
from typing import List, Union, Tuple, cast, Any

from sweetpea.backend import BackendRequest
from sweetpea.internal import get_all_levels
from sweetpea.primitives import Factor, Transition, Window, SimpleLevel, DerivedLevel, get_external_level_name, get_internal_level_name
from sweetpea.logic import to_cnf_tseitin
from sweetpea.base_constraint import Constraint
from sweetpea.design_graph import DesignGraph


"""
Abstract class for Blocks. Contains the required data, and defines abstract
methods that other blocks _must_ implement in order to work correctly.
"""
class Block:
    def __init__(self,
                 design: List[Factor],
                 crossing: List[Factor],
                 constraints: List[Constraint],
                 cnf_fn) -> None:
        self.design = list(design).copy()
        self.crossing = list(crossing).copy()
        self.constraints = list(constraints).copy()
        self.cnf_fn = cnf_fn
        self.complex_factors_or_constraints = True
        self.min_trials = 0
        self.exclude = cast(List[Tuple[int]], [])
        self.__validate()

    def __validate(self):
        # TODO: Make sure factor names are unique
        from sweetpea.constraints import MinimumTrials, Exclude
        for c in self.constraints:
            c.validate(self)
            if isinstance(c, MinimumTrials):
                c.apply(self, None)
            if isinstance(c, Exclude):
                self.exclude.append((c.factor, c.level))

    """
    Indicates the number of trials that are generated per sample for this block
    configuration.

    Analogous to the old __fully_cross_size function.
    """
    @abstractmethod
    def trials_per_sample(self):
        pass

    """
    Indicates the number of variables that are present in each trial.

    Analogous to the old __design_size function.
    """
    @abstractmethod
    def variables_per_trial(self):
        pass

    """
    Indicates the number of variables that are present in the core variable grid.
    this does not include variables used to encode complex windows.

    In a design _without_ complex windows, this is equivalent to variables_per_sample.
    """
    @abstractmethod
    def grid_variables(self):
        pass

    """
    Indicates the total number of variables needed to encode the core experiment
    description.

    Alternatively stated, this returns the number of variables in the formula
    that constitute the independent support.
    """
    def variables_per_sample(self):
        return reduce(lambda sum, f: sum + self.variables_for_factor(f), self.design, 0)

    """
    Indicates the number of variables needed to encode this factor.
    """
    def variables_for_factor(self, f: Factor) -> int:
        trial_list = range(1, self.trials_per_sample() + 1)
        return reduce(lambda sum, t: sum + len(f.levels) if f.applies_to_trial(t) else sum, trial_list, 0)

    """
    Determines whether a given factor is in this block.
    """
    def has_factor(self, factor: Factor) -> Factor:
        if (type(factor) is not Factor):
            raise ValueError('Non-factor argument to has_factor.')
        if factor in self.design:
            return factor
        return cast(Factor, None)

    """
    Returns the first index for this variable in a trial sequence representing the given factor and level.
    (0 based)
    """
    def first_variable_for_level(self, factor: Factor, level: Any ) -> int:
        if (type(level) is not SimpleLevel and type(level) is not DerivedLevel):
            print("Attempt to find first variable for a non-level object " + str(level))
        if factor.has_complex_window():
            offset = 0
            complex_factors = filter(lambda f: f.has_complex_window(), self.design)
            for f in complex_factors:
                if f == factor:
                    offset += f.levels.index(level)
                    break
                else:
                    offset += self.variables_for_factor(f)

            return self.grid_variables() + offset

        else:
            simple_factors = list(filter(lambda f: not f.has_complex_window(), self.design))
            simple_levels = get_all_levels(simple_factors)
            return simple_levels.index((factor, level))

    """
    Given a factor and a trial number (1-based) this function will return a list of the variables
    representing the levels of the given factor for that trial. The variable list is also 1 based.
    """
    def factor_variables_for_trial(self, f: Factor, t: int) -> List[int]:
        if not f.applies_to_trial(t):
            raise ValueError('Factor does not apply to trial #' + str(t) + ' f=' + str(f))

        previous_trials = sum(map(lambda trial: 1 if f.applies_to_trial(trial + 1) else 0, range(t))) - 1
        initial_sequence = list(map(lambda l: self.first_variable_for_level(f, l), list(filter(lambda l: (f, l) not in self.exclude, f.levels))))
        offset = 0
        if f.has_complex_window():
            offset = len(f.levels) * previous_trials
        else:
            offset = self.variables_per_trial() * previous_trials
        return list(map(lambda n: n + offset + 1, initial_sequence))

    """
    Given a trial number (1-based) this function will return a list of lists of the variables
    that pertain to that trial.

    For example, for stroop-2 with a congruency level, this method would return the following
    for trial #1:

        [[1, 2], [3, 4], [5, 6]]

    If a transition were involved, and it didn't apply to level one, then the factor would
    have an empty list:

        [[1, 2], [3, 4], []]
    """
    def variable_list_for_trial(self, t: int) -> List[List[int]]:
        variables = cast(List[List[int]], [])
        for f in self.design:
            # Skip factors that don't apply.
            if not f.applies_to_trial(t):
                variables.append([])
                continue

            variables.append(self.factor_variables_for_trial(f, t))

        return variables;

    """
    Given a variable number from the SAT formula, this method will return
    the associated factor and level name.
    """
    def decode_variable(self, variable: int) -> Tuple[Factor, Union[SimpleLevel, DerivedLevel]]:
        # Shift to zero-based index
        variable -= 1

        if variable < self.grid_variables():
            variable = variable % self.variables_per_trial()
            simple_factors = list(filter(lambda f: not f.has_complex_window(), self.design))
            simple_tuples = get_all_levels(simple_factors)
            return simple_tuples[variable]
        else:
            complex_factors = list(filter(lambda f: f.has_complex_window(), self.design))
            for f in complex_factors:
                start = self.first_variable_for_level(f, f.levels[0])
                end = start + self.variables_for_factor(f)
                if variable in range(start, end):
                    tuples = get_all_levels([f])
                    return tuples[(variable - start) % len(f.levels)]

        raise RuntimeError('Unable to find factor/level for variable!')

    """
    Apply all constraints to build a BackendRequest. Formerly known as __desugar in __init.py__
    """
    def build_backend_request(self) -> BackendRequest:
        fresh = 1 + self.variables_per_sample()
        backend_request = BackendRequest(fresh)

        from sweetpea.constraints import MinimumTrials
        for c in self.constraints:
            if isinstance(c, MinimumTrials):
                continue
            c.apply(self, backend_request)

        return backend_request

    """
    Given a trial number (1 based), factor, and level, this method will return the SAT
    variable that represents that selection. Only works for factors without complex windows at the
    moment.
    """
    def get_variable(self, trial_number: int, level: Tuple[Factor, Any]) -> int:
        f = level[0]
        if f.has_complex_window():
            raise ValueError("get_variable doens't handle complex windows yet! factor={}".format(f))

        return self.build_variable_list(level)[trial_number - 1]

    """
    Given a specific level (factor + level pair), this method will return the list of variables
    that correspond to that level in each trial in the encoding.
    """
    def build_variable_list(self, level: Tuple[Factor, Union[SimpleLevel, DerivedLevel]]) -> List[int]:
        if (type(level[0]) is not Factor):
            raise ValueError('First element in level argument to variable list builder must be a FACTOR.')
        if (type(level[1]) is not SimpleLevel and type(level[1]) is not DerivedLevel):
            raise ValueError('Second element in level argument to variable list builder must be a SIMPLE LEVEL or a DERIVED LEVEL.')
        if level[0].has_complex_window():
            return self.__build_complex_variable_list(level)
        else:
            return self.__build_simple_variable_list(level)

    def __build_simple_variable_list(self, level: Tuple[Factor, Union[SimpleLevel, DerivedLevel]]) -> List[int]:
        first_variable = self.first_variable_for_level(level[0], level[1]) + 1
        design_var_count = self.variables_per_trial()
        num_trials = self.trials_per_sample()
        return list(accumulate(repeat(first_variable, num_trials), lambda acc, _: acc + design_var_count))

    def __build_complex_variable_list(self, level: Tuple[Factor, Union[SimpleLevel, DerivedLevel]]) -> List[int]:
        factor = level[0]
        level_count = len(factor.levels)
        n = int(self.variables_for_factor(factor) / level_count)
        start = self.first_variable_for_level(level[0], level[1]) + 1
        return reduce(lambda l, v: l + [start + (v * level_count)], range(n), [])


"""
A fully-crossed block. This block generates as many trials as needed to fully
cross all levels across all factors in the block's crossing.
"""
class FullyCrossBlock(Block):
    def __init__(self, design, crossing, constraints, require_complete_crossing=True, cnf_fn=to_cnf_tseitin):
        super().__init__(design, crossing, constraints, cnf_fn)
        self.require_complete_crossing = require_complete_crossing
        if not self.require_complete_crossing:
            print("WARNING: Some combinations have been excluded, this crossing may not be complete!")
        self.__validate()

    def __validate(self):
        self.__validate_crossing()

    def __validate_crossing(self):
        dg = DesignGraph(self.design).graph
        combos = combinations(self.crossing, 2)

        warnings = []
        template = "'{}' depends on '{}'"
        for c in combos:
            if has_path(dg, c[0].factor_name, c[1].factor_name):
                warnings.append(template.format(c[0].factor_name, c[1].factor_name))
            elif has_path(dg, c[1].factor_name, c[0].factor_name):
                warnings.append(template.format(c[1].factor_name, c[0].factor_name))

        if warnings:
            print("WARNING: There are dependencies between factors in the crossing. This may lead to unsatisfiable designs.\n" + reduce(lambda accum, s: accum + s + "\n", warnings, ""))

    """
    Given a factor f, and a crossing size, this function will compute the number of trials
    required to fully cross f with the other factors.

    For example, if f is a transition, it doesn't apply to trial 1. So when the crossing_size
    is 4, we'd actually need 5 trials to fully cross with f.

    This is a helper for trials_per_sample.
    """
    def __trials_required_for_crossing(self, f: Factor, crossing_size: int) -> int:
        trial = 0
        counter = 0
        while counter != crossing_size:
            trial += 1
            if f.applies_to_trial(trial):
                counter += 1
        return trial

    def trials_per_sample(self):
        crossing_size = self.crossing_size()
        required_trials = list(map(lambda f: self.__trials_required_for_crossing(f, crossing_size), self.crossing))
        required_trials.append(self.min_trials)
        return max(required_trials)

    def variables_per_trial(self):
        # Factors with complex windows are excluded because we don't want variables allocated
        # in every trial when the window spans multiple trials.
        grid_factors = filter(lambda f: not f.has_complex_window(), self.design)
        return sum([len(factor.levels) for factor in grid_factors])

    def grid_variables(self):
        return self.trials_per_sample() * self.variables_per_trial()

    """
    This method is responsible for determining the number of trials that should be excluded from the full
    crossing, based on any `Exclude` constraints that the user provides.
    A single `Exclude` constraint may prevent multiple crossings, depending on the derivation function used.
    """
    def __count_exclusions(self):
        from sweetpea.constraints import Exclude

        excluded_crossings = set()

        # Get the exclude constraints.
        exclusions = list(filter(lambda c: isinstance(c, Exclude), self.constraints))
        if not exclusions:
            return 0

        # If there are any, generate the full crossing as a list of tuples.
        levels_lists = [list(f.levels) for f in self.crossing]
        all_crossings = list(product(*levels_lists))

        for constraint in exclusions:
            if constraint.factor.has_complex_window():
                # If the excluded factor has a complex window, then we don't need
                # to reduce the sequence length. What if the transition being excluded
                # is in the crossing? If it is, then they shouldn't be excluding it.
                # We should give an error if we detect that.
                continue

            # Retrieve the derivation function that defines this exclusion.
            excluded_level = constraint.level

            if type(excluded_level) is SimpleLevel:
                for c in all_crossings:
                    if excluded_level in c:
                        excluded_crossings.add(get_internal_level_name(c[0]) + ", " + get_internal_level_name(c[1]))
            else:
                # For each crossing, extract the levels for this derviation function, and execute it.
                for c in all_crossings:
                    args = [get_external_level_name(c[i]) for i in map(lambda f: self.crossing.index(f), excluded_level.window.args)]
                    # Invoking the fn this way is only ok because we only do this for WithinTrial windows.
                    # With complex windows, it wouldn't work due to the list aspect for each argument.
                    if excluded_level.window.fn(*args):
                        excluded_crossings.add(get_internal_level_name(c[0]) + ", " + get_internal_level_name(c[1]))
        return len(excluded_crossings)

    def crossing_size(self):
        crossing_size = self.crossing_size_without_exclusions()
        if not self.require_complete_crossing:
            crossing_size -= self.__count_exclusions()
        return crossing_size

    def crossing_size_without_exclusions(self):
        return reduce(lambda sum, factor: sum * len(factor.levels), self.crossing, 1)

    def draw_design_graph(self):
        dg = DesignGraph(self.design)
        dg.draw()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

"""
A multiple-crossed block. This block generates as many trials as needed to
cross the levels across factors mentioned as lists in the block's crossing.
"""
class MultipleCrossBlock(Block):
    def __init__(self, design, crossing, constraints, require_complete_crossing=True, cnf_fn=to_cnf_tseitin):
        super().__init__(design, [], constraints, cnf_fn)
        self.crossings = crossing
        self.require_complete_crossing = require_complete_crossing
        if not self.require_complete_crossing:
            print("WARNING: Some combinations have been excluded, this crossing may not be complete!")
        self.__validate()

    def __validate(self):
        self.__validate_crossing()

    def __validate_crossing(self):
        dg = DesignGraph(self.design).graph
        warnings = []
        template = "'{}' depends on '{}'"
        for crossing in self.crossings:
            combos = combinations(crossing, 2)

            for c in combos:
                if has_path(dg, c[0].factor_name, c[1].factor_name):
                    warnings.append(template.format(c[0].factor_name, c[1].factor_name))
                elif has_path(dg, c[1].factor_name, c[0].factor_name):
                    warnings.append(template.format(c[1].factor_name, c[0].factor_name))

        if warnings:
            print("WARNING: There are dependencies between factors in the crossing. This may lead to unsatisfiable designs.\n" + reduce(lambda accum, s: accum + s + "\n", warnings, ""))

    """
    Given a factor f, and a crossing size, this function will compute the number of trials
    required to fully cross f with the other factors.

    For example, if f is a transition, it doesn't apply to trial 1. So when the crossing_size
    is 4, we'd actually need 5 trials to fully cross with f.

    This is a helper for trials_per_sample.
    """
    def __trials_required_for_crossing(self, f: Factor, crossing_size: int) -> int:
        trial = 0
        counter = 0
        while counter != crossing_size:
            trial += 1
            if f.applies_to_trial(trial):
                counter += 1
        return trial

    def trials_per_sample(self):
        crossing_size = self.crossing_size()
        required_trials = list(map(max, list(map(lambda c: list(map(lambda f: self.__trials_required_for_crossing(f, crossing_size), c)), self.crossings))))
        required_trials.append(self.min_trials)
        # required_trials = list(map(lambda f: self.__trials_required_for_crossing(f, crossing_size), self.crossing))
        return max(required_trials)

    def variables_per_trial(self):
        # Factors with complex windows are excluded because we don't want variables allocated
        # in every trial when the window spans multiple trials.
        grid_factors = filter(lambda f: not f.has_complex_window(), self.design)
        return sum([len(factor.levels) for factor in grid_factors])

    def grid_variables(self):
        return self.trials_per_sample() * self.variables_per_trial()

    """
    This method is responsible for determining the number of trials that should be excluded from the full
    crossing, based on any `Exclude` constraints that the user provides.
    A single `Exclude` constraint may prevent multiple crossings, depending on the derivation function used.
    """
    def __count_exclusions(self):
        from sweetpea.constraints import Exclude

        excluded_crossings = set()

        # Get the exclude constraints.
        exclusions = list(filter(lambda c: isinstance(c, Exclude), self.constraints))
        if not exclusions:
            return 0

        # If there are any, generate the full crossing as a list of tuples.
        levels_lists = [list(f.levels) for f in self.crossing]
        all_crossings = list(product(*levels_lists))

        for constraint in exclusions:
            if constraint.factor.has_complex_window():
                # If the excluded factor has a complex window, then we don't need
                # to reduce the sequence length. What if the transition being excluded
                # is in the crossing? If it is, then they shouldn't be excluding it.
                # We should give an error if we detect that.
                continue

            # Retrieve the derivation function that defines this exclusion.
            excluded_level = constraint.level

            # For each crossing, extract the levels for this derviation function, and execute it.
            for c in all_crossings:
                args = [get_external_level_name(c[i]) for i in map(lambda f: self.crossing.index(f), excluded_level.window.args)]
                # Invoking the fn this way is only ok because we only do this for WithinTrial windows.
                # With complex windows, it wouldn't work due to the list aspect for each argument.

                if excluded_level.window.fn(*args):
                    excluded_crossings.add(get_internal_level_name(c[0]) + ", " + get_internal_level_name(c[1]))

        return len(excluded_crossings)

    def crossing_size(self):
        crossing_size = self.crossing_size_without_exclusions()
        if not self.require_complete_crossing:
            crossing_size -= self.__count_exclusions()
        return crossing_size

    def crossing_size_without_exclusions(self):
        return max(map(lambda c: reduce(lambda sum, factor: sum * len(factor.levels), c, 1), self.crossings))

    def draw_design_graph(self):
        dg = DesignGraph(self.design)
        dg.draw()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
