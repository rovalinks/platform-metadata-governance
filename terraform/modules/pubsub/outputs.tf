output "topic_name" {
  value = google_pubsub_topic.governance.name
}

output "topic_id" {
  value = google_pubsub_topic.governance.id
}

output "subscription_name" {
  value = google_pubsub_subscription.governance.name
}