variable "client_id" {
    type = string
    description = "github client id"
    sensitive = true
}

variable "client_secret" {
    type = string
    description = "github client secret"
    sensitive = true
}

variable "SECRET_KEY" {
    type = string
    description = "Flask Secret Key"
    sensitive = true
}

variable "azure_client_secret" {
    description = "Azure service principal secret"
    sensitive = true
}

variable "azure_client_id" {
    description = "Azure service principal id"
    sensitive   = true
}

variable "azure_subscription_id" {
    description = "The subscription ID for the azure provider"
    sensitive   = true
}

variable "azure_tenant_id" {
    description = "Azure tenant id"
    sensitive   = true
}

variable "FLASK_APP" {
    description = "Flask app path"
}

variable "FLASK_ENV" {
    description = "Flask environment file to use"
}

variable "WEBSITES_PORT" {
    description = "Flask server configuration"
}

variable "LOG_LEVEL" {
    description = "log level configuration"
}

variable "LOGGLY_TOKEN" {
    type = string
    description = "Loggly customer token"
    sensitive   = true
}