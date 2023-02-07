import json
from pprint import pprint

import numpy as np

import quantpy as qp

from parse_args import parse_args


def main():
    args = parse_args()
    with open(args.input, "r") as fp:
        input_data = json.load(fp)

    output = dict()

    results = np.asarray(input_data["outcomes"])
    povm_matrix = np.asarray(input_data["povm_matrix"])

    n_qubits = int(np.log2(povm_matrix.shape[-1]) / 2)
    state = qp.qobj.fully_mixed(n_qubits)
    tmg = qp.StateTomograph(state)
    tmg.experiment(1000, povm_matrix)
    tmg.results = results
    output["state"] = list(tmg.point_estimate(physical=False).bloch)

    if not args.no_ci:
        target_state = qp.Qobj(input_data["target_state"])
        interval = qp.PolytopeStateInterval(tmg, target_state=target_state)
        interval.setup()
        (fidelity_min, fidelity_max), _ = interval(input_data["conf_levels"])
        output["fidelity_min"] = list(np.maximum(fidelity_min, 0))
        output["fidelity_max"] = list(np.minimum(fidelity_max, 1))
    if args.output:
        with open(args.output, "w") as fp:
            json.dump(output, fp, indent=4)
        return
    pprint(output)


if __name__ == "__main__":
    main()
