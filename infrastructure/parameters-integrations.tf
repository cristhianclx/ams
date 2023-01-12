resource "aws_ssm_parameter" "stripe_sk" {
  name        = "/${var.name}/integrations/alpha-vantage-api-key"
  description = "${local.slug}-integrations-alpha-vantage-api-key"
  type        = "SecureString"
  value       = var.alpha_vantage_api_key

  key_id    = "alias/aws/ssm"
  overwrite = true
  tier      = "Standard"
}
