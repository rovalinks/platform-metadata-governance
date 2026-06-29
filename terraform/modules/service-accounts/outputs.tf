output "emails" {
  description = "Service account email addresses"

  value = {
    for key, sa in google_service_account.this :
    key => sa.email
  }
}

output "names" {
  description = "Service account resource names"

  value = {
    for key, sa in google_service_account.this :
    key => sa.name
  }
}