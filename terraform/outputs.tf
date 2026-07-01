output "registry_bucket" {

  value = module.registry_bucket.bucket_name
  description = "The URL (gs://) of the created registry bucket."

}