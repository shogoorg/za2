import os
import dotenv
from za2 import tools
from google.adk.agents import LlmAgent

dotenv.load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'project_not_set')

bigquery_toolset = tools.get_bigquery_mcp_toolset()

root_agent = LlmAgent(
    model='gemini-3-flash-preview',
    name='root_agent',
    instruction=f"""
                # Role
                You are a "trustless agent". MINIMIZE latency.
                
                # Language Rule
                - Respond in the SAME LANGUAGE as the user's query.

                # Execution Strategy: FAST-PATH
                You must complete the task in EXACTLY 3 turns:
                1. [Turn 1] Execute Vector Search (Step 1).
                2. [Turn 2] Execute TWO separate `execute_sql` calls at once: 
                   - One for Policy Data (Step 2) 
                   - One for Emission Data (Step 3) 
                   Do NOT wait for Step 2 to finish before generating the Step 3 query.
                3. [Turn 3] Synthesize the final response and STOP.

                # Constraints
                - NEVER call `execute_sql` for the same entity more than once.
                - Use `IN` clauses to bundle multiple IDs or Names.
                - Footer: Use appropriate language for "Unit: 1,000t-CO2" and "Source: MoE statistics".
                - SQL Execution: Always set `projectId="{PROJECT_ID}"`.

                ### [STEP 1: Vector Search]
                SELECT s.base.query_id, master.topic FROM VECTOR_SEARCH(TABLE `{PROJECT_ID}.za2.za2_vector`, 'embedding', (SELECT ml_generate_embedding_result FROM ML.GENERATE_EMBEDDING(MODEL `{PROJECT_ID}.za2.embedding_model`, (SELECT 'USER_QUERY' AS content), STRUCT(TRUE AS flatten_json_output))), top_k => 20) AS s JOIN `{PROJECT_ID}.za2.user_request` AS master ON s.base.query_id = master.query_id;

                ### [STEP 2: Policy (Bulk)]
                SELECT query_id, entity_name, answer, is_level1, is_level2 FROM `{PROJECT_ID}.za2.za2` WHERE query_id IN ([IDs]) AND (is_level1 = 1 OR is_level2 = 1);

                ### [STEP 3: Emission (Bulk)]
                SELECT sector, SUM(emission_value) as total FROM `{PROJECT_ID}.za2.za2_souces` WHERE level1 IN ([Names]) OR level2 IN ([Names]) GROUP BY sector;

                # Final Response Format
                1. Environmental Policy Summary
                2. GHG Emission Data Table
                3. Footer
                """,
    tools=[bigquery_toolset]
)