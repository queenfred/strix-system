import boto3
import time
import logging
from botocore.exceptions import NoCredentialsError, BotoCoreError
from core.config.settings import AWS_CONFIG

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

class S3Client:
    def __init__(self, config=AWS_CONFIG):
        self.s3_client = None
        self.config = config
    

    def conn_s3(self):
        """
        Establece la conexión con S3 y devuelve la instancia del cliente.
        """
        try:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=self.config["ACCESS_KEY"],
                aws_secret_access_key=self.config["SECRET_KEY"]
            )
            print("✅ Conexión a S3 establecida con éxito.")
            return self  # 🔹 Retorna el objeto `S3Client`, no solo `boto3.client`
        except Exception as e:
            print(f"❌ Error al conectar con S3: {e}")
            return None


    def list_buckets(self):
        """
        Lista los buckets de S3 disponibles si la conexión es exitosa.
        """
        if not self.s3_client:
            logger.error("⚠️ No hay una conexión activa a S3.")
            return None
        try:
            response = self.s3_client.list_buckets()
            buckets = [bucket["Name"] for bucket in response["Buckets"]]
            logger.info(f"📦 Buckets disponibles: {buckets}")
            return buckets
        except BotoCoreError as e:
            logger.error(f"❌ Error al listar los buckets de S3: {e}")
            return None
