# Kubernetes Deployment Notes

Today we are using LangFuse's deployment wrapping to monitor Kubernetes pod deployment and test debugging. 

## Original Build Results

LangFuse refuses to work. I have spent several hours working on it and I quit. kubectl debugging will have to wait for another time.

Future production alerts will contain:

- OpenAI cost ceiling by tokens
- error-rate threshold
- latency threshold
- connection timeouts