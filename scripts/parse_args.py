from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="path to input data file",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        type=str,
        help="path to output file",
        required=False,
    )
    parser.add_argument(
        "--no-ci",
        default=False,
        action="store_true",
        help="removes confidence intervals",
    )
    return parser.parse_args()