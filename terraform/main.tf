module "artifact_registry" {

  source = "./modules/artifact-registry"

  project_id = var.project_id

  region = var.region

  repository_id = var.artifact_registry_repository

  description = var.artifact_registry_description

}

module "service_accounts" {
  source = "./modules/service-accounts"

  project_id       = var.project_id
  service_accounts = var.service_accounts
}