from security.services.health_check import health_check

#from pipeline.services.portfolio_pipeline import PortfolioPipelineProcessor
#from pipeline.services.siniestro_processor_service import SiniestroPipelineProcessor

if __name__ == "__main__":
    status = health_check()
    print(f"🔍 Estado de conexiones: {status}")


    """processor = PortfolioPipelineProcessor()
    result = processor.run_pipeline()
    print(result)


    file_path = "C:/Desarrollo/pipeline-master/test/output/limpieza_siniestro_pipeline.csv"
    processor = SiniestroPipelineProcessor(file_path)
    result = processor.run_pipeline()
    print(result)"""

    