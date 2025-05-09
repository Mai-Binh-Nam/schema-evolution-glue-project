# Create Glue Database
resource "aws_glue_catalog_database" "glue_database" {
  name = var.glue_database_name
}


# Create Glue Crawler
resource "aws_glue_crawler" "schema_evolution_crawler" {
  name          = var.glue_crawler_name
  role          = var.glue_job_role_arn
  database_name = aws_glue_catalog_database.glue_database.name

  s3_target {
    path = "s3://${local.s3_config.bucket}/${local.s3_config.prefix}/output/"
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }

  configuration = jsonencode({
    Version = 1.0
    CrawlerOutput = {
      Partitions = { AddOrUpdateBehavior = "InheritFromTable" }
    }
  })
}