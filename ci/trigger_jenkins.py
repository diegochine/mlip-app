import os
import requests
import argparse

def trigger_jenkins_job(job_name: str) -> None:
    """
    Triggers a Jenkins job using the Jenkins REST API.
    Requires the following environment variables to be set:
      - JENKINS_URL: Base URL of the Jenkins server.
      - JENKINS_USER: Jenkins username.
      - JENKINS_API_TOKEN: Jenkins API token.
    """
    jenkins_url = os.environ.get("JENKINS_URL")
    user = os.environ.get("JENKINS_USER")
    token = os.environ.get("JENKINS_API_TOKEN")
    
    if not jenkins_url or not user or not token:
        raise Exception("Jenkins URL, user, or API token not set in environment variables.")
    
    build_url = f"{jenkins_url}/job/{job_name}/build"
    response = requests.post(build_url, auth=(user, token))
    
    if response.status_code == 201:
        print("Jenkins job triggered successfully.")
    else:
        raise Exception(f"Failed to trigger Jenkins job. Status code: {response.status_code}, response: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger a Jenkins job via REST API.")
    parser.add_argument("job_name", help="Name of the Jenkins job to trigger")
    args = parser.parse_args()
    trigger_jenkins_job(args.job_name)
