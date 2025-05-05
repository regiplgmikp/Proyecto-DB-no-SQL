# Do it by Regina Plascencia Gómez

# 1. Import the necessary libraries

import csv
import json
import pydgraph
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# 2. Define the schema for the database

def create_schema(client):
    schema = """
    type agentes{

    }

    type clientes{
    
    }

    type empresas{
    
    }

    type tickets{
    
    }
    
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op)