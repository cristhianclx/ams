terraform {
  required_version = ">=1.3.5"

  backend "s3" {
    bucket  = "infrastructure.demo.pe"
    key     = "tf/main/market-stock.tfstate"
    encrypt = "true"
    region  = "sa-east-1"
  }
}
