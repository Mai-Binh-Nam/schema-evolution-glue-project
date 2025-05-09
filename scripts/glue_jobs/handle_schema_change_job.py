import sys
import boto3
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Add utils directory to path for AWS Glue environment
import os
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)

# Import custom logger
try:
    from utils.logger import setup_logging
except ImportError:
    # Fallback logging if module can't be imported
    import logging
    def setup_logging(log_level=logging.INFO):
        logger = logging.getLogger('glue_schema_evolution')
        logger.setLevel(log_level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger

# Set up logger
logger = setup_logging()

def get_job_args():
    """Get job arguments from Glue job parameters"""
    return getResolvedOptions(sys.argv, [
        'JOB_NAME',
        'source_path',
        'target_path',
        'database_name',
        'table_name'
    ])

def create_dynamic_frame(glue_context, source_path, format="json"):
    """Create a DynamicFrame from source data"""
    logger.info(f"Reading data from {source_path}")
    return glue_context.create_dynamic_frame.from_options(
        connection_type="s3",
        connection_options={
            "paths": [source_path],
            "recurse": True
        },
        format=format
    )

def handle_schema_evolution(dynamic_frame):
    """
    Apply schema evolution strategies using DynamicFrame's resolveChoice 
    to handle schema drift automatically
    """
    logger.info("Applying schema evolution strategies")
    
    # Different strategies to handle schema changes:
    # 1. CAST - try to cast the column to expected type
    # 2. PROJECT - drop columns that don't match expected type
    # 3. MAKE_STRUCT - convert inconsistent/different typed columns into structs
    # 4. MATCH_CATALOG - match to catalog schema
    
    # Here we're using CAST as a default strategy for all fields
    resolved_frame = dynamic_frame.resolveChoice(choice="CAST:STRING")
    
    # Alternative: You could resolve specific fields differently
    # resolved_frame = dynamic_frame.resolveChoice(specs=[
    #     ("problematic_column_1", "CAST:INT"),
    #     ("problematic_column_2", "MAKE_STRUCT"),
    #     ("problematic_column_3", "PROJECT")
    # ])
    
    return resolved_frame

def write_to_target(dynamic_frame, glue_context, target_path, format="parquet"):
    """Write the DynamicFrame to the target location"""
    logger.info(f"Writing data to {target_path}")
    glue_context.write_dynamic_frame.from_options(
        frame=dynamic_frame,
        connection_type="s3",
        connection_options={
            "path": target_path,
            "partitionKeys": ["year", "month", "day"]
        },
        format=format
    )

def update_glue_catalog(glue_client, database_name, table_name, target_path):
    """Update the Glue Data Catalog with the latest schema"""
    logger.info(f"Updating Glue Catalog for {database_name}.{table_name}")
    
    # You could start a crawler here or update the table directly
    # For this example, we'll assume a crawler will be run separately

def main():
    # Get job parameters
    args = get_job_args()
    
    # Initialize Spark and Glue context
    sc = SparkContext()
    glue_context = GlueContext(sc)
    spark = glue_context.spark_session
    job = Job(glue_context)
    job.init(args['JOB_NAME'], args)
    
    # Log job start
    logger.info(f"Starting Glue job: {args['JOB_NAME']}")
    
    # Extract paths and table info from arguments
    source_path = args['source_path']
    target_path = args['target_path']
    database_name = args['database_name']
    table_name = args['table_name']
    
    # Create DynamicFrame from source
    source_dyf = create_dynamic_frame(glue_context, source_path)
    
    # Print schema before resolution
    logger.info("Schema before resolution:")
    source_dyf.printSchema()
    
    # Apply schema evolution strategies
    resolved_dyf = handle_schema_evolution(source_dyf)
    
    # Print schema after resolution
    logger.info("Schema after resolution:")
    resolved_dyf.printSchema()
    
    # Add partition columns (example)
    df = resolved_dyf.toDF()
    df = df.withColumn("year", F.year(F.current_date()))
    df = df.withColumn("month", F.month(F.current_date()))
    df = df.withColumn("day", F.dayofmonth(F.current_date()))
    partitioned_dyf = DynamicFrame.fromDF(df, glue_context, "partitioned_data")
    
    # Write to target
    write_to_target(partitioned_dyf, glue_context, target_path)
    
    # Update Glue Data Catalog
    glue_client = boto3.client('glue')
    update_glue_catalog(glue_client, database_name, table_name, target_path)
    
    # Log job completion
    logger.info(f"Completed Glue job: {args['JOB_NAME']}")
    
    # Commit the job
    job.commit()

if __name__ == "__main__":
    main()
