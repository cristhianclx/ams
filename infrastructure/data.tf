data "aws_acm_certificate" "main" {
  domain   = var.zone
  statuses = ["ISSUED"]
}
data "aws_region" "self" {}
data "aws_route53_zone" "main" {
  name         = var.zone
  private_zone = false
}
