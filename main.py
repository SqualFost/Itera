from itera.cli import main
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ITERA",
        description="local CLI agent"
    )

    parser.add_argument("--model", required=False, type=str)
    args = parser.parse_args()
    model = args.model
    main(model)
