import argparse
from src.adc_orchestrator import ADCPipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    
    pipeline = ADCPipeline(...)
    with open(args.file, "rb") as f:
        pipeline.process_file(args.file, f.read())
