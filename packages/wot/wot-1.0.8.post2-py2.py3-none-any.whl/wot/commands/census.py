#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import anndata
import pandas as pd

import wot
import wot.io


def create_parser():
    parser = argparse.ArgumentParser(
        description='Generate ancestor census for each time point given an initial cell set')
    parser.add_argument('--tmap', help=wot.commands.TMAP_HELP, required=True)
    parser.add_argument('--cell_set', help=wot.commands.CELL_SET_HELP, required=True)
    parser.add_argument('--day', help='The starting timepoint at which to consider the cell sets', required=True)
    parser.add_argument('--out', help='Output files prefix', default='census')
    return parser


def main(args):
    tmap_model = wot.tmap.TransportMapModel.from_directory(args.tmap)
    cell_sets_matrix = wot.io.read_sets(args.cell_set)
    cell_sets = wot.io.convert_binary_dataset_to_dict(cell_sets_matrix)
    populations = tmap_model.population_from_cell_sets(cell_sets, at_time=args.day)

    timepoints, census = tmap_model.ancestor_census(cell_sets_matrix, *populations)

    obs = pd.DataFrame(index=timepoints)

    for i in range(len(census)):
        res = anndata.AnnData(census[i], obs, cell_sets_matrix.var)
        wot.io.write_dataset(res, args.out + '_' + populations[i].name, output_format='txt')
