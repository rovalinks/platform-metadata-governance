output "trigger_name" {
  value = google_eventarc_trigger.this.name
}

output "trigger_id" {
  value = google_eventarc_trigger.this.id
}

output "trigger_names" {

  value = keys(
    google_eventarc_trigger.this
  )

}