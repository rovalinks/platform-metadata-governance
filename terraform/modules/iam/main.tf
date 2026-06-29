locals {
  iam_bindings = flatten([
    for sa_name, roles in var.service_account_roles : [
      for role in roles : {
        service_account = sa_name
        email           = var.service_account_emails[sa_name]
        role            = role
      }
    ]
  ])
}

resource "google_project_iam_member" "service_account_roles" {

  for_each = {
    for binding in local.iam_bindings :
    "${binding.service_account}-${binding.role}" => binding
  }

  project = var.project_id

  role = each.value.role

  member = "serviceAccount:${each.value.email}"
}