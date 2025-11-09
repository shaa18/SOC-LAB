# SOC-LAB — Security Operations Center Simulation

**Author:** Shashank  
**GitHub:** [@shaa18](https://github.com/shaa18)

---

## Overview
SOC-LAB is a self-contained Security Operations Center (SOC) simulation environment designed for learning and experimentation.  
It helps students, analysts, and developers understand how a SOC operates — from log collection and event generation to analysis and visualization.

This setup uses Docker to deploy an Elasticsearch and Kibana stack, with a Python-based log generator to simulate system and network events.  
The project structure is simple and easy to extend for research or training purposes.

---

## Project Structure

| Folder | Description |
|---------|-------------|
| docker/ | Contains Docker configuration and the compose file for Elasticsearch and Kibana. |
| tools/ | Contains Python scripts for log and event generation. |
| dashboards/ | Includes sample Kibana dashboard templates and instructions. |
| .gitignore, LICENSE | Standard repository configuration and license information. |

---

## Getting Started

### 1. Start the SOC environment
Run the following command to start Elasticsearch and Kibana locally:

## 2. Generate logs

Use the Python script to generate test logs:

```bash
python tools/log_generator.py
```
## 3. Access Kibana

Once the containers are running, open your browser and go to:

```text


http://localhost:5601
```
```bash
docker-compose -f docker/docker-compose.yml up -d
```

## Objectives
- Understand how logs flow through a SOC setup.
- Practice analyzing simulated events in Kibana.
- Learn how to use SIEM tools for detection and alerting.
- Develop practical familiarity with Elasticsearch and Docker.

---

## Technologies Used
- Python
- Docker and Docker Compose
- Elasticsearch
- Kibana

---

## Future Enhancements
- Add Splunk or Wazuh integration for SIEM comparison.
- Implement automated alert rules and detection logic.
- Include a threat simulation module for advanced analysis.
- Develop sample incident response workflows and playbooks.

---

## License
This project is distributed under the MIT License.  
You are free to use, modify, and distribute this project with appropriate credit to the author.


