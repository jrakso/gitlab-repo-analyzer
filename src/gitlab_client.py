import requests

GITLAB_API = "https://gitlab.lnu.se/api/v4"


class GitlabClient:
    def __init__(self, token: str):
        self.headers = {
            "PRIVATE-TOKEN": token
        }

    def get_group_projects(self, group_id: str):
        url = f"{GITLAB_API}/groups/{group_id}/projects"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()
