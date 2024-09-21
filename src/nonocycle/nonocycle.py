from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import TypeAlias

import networkx as nx
from networkx.classes.digraph import DiGraph
from pydeps import cli, py2depgraph
from pydeps.depgraph import DepGraph
from pydeps.target import Target


def get_pydep_graph(package_path: Path, package_name: str) -> DepGraph:
    """Creates an import graph using pydeps."""
    # Based on https://github.com/thebjorn/pydeps/issues/59
    options = cli.parse_args([str(package_path), "--no-show", "--only", package_name])
    target = Target(options["fname"])
    with target.chdir_work():
        dep_graph = py2depgraph.py2dep(target, **options)
    return dep_graph


def get_nx_graphs(graph: DepGraph) -> dict[str, DiGraph]:
    """Creates a networkx graph for each (sub)package in the pydeps graph."""
    graphs = {}
    for node in graph.sources.values():
        path = node.name.split(".")
        for level in range(1, len(path)):
            parent_path = ".".join(path[:level])
            curr_name = ".".join(path[: level + 1])
            curr_graph = graphs.setdefault(parent_path, nx.DiGraph())
            edges = []
            for imp_name in node.imports:
                imp_path = imp_name.split(".")
                if len(imp_path) <= level:
                    continue
                imp_name_level = ".".join(imp_path[: level + 1])
                if curr_name != imp_name_level:
                    curr_graph.add_edges_from([(curr_name, imp_name_level)])
                    imports = curr_graph.nodes[curr_name].setdefault("imports", set())
                    imports.add(imp_name)
            curr_graph.add_edges_from(edges)
    return graphs


# Dict from model name to dict of cycles.
# Each cycle dict has as key a tuple with the first and last node in the cycle and
# as value a dict from node name to list of imports from the next node in the cycle.
Cycles: TypeAlias = dict[str, dict[tuple[str, str], dict[str, list[str]]]]


def find_cycles(graphs: dict[str, DiGraph]) -> Cycles:
    """Finds cycles within each networkx graph."""
    cycles = {}
    for name, graph in sorted(graphs.items()):
        graph_cycles = cycles.setdefault(name, {})
        for cycle in nx.simple_cycles(graph):
            node_start = cycle[0]
            node_end = cycle[-1]
            cycle_key = (node_start, node_end)
            if cycle_key in graph_cycles:
                continue
            cycle_info = graph_cycles.setdefault(cycle_key, {})
            # Add first node to the end to close the cycle.
            cycle.append(cycle[0])
            for node1, node2 in zip(cycle[:-1], cycle[1:]):
                imports = cycle_info.setdefault(node1, [])
                for import_name in graph.nodes[node1]["imports"]:
                    if import_name.startswith(node2):
                        imports.append(import_name)
    return cycles


def print_cycles(cycles: Cycles, verbose: bool) -> None:
    total_num_cycles = 0
    for module_name, module_cycles in cycles.items():
        if not module_cycles and not verbose:
            continue
        print(module_name)
        num_cycles = len(module_cycles)
        total_num_cycles += num_cycles
        if num_cycles > 0:
            print(f"  Num Potential Cycles: {num_cycles}")
        for i, cycle in enumerate(module_cycles.values()):
            print(f"  Cycle {i}")
            for name, imports in sorted(cycle.items()):
                print(f"    {name} imports")
                for imp in imports:
                    print(f"      {imp}")
    print()


def main(package_path: Path, package_name: str, verbose: bool = False):
    graph = get_pydep_graph(package_path=package_path, package_name=package_name)
    nx_graphs = get_nx_graphs(graph=graph)
    cycles = find_cycles(graphs=nx_graphs)
    print_cycles(cycles=cycles, verbose=verbose)
    num_modules = len(cycles)
    num_cycles = sum(len(module_cycles) for module_cycles in cycles.values())
    if num_cycles:
        print(
            f"Oh no! Found {num_cycles} potential cycle(s) in {num_modules} module(s)."
        )
        sys.exit(1)
    else:
        print(f"No cycle(s) found in {num_modules} module(s).")


def cli_entrypoint() -> None:
    parser = ArgumentParser()
    parser.add_argument("package_path", type=Path)
    parser.add_argument("--package-name", type=str)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    main(
        package_path=args.package_path,
        package_name=args.package_name or args.package_path.name,
        verbose=args.verbose,
    )
