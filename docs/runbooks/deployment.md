# Deployment Runbook

## Deployment Flow

1. Developer pushes code to GitHub.
2. GitHub Actions authenticates using Workload Identity Federation.
3. Cloud Build builds the container image.
4. Cloud Build pushes the image to Artifact Registry.
5. Terraform deploys the approved image to Cloud Run.

## Rollback

Cloud Run supports traffic management between revisions.

Previous revisions remain available for rollback until deleted.
