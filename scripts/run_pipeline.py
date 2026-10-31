from src.pipeline import ETLPipeline


if __name__ == "__main__":

    pipeline = ETLPipeline()

    result = pipeline.run(
        file_path="data/input/customers.csv",
        run_id="RUN002"
    )

    print("\nETL PIPELINE SUMMARY")
    print("--------------------")

    for key, value in result.items():
        print(f"{key}: {value}")