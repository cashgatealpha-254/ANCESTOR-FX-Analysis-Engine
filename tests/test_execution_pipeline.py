import time
import MetaTrader5 as mt5

from environment.execution_pipeline import ExecutionPipeline

# IMPORTANT:
# Replace this import with the actual class/function
# your analysis engine uses to generate setups.
from environment.analysis_engine import AnalysisEngine


SYMBOL = "GBPUSD"
HORIZON = "INTRADAY"

RUNS = 20
DELAY_SECONDS = 2


def main():

    if not mt5.initialize():

        print("❌ MT5 initialization failed")
        raise SystemExit

    try:

        analyzer = AnalysisEngine()

        pipeline = ExecutionPipeline(

            risk_percent=1.0,

            max_risk_percent=2.0,

            minimum_rr=2.0,

            max_positions=1,

            dry_run=True
        )

        print()
        print("=" * 80)
        print("LIVE ANALYSIS → EXECUTION PIPELINE STRESS TEST")
        print("=" * 80)

        print()
        print(f"Symbol: {SYMBOL}")
        print(f"Horizon: {HORIZON}")
        print(f"Runs: {RUNS}")
        print("Mode: DRY RUN")
        print()

        for run in range(1, RUNS + 1):

            print("-" * 80)
            print(f"TEST RUN {run}/{RUNS}")
            print("-" * 80)

            # ==================================================
            # GET REAL MARKET ANALYSIS
            # ==================================================

            setup = analyzer.analyze(
                symbol=SYMBOL,
                horizon=HORIZON
            )

            if setup is None:

                print("ANALYSIS: No setup produced")
                time.sleep(DELAY_SECONDS)
                continue

            print()
            print("ANALYSIS OUTPUT")

            for key, value in setup.items():

                print(
                    f"{key}: {value}"
                )

            # ==================================================
            # EXECUTION PIPELINE
            # ==================================================

            result = pipeline.execute(
                setup
            )

            print()
            print("PIPELINE RESULT")

            for key, value in result.items():

                print(
                    f"{key}: {value}"
                )

            time.sleep(
                DELAY_SECONDS
            )

        print()
        print("=" * 80)
        print("STRESS TEST COMPLETE")
        print("=" * 80)

    finally:

        mt5.shutdown()


if __name__ == "__main__":

    main()