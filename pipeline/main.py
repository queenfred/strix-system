from pipeline.services.portfolio_pipeline import PortfolioPipelineProcessor


def main():
    """
    Punto de entrada del módulo pipeline: ejecuta el procesamiento de la cartera.
    """
    processor = PortfolioPipelineProcessor()
    result = processor.run_pipeline()
    print(result)


if __name__ == "__main__":
    main()