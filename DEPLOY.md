# Deployment

> ![CAUTION]
> This is a work in progress documentation, make sure to take it with precaution

## Setup

### Google Cloud Project setup

Enable APIs in your new project:

- Cloud Build
    - e.g: https://console.cloud.google.com/apis/library/cloudbuild.googleapis.com?project=mapswipe-alpha-01
- Cloud Function
    - e.g: https://console.cloud.google.com/apis/library/cloudfunctions.googleapis.com?project=mapswipe-alpha-01
- Firebase Extensions
    - e.g: https://console.cloud.google.com/apis/api/firebaseextensions.googleapis.com/metrics?project=mapswipe-alpha-01
- Cloud Billing
    - e.g: https://console.cloud.google.com/apis/api/cloudbilling.googleapis.com/metrics?project=mapswipe-alpha-01

### Service account for deployment

- https://console.cloud.google.com/iam-admin/serviceaccounts
- Select project (e.g: "mapswipe-alpha-01")
- Create service account
  - Create service account
    - **Service account name:** firebase-deploy
    - **Service account ID:** firebase-deploy
    - Create and continue
- Permissions (Add)
  - Role: Cloud Function Developer
  - Role: Firebase Admin
  - Role: Firebase Hosting Admin
  - Role: Firebase Rules Admin
  - Role: Service Account User
- Principals with access (Skip)
- Select the new service account (firebase-deploy...)
- Keys
  - Add key
  - Create new key
  - JSON
  - Create
