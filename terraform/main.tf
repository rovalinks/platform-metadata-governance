module "artifact_registry" {

  source = "./modules/artifact-registry"

  project_id    = var.project_id
  region        = var.region
  repository_id = var.artifact_registry_repository
  description   = var.artifact_registry_description

}

module "service_accounts" {
  source = "./modules/service-accounts"

  project_id       = var.project_id
  service_accounts = var.service_accounts
}

module "iam" {
  source                 = "./modules/iam"
  project_id             = var.project_id
  service_account_emails = module.service_accounts.emails
  service_account_roles  = var.service_account_roles
}

module "cloud_run" {
  count                 = var.deploy_cloud_run ? 1 : 0
  source                = "./modules/cloud-run"
  project_id            = var.project_id
  region                = var.region
  service_name          = var.cloud_run.service_name
  image                 = var.cloud_run.image
  service_account_email = module.service_accounts.emails["governance"]
  registry_bucket       = module.registry_bucket.bucket_name
  registry_cache_ttl    = var.registry_cache_ttl
  excluded_buckets      = var.excluded_buckets
  dry_run               = var.dry_run
  log_level             = var.log_level
  bigquery              = var.bigquery
  task_queue            = module.cloud_tasks.queue_name
  cloud_run_url         ="https://metadata-governance-375142238023.europe-west2.run.app"
}

module "eventarc" {
  count                 = var.deploy_cloud_run ? 1 : 0
  source                = "./modules/eventarc"
  project_id            = var.project_id
  region                = var.region
  cloud_run_service     = module.cloud_run[0].service_name
  service_account_email = module.service_accounts.emails["governance"]
  triggers              = var.eventarc.triggers
}

module "workload_identity" {
  source                 = "./modules/workload-identity"
  project_id             = var.project_id
  github_service_account = module.service_accounts.names["github"]
  workload_identity      = var.workload_identity
}

module "registry_bucket" {
  source                     = "./modules/registry-bucket"
  project_id                 = var.project_id
  region                     = var.region
  bucket_name                = var.registry_bucket_name
  governance_service_account = module.service_accounts.emails["governance"]
  github_service_account     = module.service_accounts.emails["github"]
}

module "bigquery" {
  source     = "./modules/bigquery"
  project_id = var.project_id
  region     = var.region
  dataset_id = var.bigquery.dataset_id
}

module "project_services" {

  source = "./modules/project-services"

  project_id = var.project_id

  services = [
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudtasks.googleapis.com",
    "compute.googleapis.com",
    "container.googleapis.com",
    "eventarc.googleapis.com",
    "iam.googleapis.com",
    "logging.googleapis.com",
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "storage.googleapis.com",
  ]
}

module "cloud_tasks" {

  source = "./modules/cloud-tasks"

  project_id = var.project_id
  region     = var.region
  queue_name = "metadata-remediation"
  depends_on = [
    module.project_services
  ]
}