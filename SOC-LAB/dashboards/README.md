# Dashboards folder

This folder is a placeholder for Kibana saved objects (dashboards, visualizations).
To export/import dashboards in Kibana:
1. Open Kibana → Management → Saved Objects.
2. Click Export (from another instance) to get JSONs, or Import to import the JSON files present here.
3. If you import objects, ensure index patterns referenced by the saved objects exist in Kibana first (create an index pattern that matches the log index, e.g., 'syslog-*').

You can create dashboards manually by using Discover → Visualize → Dashboard and then save/export them into JSON files here.
