# Docker Containerization Experiment

Today I learned about Docker containerization, where I take a terminal that I would normally open for each application operation and instead I containerize them so docker can do it on its own with `docker compose up --build`

health results from `docker ps`:

CONTAINER ID   IMAGE                       COMMAND                  CREATED              STATUS                        PORTS                                             NAMES
38f513e67d8c   abtalksai-cohort-frontend   "streamlit run app.p…"   About a minute ago   Up About a minute             0.0.0.0:8501->8501/tcp, [::]:8501->8501/tcp       abtalksai-cohort-frontend-1
0435a49353dc   abtalksai-cohort-backend    "uvicorn coverage-ch…"   About a minute ago   Up **About a minute (healthy)**   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp       abtalksai-cohort-backend-1
3c2dea89f8c9   ollama/ollama               "/bin/ollama serve"      21 minutes ago       Up About a minute             0.0.0.0:11434->11434/tcp, [::]:11434->11434/tcp   abtalksai-cohort-ollama-1

We can see that the health check I included in the backend Dockerfile is functional and working. Success.