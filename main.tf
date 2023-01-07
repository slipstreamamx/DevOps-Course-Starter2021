terraform {

  backend "azurerm" {
    resource_group_name  = "bearxapp_ProjectExercise"
    storage_account_name = "storageaccounttfstate27"
    container_name       = "containertfstate27"
    key                  = "terraform.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
}

provider "azurerm" {
  features {}
  
  subscription_id = var.azure_subscription_id
  client_id       = var.azure_client_id
  client_secret   = var.azure_client_secret
  tenant_id       = var.azure_tenant_id
}

data "azurerm_resource_group" "main" {
    name = "bearxapp_ProjectExercise"

}

resource "azurerm_service_plan" "main" {
    name = "bears-app-service-plan-tr" 
    location = data.azurerm_resource_group.main.location 
    resource_group_name = data.azurerm_resource_group.main.name 
    os_type = "Linux"
    sku_name = "B1"
}

resource "azurerm_linux_web_app" "main" {
    name = "bearxapp-tr" 
    location = data.azurerm_resource_group.main.location 
    resource_group_name = data.azurerm_resource_group.main.name 
    service_plan_id = azurerm_service_plan.main.id 

 site_config { 
    application_stack { 
        docker_image = "slipsreamamx/todo-app" 
        docker_image_tag = "prod-latest" 
    } 
 } 

 app_settings = { 
    "CLIENT_ID" = var.client_id
    "CLIENT_SECRET" = var.client_secret
    "DATABASE" = azurerm_cosmosdb_mongo_database.main.name
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGODB_CONNECTION_STRING" = azurerm_cosmosdb_account.main.connection_strings[0]
    "SECRET_KEY" = var.SECRET_KEY
    "FLASK_APP" = var.FLASK_APP
    "FLASK_ENV" = var.FLASK_ENV
    }
}

resource "azurerm_cosmosdb_account" "main" {

  name                = "bearscosmosdb-tr"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }

  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  capabilities {
    name = "EnableServerless"
  }

  lifecycle {
    prevent_destroy = true
  }

  geo_location {
    failover_priority = 0
    location          = "uksouth"
    zone_redundant    = false
  }
  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }
  offer_type = "Standard"

}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "bearxapp-database-tr"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
  
  lifecycle {
    prevent_destroy = false
  }  
}