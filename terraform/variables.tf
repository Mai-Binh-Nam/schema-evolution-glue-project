variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for storing data"
  type        = string
}

variable "glue_database_name" {
  description = "Name of the Glue Database"
  type        = string
  default     = "schema_evolution_db"
}

variable "glue_crawler_name" {
  description = "Name of the Glue Crawler"
  type        = string
  default     = "schema_evolution_crawler"
}

variable "glue_job_name" {
  description = "Name of the Glue Job"
  type        = string
  default     = "schema_evolution_job"
}

variable "glue_table_name" {
  description = "Name of the Glue Table"
  type        = string
  default     = "customer_orders"
}

variable "raw_table_name" {
  description = "Name of the raw table"
  type        = string
  default     = "raw_data"
}

variable "processed_table_name" {
  description = "Name of the processed table"
  type        = string
  default     = "processed_data"
}

variable "glue_job_role_arn" {
  description = "ARN of the IAM role for the Glue job"
  type        = string
}