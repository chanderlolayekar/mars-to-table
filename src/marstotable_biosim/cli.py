import argparse
import json
from pathlib import Path

from .simulation import Simulation

def main():
    parser = argparse.ArgumentParser(description="Run the Mars to Table simulation")
    parser.add_argument("--scenario", default="nominal")
    parser.add_argument("--output", default="results/")
    args = parser.parse_args()

    config_path = Path(__file__).parent / "config" / f"{args.scenario}.json"
    if config_path.exists():
        config = json.loads(config_path.read_text())
    else:
        config = {"crew_size": 15}

    sim = Simulation(config)
    results = sim.run(hours=168)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(out_dir / "biosim_results.csv", index=False)
    print("Simulation complete")

if __name__ == "__main__":
    main()
