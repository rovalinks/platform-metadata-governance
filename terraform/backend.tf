terraform {
  backend "gcs" {
    bucket = "platform-metadata-demo-tfstate"
    prefix = "terraform/state"
  }
}