# Source Mapping and Attribution

## Original academic artifacts
The source materials describe a Customer Sales Database System created for Saint Louis University coursework. The report credits Sameer Basha Md H, Brendan Gillow, and Chandra Kiran Challamalasetti. The presentation credits the same team using expanded names.

Keep that attribution when publishing. Add your personal contribution separately and accurately.

## How each source was used
| Source artifact | Contribution to this repository |
|---|---|
| `Customer Sales Database - IR.sql` | Original entities, keys, sample records, function, procedure, and analytical-view concepts |
| `Python Data Insertion - IR (2).ipynb` | Python/pyodbc insertion workflow and deterministic data-generation concept |
| `Data Visualization - IR (2).ipynb` | Sales-by-customer, sales-by-state, and top-product analysis concepts |
| `Customer Sales Database System - IR.docx` | Objectives, 3NF rationale, table descriptions, run instructions, and conclusion |
| `Customer Orders Database – Final Project Overview.pptx` | Five-table model intent, presentation narrative, tools, views, and visualization goals |

## Modernization decisions
1. Added a dedicated Product table to reconcile the report's four-table implementation with the presentation's five-table design.
2. Replaced hard-coded SQL Server credentials with a portable SQLite demo database.
3. Added order status, data lineage, indexes, reusable queries, tests, CI, and deployment documentation.
4. Converted static matplotlib/seaborn outputs into interactive Plotly/Streamlit experiences.
5. Corrected one fractional legacy quantity (`0.5`) to one unit because the source schema defined quantity as an integer.
