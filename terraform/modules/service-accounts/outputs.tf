output "emails" {
  value = {
    for key, sa in google_service_account.this :
    key => sa.email
  }
}