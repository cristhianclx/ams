stage = "main"

name    = "ams.demo.pe/main"
website = "ams.demo.pe"

zone = "demo.pe"

database_type    = "postgres"
database_version = "14.5"
database_size    = "db.t3.micro"

database_user     = "api"
database_password = "password"
database_port     = 5432

cache_redis_version = "7.0"
cache_redis_size    = "cache.t3.micro"
cache_redis_port    = 6379

ecs_name = "main"

service_port         = 8000
service_health_check = "/ping/"

service_image  = "263424986970.dkr.ecr.us-east-1.amazonaws.com/ams.demo.pe:main"
service_cpu    = 256
service_memory = 512
service_run    = "/code/scripts/settings/main.sh && /code/scripts/migrate.sh && /code/scripts/seed.sh && /code/scripts/run.sh"

service_metrics_cpu_utilization_high_threshold    = 80
service_metrics_cpu_utilization_low_threshold     = 20
service_metrics_memory_utilization_high_threshold = 80

service_scale_desired = 1
service_scale_max     = 1
service_scale_min     = 1

alpha_vantage_api_key = "DU42M4W3530FEJOB"
