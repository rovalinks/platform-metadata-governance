output "registry_bucket" {

  value       = module.registry_bucket.bucket_name
  description = "The URL (gs://) of the created registry bucket."

}

output "eventarc_trigger" {

  value = (
    var.deploy_cloud_run
    ? module.eventarc[0].trigger_name
    : null
  )

  description = "Eventarc trigger name"

}