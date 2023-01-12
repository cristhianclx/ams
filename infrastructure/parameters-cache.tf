resource "aws_ssm_parameter" "cache_host" {
  name        = "/${var.name}/cache/host"
  description = "${local.slug}-cache-host"
  type        = "String"
  value       = aws_elasticache_cluster.cache_redis.cache_nodes[0].address

  overwrite = true
  tier      = "Standard"
}
resource "aws_ssm_parameter" "cache_port" {
  name        = "/${var.name}/cache/port"
  description = "${local.slug}-cache-port"
  type        = "String"
  value       = aws_elasticache_cluster.cache_redis.cache_nodes[0].port

  overwrite = true
  tier      = "Standard"
}
