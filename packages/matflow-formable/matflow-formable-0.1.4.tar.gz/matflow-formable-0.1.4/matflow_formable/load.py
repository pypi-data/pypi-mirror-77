'`matflow_formable.load.py`'

import numpy as np
from formable import load_cases

from matflow_formable import (
    input_mapper,
    output_mapper,
    cli_format_mapper,
    register_output_file,
    func_mapper,
)


@func_mapper(task='generate_load_case', method='uniaxial')
def get_uniaxial_load_cases(total_times, num_increments, directions,
                            target_strain_rates=None, target_strains=None,
                            rotations=None, dump_frequency=None):

    if target_strains is None:
        target_strains = [None] * len(total_times)
    elif target_strain_rates is None:
        target_strain_rates = [None] * len(total_times)

    if dump_frequency is None:
        dump_frequency = [1] * len(total_times)

    if rotations is None:
        rotations = [None] * len(total_times)

    all_load_cases = []
    for t, n, eps_dot, eps, d, rot, freq in zip(
        total_times,
        num_increments,
        target_strain_rates,
        target_strains,
        directions,
        rotations,
        dump_frequency,
    ):
        all_load_cases.append(
            load_cases.get_load_case_uniaxial(
                total_time=t,
                num_increments=n,
                direction=d,
                target_strain_rate=eps_dot,
                target_strain=eps,
                rotation=rot,
                dump_frequency=freq,
            )
        )

    out = {'load_case': all_load_cases}

    return out


@func_mapper(task='generate_load_case', method='biaxial')
def get_biaxial_load_cases(total_times, num_increments, directions,
                           target_strain_rates=None, target_strains=None,
                           dump_frequency=None):

    if target_strains is None:
        target_strains = [None] * len(total_times)
    elif target_strain_rates is None:
        target_strain_rates = [None] * len(total_times)

    if dump_frequency is None:
        dump_frequency = [1] * len(total_times)

    all_load_cases = []
    for t, n, eps_dot, eps, d, freq in zip(
        total_times,
        num_increments,
        target_strain_rates,
        target_strains,
        directions,
        dump_frequency,
    ):
        all_load_cases.append(
            load_cases.get_load_case_biaxial(
                total_time=t,
                num_increments=n,
                direction=d,
                target_strain_rate=eps_dot,
                target_strain=eps,
                dump_frequency=freq,
            )
        )

    out = {
        'load_case': all_load_cases,
    }
    return out


@func_mapper(task='generate_load_case', method='plane_strain')
def get_plane_strain_load_cases(total_times, num_increments, directions,
                                target_strain_rates=None, target_strains=None,
                                dump_frequency=None):

    if target_strains is None:
        target_strains = [None] * len(total_times)
    elif target_strain_rates is None:
        target_strain_rates = [None] * len(total_times)

    if dump_frequency is None:
        dump_frequency = [1] * len(total_times)

    all_load_cases = []
    for t, n, eps_dot, eps, d, freq in zip(
        total_times,
        num_increments,
        target_strain_rates,
        target_strains,
        directions,
        dump_frequency,
    ):
        all_load_cases.append(
            load_cases.get_load_case_plane_strain(
                total_time=t,
                num_increments=n,
                direction=d,
                target_strain_rate=eps_dot,
                target_strain=eps,
                dump_frequency=freq,
            )
        )

    out = {
        'load_case': all_load_cases,
    }
    return out


@func_mapper(task='generate_load_case', method='random_2D')
def get_random_2D_load_cases(total_times, num_increments, normal_directions,
                             target_strain_rates=None, target_strains=None,
                             dump_frequency=None):

    if target_strains is None:
        target_strains = [None] * len(total_times)
    elif target_strain_rates is None:
        target_strain_rates = [None] * len(total_times)

    if dump_frequency is None:
        dump_frequency = [1] * len(total_times)

    all_load_cases = []
    for t, n, eps_dot, eps, nd, freq in zip(
        total_times,
        num_increments,
        target_strain_rates,
        target_strains,
        normal_directions,
        dump_frequency,
    ):
        all_load_cases.append(
            load_cases.get_load_case_random_2D(
                total_time=t,
                num_increments=n,
                normal_direction=nd,
                target_strain_rate=eps_dot,
                target_strain=eps,
                dump_frequency=freq,
            )
        )

    out = {
        'load_case': all_load_cases,
    }
    return out


@func_mapper(task='generate_load_case', method='random_3D')
def get_random_3D_load_cases(total_times, num_increments, target_strains, rotation=True,
                             rotation_max_angle=10, rotation_load_case=True,
                             non_random_rotation=None, dump_frequency=None):

    if non_random_rotation is None:
        non_random_rotation = [None] * len(total_times)

    if dump_frequency is None:
        dump_frequency = [1] * len(total_times)

    all_load_cases = []
    for t, n, eps, rot, freq in zip(
        total_times,
        num_increments,
        target_strains,
        non_random_rotation,
        dump_frequency
    ):
        all_load_cases.append(
            load_cases.get_load_case_random_3D(
                total_time=t,
                num_increments=n,
                target_strain=eps,
                rotation=rotation,
                rotation_max_angle=rotation_max_angle,
                rotation_load_case=rotation_load_case,
                non_random_rotation=rot,
                dump_frequency=freq,
            )
        )

    out = {
        'load_case': all_load_cases,
    }
    return out
