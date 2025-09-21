import json, os, re
with open("deployment.json", "r") as f:
    deployment_map = json.load(f)["branch-to-env-regex"]
branch = os.environ['GITHUB_REF_NAME']
env = None
print(deployment_map)
for pattern, target in deployment_map.items():
    if re.fullmatch(pattern, branch):
        env = target
if env is None:
    raise Exception(f"Could not match branch '{branch}' to any env")
print(f"Matched branch '{branch}' to env '{env}'")
with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
    gh_out.write(f"env={env}\n")