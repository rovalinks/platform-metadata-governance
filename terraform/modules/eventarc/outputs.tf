output "trigger_names" {

  description = "Eventarc trigger names"

  value = [
    for trigger in google_eventarc_trigger.this :
    trigger.name
  ]
}

output "trigger_ids" {

  description = "Eventarc trigger ids"

  value = [
    for trigger in google_eventarc_trigger.this :
    trigger.id
  ]
}