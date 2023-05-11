import subprocess

def call_near_interaction_script(operation, *args):
    result = subprocess.run(
        ["node", "near_interaction.js", operation, *args],
        capture_output=True,
        text=True,
    )
    if result.stderr:
        raise Exception(result.stderr)
    return result.stdout.strip()
