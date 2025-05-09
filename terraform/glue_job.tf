# Create Glue Job
resource "aws_glue_job" "schema_evolution_job" {
  name     = var.glue_job_name
  role_arn = var.glue_job_role_arn
  glue_version = "3.0"
  worker_type = "G.1X"
  number_of_workers = 2
  max_retries = 0
  timeout = 2880

  command {
    script_location = "s3://${local.s3_config.bucket}/${local.s3_config.prefix}/scripts/handle_schema_change_job.py"
    python_version = "3"
  }

  default_arguments = {
    "--job-language" = "python"
    "--job-bookmark-option" = "job-bookmark-enable"
    "--enable-metrics" = "true"
    "--enable-continuous-cloudwatch-log" = "true"
    "--source_path" = "s3://${local.s3_config.bucket}/${local.s3_config.prefix}/input/"
    "--target_path" = "s3://${local.s3_config.bucket}/${local.s3_config.prefix}/output/"
    "--database_name" = aws_glue_catalog_database.glue_database.name
    "--table_name" = var.glue_table_name
    "--TempDir" = "s3://${local.s3_config.bucket}/${local.s3_config.prefix}/temp/"
    "--class" = "GlueApp"
  }
}
