resource "google_tags_tag_key" "this" {

  for_each = toset(var.tag_keys)

  parent = "organizations/${var.organization_id}"

  short_name = each.value

  description = "Platform managed TagKey: ${each.value}"
}